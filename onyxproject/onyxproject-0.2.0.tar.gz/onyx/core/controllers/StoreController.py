#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import render_template, request , redirect , url_for
from flask.ext.login import login_required
from onyx.core import core



@core.route('/store')
@login_required
def store():
    return render_template('store/index.html')