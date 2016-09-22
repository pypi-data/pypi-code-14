#!/usr/bin/env python
# -*- coding: utf-8 -*-
from onyx.core import core
from flask import render_template
from flask.ext.login import login_required


@core.route('/map')
def map():
	return render_template('map/index.html')