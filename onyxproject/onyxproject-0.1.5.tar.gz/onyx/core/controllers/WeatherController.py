#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import render_template, request , redirect , url_for
from flask.ext.login import login_required
from onyx.core.assets import getMeteo
from onyx.core import core
import os

@core.route('/weather')
@login_required
def weather():
    return render_template('weather.html', day=getMeteo.getDay(), city=getMeteo.getCity() , imgurl=getMeteo.getImg() , lat=getMeteo.getLat(), lon=getMeteo.getLon())
