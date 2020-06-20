import os.path
import secrets
import connexion
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt

base_dir = os.path.abspath(os.path.dirname(__file__))
notes_db_path = os.path.join(base_dir, 'notes', 'db')
payments_db_path = os.path.join(base_dir, 'payments', 'db')

# todo: call db creation scripts from here (migration?)
#       run setup {files?} of each individual app from here

sqlalchemy_binds = {
                        'notes': 'sqlite:///' + os.path.join(notes_db_path, 'notes.db'),
                        'payments': 'sqlite:///' + os.path.join(payments_db_path, 'payments.db'),
                    }

connex_app = connexion.App(__name__, specification_dir=base_dir)
app = connex_app.app

app.config['SECRET_KEY'] = secrets.token_hex(16)
app.config['SQLALCHEMY_BINDS'] = sqlalchemy_binds
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

db = SQLAlchemy(app)
ma = Marshmallow(app)
bcrypt = Bcrypt(app)
tokens = {}
