#!/usr/bin/env python
# -*- coding: utf-8 -*-
from onyx.core import core
from flask import render_template , request
from flask.ext.login import login_required
import wikipedia



@core.route('/wiki', methods=['GET', 'POST'])
@login_required
def wiki():
    if request.method == 'GET':
    	return render_template('wiki/index.html')
    wikipedia.set_lang("fr")
    article = wikipedia.page(request.form['search'])
    return render_template('wiki/result.html', head = article.title , url = article.url , summary=wikipedia.summary(request.form['search']))