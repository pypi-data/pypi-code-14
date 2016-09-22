#!/usr/bin/env python
# -*- coding: utf-8 -*-
import hashlib
from onyx.core import db
from onyx.core.models import *
from flask import session
from flask.ext.login import current_user


def getAvatar():
	try:
		user = UsersModel.User.query.filter_by(id=current_user.id).first()
		email = str(user.email)
		default = "http://www.gravatar.com/avatar"
		size = 60
		url = "http://www.gravatar.com/avatar/" + hashlib.md5(email.lower()).hexdigest() + "?d=" + default + "&s=" +str(size)
		return url
	except:
		url = "http://www.gravatar.com/avatar"
		return url