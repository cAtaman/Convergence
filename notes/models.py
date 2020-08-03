from setup import db, ma


# Notes
class Note(db.Model):
    __tablename__ = 'note'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.String)
    user = db.Column(db.String(100))
    content = db.Column(db.String)


# Notes Schema
class NoteSchema(ma.ModelSchema):
    class Meta:
        model = Note
        sqla_session = db.session
