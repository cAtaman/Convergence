import os
import secrets
import connexion
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt

base_dir = os.path.dirname(__file__)
notes_db_path = os.path.join(base_dir, 'notes', 'database')

# todo: call db creation scripts from here (migration?)
#       run setup {files?} of each individual app from here

sqlalchemy_binds = {'notes': 'sqlite:///' + os.path.join(notes_db_path, 'notes.db')}  # add other db to this dictionary

connex_app = connexion.App(__name__, specification_dir=base_dir)
app = connex_app.app

app.config['SECRET_KEY'] = secrets.token_hex(16)
app.config['SQLALCHEMY_BINDS'] = sqlalchemy_binds
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)
ma = Marshmallow(app)
bcrypt = Bcrypt(app)
tokens = {}
