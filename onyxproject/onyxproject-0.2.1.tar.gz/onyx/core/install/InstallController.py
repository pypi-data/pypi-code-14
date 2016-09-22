# -*- coding: utf-8 -*-
from onyx.core import core
from flask import render_template , request , redirect , url_for , flash
from onyx.core.models import *
from onyx.core import db
import os
import site
import hashlib
import onyx
import datetime



@core.route('/install' , methods=['GET','POST'])
def install():
	if request.method == 'GET':
		return render_template('install/index.html')
	user = UsersModel.User(admin=1 , username=request.form['username'] , password=hashlib.sha1(request.form['password']).hexdigest(), email=request.form['email'] , confirmed=True,
        confirmed_on=datetime.datetime.now(),registered_on=datetime.datetime.now() )
	db.session.add(user)
	db.session.commit()
	os.rename(str(onyx.__path__[0]) + "/core/install" , str(onyx.__path__[0]) + "/core/installOld")
	from onyx.core.controllers import *
	flash('Onyx a bien été installé !' , 'success')
	return redirect(url_for("hello"))

@core.errorhandler(401)
@core.errorhandler(404)
@core.errorhandler(500)
def errorInstall(error):
	return render_template('404Install.html', error=error.code)
