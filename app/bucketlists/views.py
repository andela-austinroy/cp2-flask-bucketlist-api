from flask import Blueprint, request, jsonify, abort
from flask_httpauth import HTTPBasicAuth
from flask import url_for, g
from flask_httpauth import HTTPTokenAuth
from itsdangerous import SignatureExpired, BadSignature, TimedJSONWebSignatureSerializer as Serializer
from app import token_signer, db, app
from app.auth.models import User
from app.bucketlists.models import BucketList, BucketListItem

auth = HTTPTokenAuth('Token')


bucketlists = Blueprint('bucketlists', __name__, url_prefix='/bucketlists')

buckets = []


@app.errorhandler(401)
def custom401error(exception):
    return jsonify(exception.description), 401


@app.errorhandler(403)
def custom403error(exception):
    return jsonify(exception.description), 403


@app.errorhandler(404)
def custom404error(exception):
    return jsonify(exception.description), 404


@app.errorhandler(400)
def custom400error(exception):
    return jsonify(exception.description), 400


@auth.verify_token
def verify_auth_token(token):
    s = Serializer(app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
        user = User.query.filter_by(username=data['username']).scalar()
        if user:
            g.user_id = user.id
            return True
    except (SignatureExpired, BadSignature):
        return abort(401, {'message': 'invalid token'})

    return False


@app.route('/')
def home():
    return "Welcome to my bucketlist api"


@app.route('/bucketlists/', methods=['POST'])
@auth.login_required
def create_new_bucketlist():
    """Adds a new bucketlist"""
    name = request.form.get('name')
    created_by = g.user_id
    new_bucketlist = BucketList(name, created_by)
    new_bucketlist.save()
    new_bucketlist.refresh_from_db()
    return jsonify({'Successfully added bucketlist':
                    {'id': new_bucketlist.id,
                     'name': new_bucketlist.name,
                     'date_created': new_bucketlist.date_created,
                     'date_modified': new_bucketlist.date_modified,
                     'created_by': new_bucketlist.created_by
                     }
                    }), 201


@app.route('/bucketlists/', methods=['GET'])
@auth.login_required
def fetch_all_bucketlists():
    """Returns all bucketlists"""

    page_no = request.args.get('page_no', 1)
    limit = request.args.get('limit', 20)
    q_name = request.args.get('q', "")

    bucketlists = BucketList.query.filter_by(
        created_by=g.user_id).filter(
        BucketList.name.like('%{}%'.format(q_name))).paginate(
        int(page_no), int(limit))

    print (bucketlists.items)

    if not bucketlists.items:
        return abort(404, {"error": "No bucketlists added"})
    for bucketlist in bucketlists.items:
        bucket_items = BucketListItem.query.filter_by(
            bucketlist_id=bucketlist.id).all()
        if bucket_items is None:
            list_items = []
        else:
            list_items = [bucket_item.name for bucket_item in bucket_items]
        # buckets.append({'id': bucketlist.id,
        #                 'name': bucketlist.name,
        #                 'items': bucket_items,
        #                 'date_created': bucketlist.date_created,
        #                 'date_modified': bucketlist.date_modified
        #                 })
    return jsonify({
        'Bucketlist': [
            {
                'id': bucketlist.id,
                'name': bucketlist.name,
                'created_by': bucketlist.created_by,
                'items': list_items,
                'date_created': bucketlist.date_created,
                'date_modified': bucketlist.date_modified
            } for bucketlist in bucketlists.items

        ],
        'next': '{}?q={}&limit={}&page={}'.format(
            str(url_for('bucketlists.get_bucketlists', _external=True)),
            str(q_name),
            str(limit),
            str(page_no + 1)) if bucketlists.has_next else None,
        'prev': '{}?q={}&limit={}&page={}'.format(
            str(url_for('bucketlists.get_bucketlists', _external=True)),
            str(q_name),
            str(limit),
            str(page_no - 1)) if bucketlists.has_prev else None
    }), 200


@app.route('/bucketlists/?q=Check', methods=['GET'])
@auth.login_required
def search_bucketlist_by_name():
    pass


@app.route('/bucketlists/<id>', methods=['GET'])
@auth.login_required
def fetch_single_bucketlist(id):
    """Returns a single bucketlist"""
    bucketlist = BucketList.query.filter_by(id=id).first()
    if bucketlist is None:
        return jsonify({"error": "bucketlist not found"}), 404
    items = BucketListItem.query.filter_by(
        bucketlist_id=bucketlist.id).first()
    if items is None:
        items = []
    else:
        items = items.name
    my_bucket = {'id': bucketlist.id,
                 'name': bucketlist.name,
                 'items': items,
                 'date_created': bucketlist.date_created,
                 'date_modified': bucketlist.date_modified
                 }
    return jsonify({'Bucketlist': my_bucket}), 200


@app.route('/bucketlists/<id>', methods=['PUT'])
@auth.login_required
def update_bucketlist(id):
    """Updates a bucketlist's details"""
    update_bucket = BucketList.query.filter_by(
        id=id).scalar()
    if not update_bucket:
        return jsonify({"error": "Bucketlist not found"}), 404
    existing_bucketlist = BucketList.query.filter_by(
        name=request.form.get('name')).first()
    if existing_bucketlist:
        return abort(403,
                     {'error': 'That bucketlist name has already been used'})
    update_bucket.name = request.form.get('name', update_bucket.name)
    update_bucket.save()
    return jsonify({"success": "Changes saved to bucketlist",
                    "name": update_bucket.name
                    }), 200


@app.route('/bucketlists/<id>', methods=['DELETE'])
@auth.login_required
def delete_bucketlist(id):
    delete_db = BucketList.query.filter_by(id=id).scalar()
    if delete_db is None:
        return jsonify({"error": "That bucketlist doesn't exist"}), 404
    db.session.delete(delete_db)
    db.session.commit()
    return "Successfully deleted bucketlist", 200


@app.route('/bucketlists/<id>/items/', methods=['POST'])
@auth.login_required
def add_bucketlist_item(id):
    """Adds an item to an existing bucketlist"""
    bucketlist_id = request.form.get('id')
    bucketlist = BucketList.query.filter_by(id=id).first()
    if not bucketlist:
        return abort(404, {"error": "bucket list does not exist"})
    name = request.form.get('name')
    description = request.form.get('description')
    done = 'false'
    new_bucketlistitem = BucketListItem(name, description, bucketlist_id, done)
    new_bucketlistitem.save()
    new_bucketlistitem.refresh_from_db()
    return jsonify({'Successfully added bucketlist item':
                    {'id': new_bucketlistitem.id,
                     'name': new_bucketlistitem.name,
                     'description': new_bucketlistitem.description,
                     'date_created': new_bucketlistitem.date_created,
                     'date_modified': new_bucketlistitem.date_modified
                     }
                    }), 201


@app.route('/bucketlists/<id>/items/<item_id>', methods=['PUT'])
@auth.login_required
def update_bucketlist_item(id, item_id):
    id = id
    item_id = item_id
    update_bucket_item = BucketListItem.query.filter_by(
        id=item_id, bucketlist_id=id).scalar()
    if not update_bucket_item:
        abort(404, ({"error": "buckelist item not found"}))
    if request.form.get('name'):
        update_bucket_item.name = request.form.get('name')
    if request.form.get('description'):
        update_bucket_item.description = request.form.get(
            'description', update_bucket_item.description)
    if request.form.get('done'):
        print request.form.get('done')
        if request.form.get('done').upper() != "TRUE" \
                and request.form.get('done').upper() != "FALSE":
            return abort(400,
                         {"error": "done should be either 'True' or 'False'"})
        if request.form.get('done').upper() == "TRUE":
            update_bucket_item.done = True
        elif request.form.get('done').upper() == "FALSE":
            update_bucket_item.done = False
    update_bucket_item.save()
    return jsonify({"success": "Changes saved to item",
                    "name": update_bucket_item.name,
                    "description": update_bucket_item.description,
                    "done": update_bucket_item.done
                    }), 200


@app.route('/bucketlists/<id>/items/<item_id>', methods=['DELETE'])
@auth.login_required
def delete_bucketlist_item():
    id = request.form.get('id')
    item_id = request.form.get('item_id')
    delete_db_item = BucketListItem.query.filter_by(
        id=item_id, bucketlist_id=id).scalar()
    if delete_db_item is None:
        return jsonify({"error": "That bucketlist doesn't exist"}), 404
    db.session.delete(delete_db_item)
    db.session.commit()
    return "Successfully deleted bucketlist item", 200
