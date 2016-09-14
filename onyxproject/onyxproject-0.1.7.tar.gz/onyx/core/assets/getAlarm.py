#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import json
import time
import threading
from onyx.core.assets import getHour
from onyx.core.assets import getSpeak
from onyx.core.assets import getMeteo
from onyx.core.assets import getMusic
from onyx.core import db
from onyx.core.models import *


def setAlarm():
	bdd = getBDD()
	getAlarm(bdd)
	threading.Timer(60, setAlarm).start()


def getBDD():
	try:
		bdd = AlarmModel.Alarm.query.all()
		print("Obtention des Alarmes")
		return bdd
	except:
		bdd = "Erreur"
		return bdd
	

def getAlarm(bdd):
	try:
		for alarms in bdd:
			today = str(getHour.getDay())	
			if today in alarms.day:
				now = getHour.getHour()
				bddalarm = alarms.heure.replace(" :",":").replace(": ",":")
				if alarms.active == "1":
					print("Prochaine Alarme : " + bddalarm + " Active")
				else : 
					print("Prochaine Alarme : " + bddalarm + " Desactive")
				if bddalarm == now and alarms.active == "1":
					lauchAlarm(alarms.ring)
			elif "no" in alarms.day:
				now = getHour.getHour()
				bddalarm = alarms.heure.replace(" :",":").replace(": ",":")
				if alarms.active == "1":
					print("Prochaine Alarme : " + bddalarm + " Active")
				else : 
					print("Prochaine Alarme : " + bddalarm + " Desactive")
				if bddalarm == now and alarms.active == "1":
					lauchAlarm(alarms.ring)
					delete = AlarmModel.Alarm.query.filter_by(id=alarms.id).first()
					db.session.delete(delete)
					db.session.commit()
	except Exception,e: print str(e)




def lauchAlarm(ring):
	print("Lancement de l'alarme en cour...")
	getMusic.getRing(ring)
	getSpeak.speak("Bonjour il est " + time.strftime("%H") + " heure " + time.strftime("%M") + " ,On est le " + time.strftime("%d/%m") + " et " + getMeteo.getText())
	