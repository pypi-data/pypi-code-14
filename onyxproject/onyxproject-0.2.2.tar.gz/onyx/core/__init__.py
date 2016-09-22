#!/usr/bin/env python
# encoding: utf-8
__version__ = '0.1.4'
import os
import os.path
from os.path import exists
import sys
import site
import platform
reload(sys)
sys.setdefaultencoding('utf-8')

import onyx
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager , login_user , login_required
from flask import flash , request , render_template , url_for , redirect
from flask_mail import Mail, Message


template_folder = os.path.dirname(os.path.dirname(__file__)) + '/templates'
static_folder = os.path.dirname(os.path.dirname(__file__)) + '/static'


core = Flask('app', template_folder=template_folder , static_folder=static_folder)
core.config.from_object('onyx.bddconfig')
db = SQLAlchemy(core)

     
if exists(str(onyx.__path__[0]) + "/core/config/mail.py") == True:
	from onyx.core.config import mail
else:
	print('notexist')



mail = Mail(core)

core.config['SECRET_KEY'] = 'onyx'
core.config['SECURITY_PASSWORD_SALT'] = 'onyx2'

from models import *

if exists(str(onyx.__path__[0]) + "/core/install") == True:
	print "Installation en cour :"
	if platform.system() == "Linux":
		os.system("sudo apt-get install moc mplayer python-dev")
		try:
			from migrate.versioning import api
			from onyx.bddconfig import SQLALCHEMY_DATABASE_URI
			from onyx.bddconfig import SQLALCHEMY_MIGRATE_REPO
			from onyx.core import db
			import os.path
			db.create_all()
			if not os.path.exists(SQLALCHEMY_MIGRATE_REPO):
			    api.create(SQLALCHEMY_MIGRATE_REPO, 'database repository')
			    api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
			else:
			    api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO,
			                        api.version(SQLALCHEMY_MIGRATE_REPO))
			print "Base de donnée initialisée"
		except:
			print "Base de donnée déjà initialisée"
	else:
		try:
			from migrate.versioning import api
			from onyx.bddconfig import SQLALCHEMY_DATABASE_URI
			from onyx.bddconfig import SQLALCHEMY_MIGRATE_REPO
			from onyx.core import db
			import os.path
			db.create_all()
			if not os.path.exists(SQLALCHEMY_MIGRATE_REPO):
			    api.create(SQLALCHEMY_MIGRATE_REPO, 'database repository')
			    api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
			else:
			    api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO,
			                        api.version(SQLALCHEMY_MIGRATE_REPO))
			print "Base de donnée initialisée"
		except:
			print "Base de donnée déjà initialisée"
	from install import *
else:
	from controllers import *





