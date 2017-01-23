import os

SECRET_KEY = 'vhnvgcgxfzgyjcfdhtdcxz5w6e43rthr53x5twt'

DEBUG = True

basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + \
    os.path.join(basedir, 'bucketlist.sqlite')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = True
DATABASE_CONNECT_OPTIONS = {}
THREADS_PER_PAGE = 3
