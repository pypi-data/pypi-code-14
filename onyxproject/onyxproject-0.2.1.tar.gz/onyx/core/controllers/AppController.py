#!/usr/bin/env python
# -*- coding: utf-8 -*-
from onyx.core import core
from flask import render_template, request
from flask.ext.login import login_required


@core.route('/app')
@login_required
def app():
	return render_template('app.html')
