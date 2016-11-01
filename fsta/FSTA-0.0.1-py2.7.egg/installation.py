#!/usr/bin/env python
# -*- coding:utf-8 -*


import sys
import signal
import time
import paho.mqtt.client as paho
import threading
import logging
import max7219.led as led
import speech_recognition as sr

#TODO : plusieurs API (google, MS, ...) pour gérer quotas
#TODO : régler pb latence sur API google qui charabia


class installation(object):
	"""A complete installation containing :
		- groups of scenarios with unique start hotword
		- mqtt serveur
	"""
	def __init__(self, groups = [], mqtt_host='localhost', mqtt_port = 1883, led = None):
		"""Initialisation
			- groups		list of groups of scenarios
			- mqtt_host		mqtt host (default localhost)
			- mqtt_port		mqtt port (default 1883)
			- led			a max7219.led
		"""
		if isinstance(groups, list):
			self.groups = groups
		else:
			self.groups = [groups]
		self.hotwords = []
		self.callbacks = []
		for group in self.groups:
			self.hotwords.append(group.hotword)
			self.callbacks.append(group.callback)
			group.init(self)
		self.mqtt_client = paho.Client()
		self.mqtt_client.connect(mqtt_host, mqtt_port, 30)		
		self.interrupted = False
		self.led = led
		self.led.brightness(0)
		self.reconizer = sr.Recognizer()
		
	def run(self):
		"""Main function : wait for hotwords and run the callback function for the groups
		"""
		signal.signal(signal.SIGINT, self.signal_handler)
		self.detector = snowboydecoder.HotwordDetector(self.hotwords, sensitivity=0.5)
		self.detector.start(detected_callback=self.callbacks,
						interrupt_check=self.interrupt_callback,
						sleep_time=0.03)
		self.detector.terminate()
	
	def signal_handler(self, signal, frame):
		self.interrupted = True
	
	def interrupt_callback(self):
		return self.interrupted
	