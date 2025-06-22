"""
the simplest possible hello world app
"""

VERSION = "00"

from flask import Flask
from flask import request
from flask import render_template, redirect
import requests
import json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from flask_socketio import SocketIO

## usual Flask initilization
app = Flask(__name__)

## DB declaration

# filename where to store stuff (sqlite is file-based)
db_name = 'notes.db'
# how do we connect to the database ?
# here we say it's by looking in a file named chat.db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_name
# this variable, db, will be used for all SQLAlchemy commands
db = SQLAlchemy(app)

socketio = SocketIO(app)

## define a table in the database

class Note(db.Model):
    __tablename__ = 'notes'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    content = db.Column(db.String)
    done = db.Column(db.Boolean)


# actually create the database (i.e. tables etc)
with app.app_context():
    db.create_all()

@app.route('/')
def hello_world():
    return redirect('/front/notes')

# try it with
"""
http :5001/api/version
"""
@app.route('/api/version')
def version():
    return {'version' : VERSION}

# try it with
"""
http :5001/api/notes title="devoirs" content="faire le devoir d'info"
http :5001/api/notes title="dentiste" content="mercredi 14h" done:=True
"""
@app.route('/api/notes', methods=['POST'])
def create_note():
    try:
        parameters = json.loads(request.data)
        title = parameters['title']
        content = parameters['content']
        if 'done' in parameters.keys() :
            done = parameters['done']
        else :
            done = False
        print("received request to create note", title, content, done)
        # temporary
        new_note = Note(title = title, content = content, done = done)
        db.session.add(new_note)
        db.session.commit()
        return parameters
    except Exception as exc:
        return dict(error=f"{type(exc)}: {exc}"), 422

@app.route('/api/notes', methods=['GET'])
def list_users():
    notes = Note.query.all()
    return [{'id' : note.id, 'title' : note.title, 'content' : note.content, 'done' : note.done} for note in notes]

@app.route('/api/notes/<int:id>/done', methods = ['POST'])
def done(id):
    notes = Note.query.all()
    i = 0
    for note in notes :
        if note.id == id :
            note.done = 1 - note.done
            db.session.commit()
            socketio.emit('done_change', {'id': note.id, 'done': note.done})
            break
        else :
            i += 1
    if i == len(notes) :
        return dict(error = f"Incorrect id")

"""
http://localhost:5001/front/notes
"""

@app.route('/front/notes')
def front_notes():
    # first option of course, is to get all notes from DB
    # notes = Note.query.all()
    # but in a more fragmented architecture we would need to
    # get that info at another endpoint
    # here we ask ourselves on the /api/notes route
    url = request.url_root + '/api/notes'
    req = requests.get(url)
    if not (200 <= req.status_code < 300):
        # return render_template('errors.html', error='...')
        return dict(error = f"could not request notes list", url = url, status = req.status_code, text = req.text)
    notes = req.json()
    return render_template('notes.html.j2', notes = notes, version = VERSION)

if __name__ == '__main__':
    app.run()