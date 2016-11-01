#!/usr/bin/env python
# -*- coding:utf-8 -*

from FSTA.installation import *
from FSTA.action import *
from FSTA.scenario import *
from FUTIL.my_logging import *

class group(object):
	"""A group of scenarios with a unique hotword
	"""
	def __init__(self, 
					name, 
					hotword = "./resource/snowboy.umdl", 
					scenarios = []):
		"""Initialisation
			- hotword			string containing path to a umdl or pmdl file as "Ok google" 
			- orders			list of order object
		"""
		# Hotword "Maison"
		self.name = name
		self.hotword = hotword
		if isinstance(scenarios, list):
			self.scenarios = scenarios
		else:
			self.scenarios = [scenarios]
		self.installation = None
		
	def init(self, installation):
		'''Initialise the group with installation datas
		'''
		self.installation = installation
		for scenario in self.scenarios:
			scenario.init(self)		
	
	def callback(self):
		""" Function called when the hotword match
		"""
		logging.info(self.name + " : J'écoute ...")
		self.installation.detector.terminate()
		self.installation.led.show_message("O")
		time.sleep(0.1)
		with sr.Microphone() as source:
			audio = self.installation.reconizer.listen(source)
		logging.info("Audio captured")
		self.installation.led.show_message("@")
		text = None
		#Google API
		try:
			text =  self.installation.reconizer.recognize_google(audio, key="AIzaSyDtizHAgEhUw5WjW9aRs84GUNk7o-fXwvA", language = 'fr-FR')
			logging.info("Text found with Google API: " + text)
		except sr.UnknownValueError:
			logging.warning("Google Speech Recognition could not understand audio")
		except sr.RequestError as e:
			logging.error("Could not request results from Google Speech Recognition service; {0}".format(e))
		#TODO : utiliser d'autres API
		if text:
			for scenario in self.scenarios:
				scenario.test(text)
			#Tri des résultats
			results = sorted(self.scenarios, key = lambda scenario:-scenario.valide)
			if results[0]:
				results[0].run(text)
			else:
				self.installation.led.show_message("?")
				time.sleep(0,5)
		self.installation.led.show_message(" ")
		self.installation.run()
