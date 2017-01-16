from flask import Flask, jsonify
from flask_restful import reqparse, abort, Api, Resource
from flask.ext.httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()
app = Flask(__name__)
api = Api(app)

@app.route('/')
def index():
	return "Homepage"


@app.route('/auth/login', methods=['POST'])
def login():
    pass


@app.route('/auth/register', methods=['POST'])
def register():
    pass


@app.route('/bucketlists/', methods=['POST'])
def create_new_bucketlist():
    pass


@app.route('/bucketlists/', methods=['GET'])
def fetch_all_bucketlists():
    pass


@app.route('/bucketlists/<id>', methods=['GET'])
def fetch_single_bucketlist():
    pass


@app.route('/bucketlists/<id>', methods=['PUT'])
def update_bucketlist():
    pass


@app.route('/bucketlists/<id>', methods=['DELETE'])
def delete_bucketlist():
    pass


@app.route('/bucketlists/<id>/items/', methods=['POST'])
def add_bucketlist_item():
    pass


@app.route('/bucketlists/<id>/items/<item_id>', methods=['PUT'])
def update_bucketlist_item():
    pass


@app.route('/bucketlists/<id>/items/<item_id>', methods=['DELETE'])
def delete_bucketlist_item():
    pass