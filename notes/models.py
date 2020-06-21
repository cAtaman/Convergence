from setup import db, ma


# Asset class
class Product(db.Model):
    __bind_key__ = 'notes'
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True)


# Notes -- new functionality
class Note(db.Model):
    __bind_key__ = 'notes'
    __tablename__ = 'note'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.String)
    user = db.Column(db.String(100))
    content = db.Column(db.String)


# Product Schema
class ProductSchema(ma.ModelSchema):
    class Meta:
        model = Product
        sqla_session = db.session


# Notes Schema
class NoteSchema(ma.ModelSchema):
    class Meta:
        model = Note
        sqla_session = db.session
