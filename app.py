import os
from flask import Flask, request, redirect, render_template
from s3 import upload_file, list_files
from flask_sqlalchemy import SQLAlchemy
import sqlite3
from datetime import datetime

app = Flask(__name__)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/daltonsaffe/devel/art-camp-combinations/db/art.sqlite'

db = SQLAlchemy(app)

class Art(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(120), unique=True, nullable=False)
    title = db.Column(db.String(120), unique=True, nullable=False)
    artist = db.Column(db.String(120), unique=False, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now)


UPLOAD_DIR = "uploads"
BUCKET = 's3-bucket-name-here'


@app.route('/')
def hello_world():
    return '<h1>Hello, World!</h1>'

@app.route('/<url>/<title>/<artist>')
def index(url, title, artist):
    art = Art(url=url, title=title, artist=artist)
    db.session.add(art)
    db.session.commit()

    return '<h1>Added new art piece</h1>'

@app.route('/<title>')
def get_art(title):
    art = Art.query.filter_by(title=title).first()

    return f'<h1>The art happens { art.artist }</h1>'

@app.route('/upload', methods=['POST'])
def upload():
    if request.method == "POST":
        f = request.files['file']
        f.save(os.path.join(UPLOAD_DIR, f.filename))
        upload_file(f"uploads/{f.filename}", BUCKET)

        return "<h1>Sweet, you uploaded the file!</h1>"


@app.route('/drive')
def list_drive():
    contents = list_files(BUCKET)
    return render_template('drive.html', contents=contents)


if __name__ == '__main__':
    app.run(debug=True)
