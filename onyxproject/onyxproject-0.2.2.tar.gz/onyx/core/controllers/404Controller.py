#!/usr/bin/env python
# -*- coding: utf-8 -*-
from onyx.core import core
from flask import render_template, request
from flask.ext.login import login_required


@core.errorhandler(401)
@core.errorhandler(404)
@core.errorhandler(500)
def erreur(error):
	return render_template('404.html', error=error.code)
