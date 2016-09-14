#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import platform
from onyx.core import core
from onyx.core.assets import getAvatar
from flask import render_template, request , jsonify
from flask.ext.login import login_required , current_user



@core.route('/')
@login_required
def index():	
    return render_template('index.html')


@core.context_processor
def Avatar():
    urlAvatar = getAvatar.getAvatar()
    return dict(urlAvatar=urlAvatar)


@core.context_processor
def ButtonColor():
	try:
		buttonColor = current_user.buttonColor
	except:
		buttonColor = ""
	return dict(buttonColor=buttonColor)

@core.context_processor
def currentUser():
	try:
		currentUser = current_user.username
	except:
		currentUser = "User"
	return dict(currentUser=currentUser)

@core.context_processor
def currentEmail():
	try:
		currentEmail = current_user.email
	except:
		currentEmail = "Email"
	return dict(currentEmail=currentEmail)

@core.context_processor
def currentID():
	try:
		currentID = current_user.id
	except:
		currentID = "ID"
	return dict(currentID=currentID)

@core.context_processor
def getOS():
	getOS = platform.system()
	return dict(getOS=getOS)

