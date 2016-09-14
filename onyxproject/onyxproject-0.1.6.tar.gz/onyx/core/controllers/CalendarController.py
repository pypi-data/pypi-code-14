#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import render_template, request , redirect , url_for , jsonify
from flask.ext.login import login_required , current_user
from onyx.core import core
from onyx.core.models import *
from onyx.core import db
import os
import json
import string



@core.route('/calendar')
@login_required
def calendar():
	return render_template('calendar/view.html')

@core.route('/calendar/set' , methods=['GET','POST'])
@login_required
def setCalendar():
	if request.method == 'GET':
		events = []
		bdd = CalendarModel.Calendar.query.filter(CalendarModel.Calendar.idAccount.endswith(str(current_user.username)))

		for fetch in bdd:	
			e = {}
			e['id'] = fetch.id
			e['title'] = fetch.title
			e['start'] = fetch.start
			e['end'] = fetch.end
			e['color'] = fetch.color
			events.append(e)
		return render_template('calendar/index.html' , events=events)
	update = CalendarModel.Calendar.query.filter_by(id=request.form['id'],idAccount=str(current_user.username)).first()
	update.start = request.form['start']
	update.end = request.form['end']
	db.session.add(update)
	db.session.commit()
	return json.dumps({'status':'success'})

@core.route('/calendar/set/add' , methods=['GET','POST'])
@login_required
def addCalendar():
	if request.method == 'POST':
		color = request.form['color']
		enddate = request.form['end']
		startdate = request.form['start']
		title = request.form['title']
		calendar = CalendarModel.Calendar(idAccount=str(current_user.username),title=title , start=startdate, end=enddate ,color=color)
		db.session.add(calendar)
		db.session.commit()
		return redirect(url_for('setCalendar'))

@core.route('/calendar/set/editTitle' , methods=['GET','POST'])
@login_required
def editEventTitle():
	if request.method == 'POST':
		checked = 'delete' in request.form
		if checked == True:
			delete = CalendarModel.Calendar.query.filter_by(id=request.form['id'],idAccount=str(current_user.username)).first()
			db.session.delete(delete)
			db.session.commit()
			return redirect(url_for('setCalendar'))
		update = CalendarModel.Calendar.query.filter_by(id=request.form['id'],idAccount=str(current_user.username)).first()
		update.title = request.form['title']
		update.color = request.form['color']
		db.session.add(update)
		db.session.commit()
		return redirect(url_for('setCalendar'))

@core.context_processor
def utility_processor():
    def split(str):
        return string.split(str, " ")
    return dict(split=split)