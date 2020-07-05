import os
import time
import json
from collections import defaultdict
from itertools import groupby
from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import requests

# Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))


# ===============================================================
# ======================  Database  =============================
# ===============================================================
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db', 'notes.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

# Init Database
# global db
db = SQLAlchemy(app)

# Init marshmallow
ma = Marshmallow(app)


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


# init schema
product_schema = ProductSchema()
note_schema = NoteSchema()
products_schema = ProductSchema(many=True)
notes_schema = NoteSchema(many=True)


# ===============================================================
# ========================  Utils  ==============================
# ===============================================================
def format_time(obj):
    obj['datetime'] = time.strftime("%a, %d-%b-%Y %H:%M:%S", time.localtime(float(obj['datetime'])))
    # return object


# ===============================================================
# ======================  Endpoints  ============================
# ===============================================================
@app.route('/')
def hello_world():
    notes = notes_schema.dump(Note.query.all())
    notes = {k: list(g) for k, g in groupby(notes, key=lambda x: x['user'])}
    users = ['<p> {}: {} </p>'.format(user, len(notes[user])) for user in notes]
    users = ''.join(users)
    count = sum([len(notes[user]) for user in notes])

    html = '''<html>
        <head>
            <title> {title} </title>
        </head>

        <body>
            {paragraphs_with_tags}
        </body >
    </html >'''

    title = 'AtamanBC - The one true timeline'
    message = '</br>'\
              '<p>Hello World! Greetings from Ataman</p>'\
              '<p>=============================================================='\
              '</br>==============================================================</p>'\
              '</br>'\
              '<h2>_______STATUS_______</h2>' \
              '</br>' \
              '<p>** Products app is still as is with unique products</p>'\
              f'<p>** Notes service currently has {count} notes from {len(notes)} unique users</p>' \
              '</br>' \
              '<h2>_______NOTES Users_______</h2>' \
              f'<p>{users}</p>' \
              '</br>' \
              '</br>' \
              '<h3> Go to... </h3>'\
              '<a href="/notes"> List of Notes </a>' \
              '</br>' \
              '<a href="/products"> List of Products </a>'

    return html.format(title=title, paragraphs_with_tags=message)

# Get all notes
@app.route('/notes', methods=['GET'])
def get_notes():
    all_notes = Note.query.all()
    results = notes_schema.dump(all_notes)
    [format_time(result) for result in results]
    return jsonify(results)


# Get one note
@app.route('/notes/get', methods=['GET'])
def get_note():
    id_to_get = request.args['id']
    all_notes = Note.query.filter_by(id=id_to_get).first()
    result = note_schema.dump(all_notes)
    format_time(result)
    return jsonify(result)


# Add notes
@app.route('/notes/add', methods=['GET'])
def add_note():
    if request.user_agent.platform and request.user_agent.browser:
        user = request.user_agent.platform + '_' + request.user_agent.browser
    else:
        user = request.user_agent.string
        user = user.split('/')[0]
    content = request.args['content']
    date_time = time.time()
    new_note = Note(user, date_time, content)

    db.session.add(new_note)
    db.session.commit()
    Note.count[user] += 1
    return 'Note added successfully', 200


# Delete note
@app.route('/notes/delete', methods=['GET'])
def delete_note():
    id_to_delete = request.args['id']
    note = Note.query.filter_by(id=id_to_delete).first()
    db.session.delete(note)
    db.session.commit()

    user = note.user
    return 'Note deleted successfully', 200


# Create  product
@app.route('/product', methods=['POST'])
def add_product():
    name = request.json['name']
    new_product = Product(name)

    db.session.add(new_product)
    db.session.commit()
    return product_schema.jsonify(new_product)


# Get all products
@app.route('/products', methods=['GET'])
def get_products():
    all_products = Product.query.all()
    result = products_schema.dump(all_products)
    return jsonify(result)


@app.route('/hng_team_neon', methods=['GET'])
def get_team_form():
    return render_template("hng.html")


@app.route('/hng_team_neon.json', methods=['GET'])
def get_json():
    with open(os.path.join(basedir, 'team_neon.json'), 'r') as file:
        neon = file.readlines()
        members = []
        for member in neon:
            members.append(json.loads(member))
    return jsonify(members)


@app.route('/hng_team_neon', methods=['POST'])
def add_member():
    data = request.form
    with open(os.path.join(basedir, 'team_neon.json'), 'a') as file:
        file.write(json.dumps(data) + "\n")
    return 'Record successfully added', 200


#####
# Get all products
@app.route('/req', methods=['GET'])
def greq():
    url = request.args['url']
    req = requests.get(url)
    return req.content


# Run server
if __name__ == "__main__":
    app.run(debug=True, port=2099)


