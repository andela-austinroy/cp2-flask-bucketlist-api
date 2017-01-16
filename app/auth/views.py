from flask import Blueprint, jsonify, abort, request

from app import app
# from app.mod_auth.models import User

auth = Blueprint('auth', __name__, url_prefix='/auth')

# @app.route('/auth/login', methods=['POST'])
# def login():
#     pass


# @app.route('/auth/register', methods=['POST'])
# def register():
#     pass
