#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import render_template, request , redirect , url_for
from flask.ext.login import login_required
from onyx.core import core
import os

@core.route('/translate')
@login_required
def translate():
	return render_template('translate/index.html')
