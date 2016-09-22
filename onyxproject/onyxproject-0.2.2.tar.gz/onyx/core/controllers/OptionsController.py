#!/usr/bin/env python
# -*- coding: utf-8 -*-
from onyx.core import core
from onyx.core import db
from flask import render_template , redirect , url_for , flash
from flask.ext.login import login_required
import pip
import platform
import os

@core.route('/options')
@login_required
def options():
    return render_template('options/index.html')

@core.route('/maj')
@login_required
def maj():
	pip.main(['install', '--upgrade', "onyxproject"])
	if platform.system() == "Linux":
		os.system("sudo pip install -U pip onyxproject")
		import imp
		from migrate.versioning import api
		from onyx.core import db
		from onyx.bddconfig import SQLALCHEMY_DATABASE_URI
		from onyx.bddconfig import SQLALCHEMY_MIGRATE_REPO
		v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
		migration = SQLALCHEMY_MIGRATE_REPO + ('/versions/%03d_migration.py' % (v+1))
		tmp_module = imp.new_module('old_model')
		old_model = api.create_model(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
		exec(old_model, tmp_module.__dict__)
		script = api.make_update_script_for_model(SQLALCHEMY_DATABASE_URI,
		                                          SQLALCHEMY_MIGRATE_REPO,
		                                          tmp_module.meta, db.metadata)
		open(migration, "wt").write(script)
		api.upgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
		v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
		print('New migration saved as ' + migration)
		print('Current database version: ' + str(v))
	else:
		import imp
		from migrate.versioning import api
		from onyx.core import db
		from onyx.bddconfig import SQLALCHEMY_DATABASE_URI
		from onyx.bddconfig import SQLALCHEMY_MIGRATE_REPO
		v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
		migration = SQLALCHEMY_MIGRATE_REPO + ('/versions/%03d_migration.py' % (v+1))
		tmp_module = imp.new_module('old_model')
		old_model = api.create_model(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
		exec(old_model, tmp_module.__dict__)
		script = api.make_update_script_for_model(SQLALCHEMY_DATABASE_URI,
		                                          SQLALCHEMY_MIGRATE_REPO,
		                                          tmp_module.meta, db.metadata)
		open(migration, "wt").write(script)
		api.upgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
		v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
		print('New migration saved as ' + migration)
		print('Current database version: ' + str(v))
	flash("Onyx vient d'etre mis a jour !",'success')
	return redirect(url_for('options'))