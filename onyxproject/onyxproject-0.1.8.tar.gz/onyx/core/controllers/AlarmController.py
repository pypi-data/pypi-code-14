#!/usr/bin/env python
# -*- coding: utf-8 -*-
from onyx.core import core , db
from flask.ext.login import login_required
from flask import render_template , redirect , request , url_for , flash
from flask import send_file
from werkzeug import secure_filename
from onyx.core.config import music
from onyx.core.models import *
import os




@core.route('/reveil' , methods=['GET','POST'])
@login_required
def reveil():
    if request.method == 'GET':
    	ring = os.listdir(music.RING_REPO)
        return render_template('alarm/index.html' , ring=ring)
    try:
    	f = request.files['ringfile']
    	if f:
    		nom = secure_filename(f.filename)
    		f.save(music.RING_REPO + nom)
    		flash('Sonnerie ajoutée avec succées !' , 'success')
    		return redirect(url_for('reveil'))
    except:
    	alarms = AlarmModel.Alarm(heure=request.form['time'] , ring=request.form['ring'] , day=str(request.form.getlist('recure')), active=int(request.form['active']))
    	db.session.add(alarms)
    	db.session.commit()
    	flash('Le réveil a bien été ajouté !' , 'success')
    	return redirect(url_for('reveil'))
    

@core.route('/reveil/delete' , methods=['GET','POST'])
@login_required
def reveildel():
	if request.method == 'GET':
		try:
		    bdd = AlarmModel.Alarm.query.all()
		    resultHeureRow = []
		    for alarms in bdd:
		    	resultHeureRow.append(alarms.heure) 
			resultHeure = resultHeureRow


			resultRingRow = []
		    for alarms in bdd:
		    	resultRingRow.append(alarms.ring) 
			resultRing = resultRingRow


			resultActiveRow = []
		    for alarms in bdd:
		    	resultActiveRow.append(alarms.active) 
			resultActive = resultActiveRow


			resultDayRow = []
		    for alarms in bdd:
		    	resultDayRow.append(alarms.day) 
			resultDay = resultDayRow


			resultIdRow = []
		    for alarms in bdd:
		    	resultIdRow.append(alarms.id) 
			resultId = resultIdRow


		    return render_template('alarm/delete.html' , heure=resultHeure , ring=resultRing , statut=resultActive , day=resultDay , id=resultId )
		except:
			return render_template('alarm/delete.html' , error="Pas de Reveil")
	

@core.route('/reveil/delete/<id_delete>')
def delete_reveil(id_delete):
	try:
		delete = AlarmModel.Alarm.query.filter_by(id=id_delete).first()
		db.session.delete(delete)
		db.session.commit()
		return redirect(url_for('reveildel'))
	except:
		return redirect(url_for('reveildel', error="Pas de Reveil avec cet ID"))

@core.route('/reveil/<ring_delete>')
def delete_ring(ring_delete):
	try:
		os.remove(os.path.join(music.RING_REPO + ring_delete))
		return redirect(url_for('reveil'))
	except:
		return redirect(url_for('reveil', error="Pas de Musique avec cet ID"))


@core.context_processor
def utility_processor():
    def formateDay(tab):
    	t = tab.replace("u"," ").replace("[","").replace("]","").replace("'","").replace("1","Lundi").replace("2","Mardi").replace("3","Mercredi").replace("4","Jeudi").replace("5","Vendredi").replace("6","Samedi").replace("0","Dimanche").replace("no","Pas de récurrence")
        return t
    return dict(formateDay=formateDay)
	
@core.context_processor
def utility_processor():
    def formateStatut(tab):
    	t = tab.replace("1","Activé").replace("0","Désactivé")
        return t
    return dict(formateStatut=formateStatut)

