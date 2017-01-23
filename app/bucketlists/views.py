from flask import Blueprint, request, jsonify, abort
from flask import url_for
from flask_httpauth import HTTPTokenAuth
from itsdangerous import BadTimeSignature, BadSignature

from app import token_signer, db, app
from app.auth.models import User
from app.bucketlists.models import BucketList, BucketListItem


bucketlists = Blueprint('bucketlists', __name__, url_prefix='/bucketlists')

buckets = []


@app.route('/')
def home():
    return "Welcome to my bucketlist api"


@app.route('/bucketlists/', methods=['POST'])
def create_new_bucketlist():
    """Adds a new bucketlist"""
    name = request.form.get('name')
    new_bucketlist = BucketList(name, 1)
    new_bucketlist.save()
    new_bucketlist.refresh_from_db()
    return jsonify({'Successfully added bucketlist':
                    {'id': new_bucketlist.id,
                     'name': new_bucketlist.name,
                     'date_created': new_bucketlist.date_created,
                     'date_modified': new_bucketlist.date_modified
                     }
                    }), 201


@app.route('/bucketlists/', methods=['GET'])
def fetch_all_bucketlists():
    """Returns all bucketlists"""
    bucketlists = BucketList.query.all()
    for bucketlist in bucketlists:
        items = BucketListItem.query.filter_by(
            bucketlist_id=bucketlist.id).first()
        if items is None:
            items = []
        else:
            items = items.name
        buckets.append({'id': bucketlist.id,
                        'name': bucketlist.name,
                        'items': items,
                        'date_created': bucketlist.date_created,
                        'date_modified': bucketlist.date_modified
                        })
    if not len(buckets):
        return jsonify({"error": "No bucketlists added"}), 404
    return jsonify({'bucketlists': buckets}), 200


@app.route('/bucketlists/?q=Check', methods=['GET'])
def search_bucketlist_by_name():
    pass


@app.route('/bucketlists/<id>', methods=['GET'])
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
def update_bucketlist(id):
    """Updates a bucketlist's details"""
    id = request.form.get('id')
    update_bucket = BucketList.query.filter_by(
        id=id).scalar()
    if not update_bucket:
        return jsonify({"error": "Bucketlist not found"}), 404
    update_bucket.name = request.form.get('name', update_bucket.name)
    bucketlists = BucketList.query.all()
    for bucket in bucketlists:
        if bucket.name == update_bucket.name:
            return jsonify({
                "error": "That bucketlist name has already been used"
            }), 403
    db.session.save()
    return jsonify({"success": "Changes saved to bucketlist"}), 200


@app.route('/bucketlists/<id>', methods=['DELETE'])
def delete_bucketlist(id):
    delete_db = BucketList.query.filter_by(id=id).scalar()
    if delete_db is None:
        return jsonify({"error": "That bucketlist doesn't exist"}), 404
    db.session.delete(delete_db)
    db.session.commit()
    return "Successfully deleted bucketlist", 200


@app.route('/bucketlists/<id>/items/', methods=['POST'])
def add_bucketlist_item(id):
    """Adds an item to an existing bucketlist"""
    bucketlist_id = request.form.get(['id'])
    name = request.form.get(['name'])
    description = request.form.get('description')
    new_bucketlistitem = BucketListItem(name, description, bucketlist_id)
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
def update_bucketlist_item(id, item_id):
    id = request.form.get('id')
    item_id = request.form.get('item_id')
    update_bucket_item = BucketListItem.query.filter_by(
        id=item_id, bucketlist_id=id).scalar()
    if request.form.get('name') is not None:
        update_bucket_item.name = request.form.get('name')
    if request.form.get('description') is not None:
        update_bucket_item.description = request.form.get(
            'description', update_bucket_item.description)
    if request.form.get('done').upper != "TRUE" or "FALSE":
        return ({"error": "done should be either 'True' or 'False'"}), 403
    update_bucket_item.done = request.form.get('done', update_bucket_item.done)
    db.session.save()
    return jsonify({"success": "Changes saved to item"}), 200


@app.route('/bucketlists/<id>/items/<item_id>', methods=['DELETE'])
def delete_bucketlist_item():
    id = request.form.get('id')
    item_id = request.form.get('item_id')
    delete_db_item = BucketListItem.query.filter_by(
        id=item_id, bucketlist_id=id).scalar()
    if delete_db_item is None:
        return jsonify({"error": "That bucketlist doesn't exist"}), 404
    db.session.delete(delete_db_item)
    db.session.commit()
    return "Successfully deleted bucketlist item",200
