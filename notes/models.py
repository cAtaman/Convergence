
import os
from setup import db, ma

environment = os.environ['FLASK_ENV']


# Notes
class Note(db.Model):
    __tablename__ = 'note'
    __table_args__ = {'extend_existing': True}
    if environment != 'production':
        __bind_key__ = 'notes'
    id = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.String)
    user = db.Column(db.String(100))
    content = db.Column(db.String)


# Notes Schema
class NoteSchema(ma.ModelSchema):
    class Meta:
        model = Note
        sqla_session = db.session
db.create_all()
