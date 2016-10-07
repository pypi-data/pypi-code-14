#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, abort, request, escape, render_template
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'xml'])
app.config['UPLOAD_FOLDER'] = "/tmp/confopy-webapp-uploads"
app.config['MAX_CONTENT_PATH'] = 20 * 1024 * 1024 # 20 MiB

try:
    os.mkdir(app.config['UPLOAD_FOLDER'])
except OSError, e:
    pass

def is_in_allowed_extensions(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route("/", methods=['GET', 'POST'])
def root():
    buf = []
    buf.append(render_template('evaluate.html'))
    if request.method == 'POST':
        files = request.files
        doc = files['document']#.get('document', None)
        if is_in_allowed_extensions(doc.filename):
            filename = secure_filename(doc.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            doc.save(filepath)
            with open(filepath) as f:
                content = escape(f.read())
                buf.append("<pre>")
                buf.append(content)
                buf.append("</pre>")
    return "\n".join(buf)

@app.route('/error')
def error():
    abort(404)

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404 File Not Found! :(</h1>", 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
