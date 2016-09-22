#!/usr/bin/env python
# -*- coding: utf-8 -*-
from onyx.core import core
from flask import render_template, request
from flask.ext.login import login_required


@core.route('/rasp')
@login_required
def rasp():
	return render_template('rasp.html')
