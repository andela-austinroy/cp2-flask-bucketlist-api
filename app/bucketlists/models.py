from app import db
from app.auth.models import User


class BucketList(db.Model):
    __tablename__ = 'Bucketlists'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(125), nullable=False)
    date_created = db.Column(db.DATETIME, default=db.func.current_timestamp())
    date_modified = db.Column(db.DATETIME, default=db.func.current_timestamp(
    ), onupdate=db.func.current_timestamp())
    created_by = db.Column(db.Integer, db.ForeignKey(User.id))
    bucket_items = db.relationship(
        'BucketListItem', backref='bucket', lazy='dynamic')

    def __init__(self, name, created_by):
        self.name = name
        self.created_by = created_by

    def save(self):
        db.session.add(self)
        db.session.commit()

    def refresh_from_db(self):
        return db.session.query(BucketList).filter_by(id=str(self.id))


class BucketListItem(db.Model):
    __tablename__ = 'BucketlistItems'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    date_created = db.Column(db.DATETIME, default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DATETIME, onupdate=db.func.current_timestamp())
    bucketlist_id = db.Column(db.Integer, db.ForeignKey(BucketList.id))
    done = db.Column(db.Boolean)

    def __init__(self, name, description, bucketlist_id, done=False):
        self.name = name
        self.done = done
        self.description = description
        self.bucketlist_id = bucketlist_id

    def save(self):
        db.session.add(self)
        db.session.commit()

    def refresh_from_db(self):
        return db.session.query(BucketListItem).filter_by(id=str(self.id))
