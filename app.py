import os
from flask import Flask, request, redirect, render_template
from s3 import upload_file, list_files

app = Flask(__name__)

UPLOAD_DIR = "uploads"
BUCKET = 's3-bucket-name-here'


@app.route('/')
def hello_world():
    return '<h1>Hello, World!</h1>'


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
