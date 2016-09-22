#!/usr/bin/env python
# -*- coding: utf-8 -*-
from onyx.core import core
from flask import render_template, request
from flask.ext.login import login_required , current_user


@core.route('/widget' , methods=['GET' , 'POST'])
@login_required
def widget():
	if request.method == 'GET':
		return render_template('widget.html')