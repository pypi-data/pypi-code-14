# -*- coding: utf-8 -*-
import os
from datetime import datetime
from elasticsearch import Elasticsearch
from flask import Flask, jsonify, render_template, request

__dir__ = os.path.dirname(os.path.realpath(__file__))

app = Flask(__name__, template_folder=__dir__ + '/templates')
app.config['STATIC_FOLDER'] = __dir__ + '/static'

es = Elasticsearch()

@app.route('/')
def index():
    user = {'nickname': 'Miguel'}  # fake user
    return render_template(
       'index.html',
       title ='Home',
       user = user
   )

@app.route('/search')
def hello_world():
    q = request.args.get('q', '')
    index = request.args.get('index', '')
    count = request.args.get('count', 10)
    page  = request.args.get('page', 0)

    try:
        res = es.search(
            index = index,
            q     = q,
            size  = count,
            from_ = page,
        )
    except Exception as e:
        return jsonify(e.info), 500

    return jsonify(res)
