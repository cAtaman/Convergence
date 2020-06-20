from collections import defaultdict
from setup import db, ma


# Asset class
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True)

    def __init__(self, name):
        self.name = name


# Notes -- new functionality
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.String)
    user = db.Column(db.String(100))
    content = db.Column(db.String)
    count = defaultdict(int)

    def __init__(self, user, date_time, content):
        self.user = user
        self.datetime = date_time
        self.content = content

    @classmethod
    def get_count(cls):
        return cls.count


# Product Schema
class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name')


# Notes Schema
class NoteSchema(ma.Schema):
    class Meta:
        fields = ('id', 'datetime', 'user', 'content')
