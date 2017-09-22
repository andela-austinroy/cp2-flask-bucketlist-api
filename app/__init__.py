from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from itsdangerous import TimestampSigner, SignatureExpired, BadSignature
import config
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer)
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"*": {"origins": "*"}})

app.config.from_object('config')
db = SQLAlchemy(app)

token_signer = TimestampSigner(config.SECRET_KEY)

from app.auth.views import auth
from app.bucketlists.views import bucketlists

app.register_blueprint(bucketlists)
app.register_blueprint(auth)
