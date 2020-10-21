import os
import time
import json
import requests
from itertools import groupby
from flask import request, jsonify, render_template
from setup import db, app
from setup import base_dir
from notes.models import NoteSchema, Note


# init schema
note_schema = NoteSchema()
notes_schema = NoteSchema(many=True)


def format_time(obj):
    if 'datetime' in obj and obj['datetime']:
        obj['datetime'] = time.strftime("%a, %d-%b-%Y %H:%M:%S", time.localtime(float(obj['datetime'])))
    # return object


html = '''<html>
    <head>
        <meta name="google-site-verification" content="wfvx2mVydsdqozFPfnvLvSzUCmslCdUCu7zs7ws0vls" />
        <title> {title} </title>
    </head>

    <body style="background-color:grey;color:black">
        {paragraphs_with_tags}
    </body >
</html >'''
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

    title = 'AtamanBC - The one true timeline'
    message = '</br>' \
              '<p>Hello World! Greetings from Ataman</p>' \
              '<p>==============================================================' \
              '</br>==============================================================</p>' \
              '</br>' \
              '<h2>_______STATUS_______</h2>' \
              '</br>' \
              '<p>** Products app is still as is with unique products</p>' \
              f'<p>** Notes service currently has {count} notes from {len(notes)} unique users</p>' \
              '</br>' \
              '<h2>_______NOTES Users_______</h2>' \
              f'<p>{users}</p>' \
              '</br>' \
              '</br>' \
              '<h3> Go to... </h3>' \
              '<a href="/"> List of Notes (Restricted)</a>' \
              '</br>' \
              '<a href="/payments/v1/ui"> Payments API </a>'

    return html.format(title=title, paragraphs_with_tags=message)


# Get all notes
def get_notes(id=None, ret_json=False):
    if id:
        all_notes = [Note.query.filter_by(id=id).first(), ]
    else:
        all_notes = Note.query.all()
    results = notes_schema.dump(all_notes)
    [format_time(result) for result in results]
    if ret_json:
        return results

    form = '<p>Note {:3} ({}): {}</p>'
    dvcs = {'android_chrome': 'Redmi', 'windows_chrome': 'Envy', 'python-requests': 'Red Py', 'linux_firefox': 'Linux-fx', 'linux_chrome': 'Linux'}
    ret = ''
    for e in results:
        if e['user'] in dvcs:
            ret += form.format(e['id'], dvcs[e['user']], e['content'])
        else:
            ret += form.format(e['id'], e['user'], e['content'])
    return html.format(title='Notes', paragraphs_with_tags=ret)


# Add notes
def add_note(content):
    if request.user_agent.platform and request.user_agent.browser:
        user = request.user_agent.platform + '_' + request.user_agent.browser
    else:
        user = request.user_agent.string
        user = user.split('/')[0]
    note = {'user': user, 'content': content, 'datetime': str(time.time())}
    note = note_schema.load(note)
    db.session.add(note)
    db.session.commit()
    return 'Note added successfully', 200


@app.route('/migrate', methods=['GET'])
def migrate_db():
    db.create_all()
    schema = NoteSchema()
    session = schema.Meta.sqla_session

    csv_path = os.path.join(base_dir, 'notes', 'db', 'note.csv')
    notes_csv = open(csv_path, 'r').readlines()[2:]

    try:
        for note in notes_csv:
            items = note.strip().split(',')
            print(items)
            note_o = schema.load({'datetime': items[1], 'user': items[2], 'content': items[3]})
            session.add(note_o)
        session.commit()
    except Exception as e:
        print(e)
        return 'Something went wrong', 400

    return 'migration successful', 200


# Delete note
@app.route('/notes/delete', methods=['GET'])
def delete_note():
    id_to_delete = request.args['id']
    note = Note.query.filter_by(id=id_to_delete).first()
    db.session.delete(note)
    db.session.commit()
    return 'Note deleted successfully', 200


@app.route('/hng_team_neon', methods=['GET'])
def get_team_form():
    return render_template('hng.html')


@app.route('/hng_team_neon.json', methods=['GET'])
def get_json():
    with open(os.path.join(base_dir, 'team_neon.json'), 'r') as file:
        neon = file.readlines()
        members = []
        for member in neon:
            members.append(json.loads(member))
    return jsonify(members)


@app.route('/hng_team_neon', methods=['POST'])
def add_member():
    data = request.form
    with open(os.path.join(base_dir, 'team_neon.json'), 'a') as file:
        file.write(json.dumps(data) + "\n")
    return 'Record successfully added', 200


# Get all products
@app.route('/req', methods=['GET'])
def greq():
    url = request.args['url']
    req = requests.get(url)
    return req.content


# Get headers
@app.route('/head', methods=['GET'])
def get_headers():
    return jsonify(dict(request.headers))
