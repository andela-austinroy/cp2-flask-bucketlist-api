import os
from os.path import join, dirname
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

SECRET_KEY = os.environ.get("SECRET_KEY")

DEBUG = True

basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + \
    os.path.join(basedir, 'bucketlist.sqlite')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = True
DATABASE_CONNECT_OPTIONS = {}
THREADS_PER_PAGE = 3
