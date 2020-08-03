import os.path
import secrets
import connexion
import jinja2
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt

base_dir = os.path.abspath(os.path.dirname(__file__))

# todo: call db creation scripts from here (migration?)
#       run setup {files?} of each individual app from here

connex_app = connexion.App(__name__, specification_dir=base_dir)
app = connex_app.app

if os.environ['FLASK_ENV'] == 'production':
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['AMAZON_RDS_DB_URL']
else:
    notes_db_path = os.path.join(base_dir, 'notes', 'db')
    payments_db_path = os.path.join(base_dir, 'payments', 'db')
    sqlalchemy_binds = {
        'notes': 'sqlite:///' + os.path.join(notes_db_path, 'notes.db'),
        'payments': 'sqlite:///' + os.path.join(payments_db_path, 'payments.db'),
    }
    app.config['SQLALCHEMY_BINDS'] = sqlalchemy_binds

app.config['SECRET_KEY'] = secrets.token_hex(16)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

# set up custom template loader
my_loader = jinja2.ChoiceLoader([
        app.jinja_loader,
        jinja2.FileSystemLoader([os.path.join(base_dir, 'notes', 'templates'),
                                 os.path.join(base_dir, 'payments', 'templates')]),
        ])
app.jinja_loader = my_loader

# initialize objects
db = SQLAlchemy(app)
ma = Marshmallow(app)
bcrypt = Bcrypt(app)
tokens = {}
