#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import render_template, request , redirect , url_for
from flask.ext.login import login_required
from onyx.core import core
import os

@core.route('/info')
@login_required
def info():
    return render_template('info.html')