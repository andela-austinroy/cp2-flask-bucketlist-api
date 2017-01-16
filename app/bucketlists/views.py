from flask import Blueprint, request, jsonify, abort
from flask import url_for
from flask_httpauth import HTTPTokenAuth
from itsdangerous import BadTimeSignature, BadSignature

from app import token_signer, db, app
from app.auth.models import User
from app.bucketlists.models import BucketList, BucketListItem


bucketlists = Blueprint('bucketlists', __name__, url_prefix='/bucketlists')


# @app.route('/bucketlists/', methods=['POST'])
# def create_new_bucketlist():
#     pass


# @app.route('/bucketlists/', methods=['GET'])
# def fetch_all_bucketlists():
#     pass


# @app.route('/bucketlists/<id>', methods=['GET'])
# def fetch_single_bucketlist():
#     pass


# @app.route('/bucketlists/<id>', methods=['PUT'])
# def update_bucketlist():
#     pass


# @app.route('/bucketlists/<id>', methods=['DELETE'])
# def delete_bucketlist():
#     pass


# @app.route('/bucketlists/<id>/items/', methods=['POST'])
# def add_bucketlist_item():
#     pass


# @app.route('/bucketlists/<id>/items/<item_id>', methods=['PUT'])
# def update_bucketlist_item():
#     pass


# @app.route('/bucketlists/<id>/items/<item_id>', methods=['DELETE'])
# def delete_bucketlist_item():
#     pass
