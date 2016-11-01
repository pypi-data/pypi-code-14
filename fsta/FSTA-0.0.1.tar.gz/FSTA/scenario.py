#!/usr/bin/env python
# -*- coding:utf-8 -*

from FSTA.installation import *
from FSTA.action import *
from FSTA.group import *
from FUTIL.my_logging import *


class scenario(object):
	"""Scenario if * or * or ... then ...
	"""
	exactly = 2
	contains = 1
	def __init__(self, phrases = [], actions = [], text = ""):
		"""Initialisation
			- phrases		list of unicode text
			- actions		list of actions obtect
			- text			explain the action (for logging)
		"""
		if isinstance(phrases, list):
			self.phrases = phrases
		else:
			self.phrases = [phrases]
		if isinstance(actions, list):
			self.actions = actions
		else:
			self.actions = [actions]	
		self.valide = False
		
	def run(self, text):
		"""Function called if phrases match
		- text		phrase dicted
		"""
		for action in self.actions:
			action.run(text)
	
	def init(self, group):
		""" Initialisation of the order with the installation datas
		"""
		for action in self.actions:
			action.installation = group.installation
	
	def test(self, text):
		"""test si le text correspond a une phrase.
		"""
		self.valide = False
		for phrase in self.phrases:
			if phrase.lower() == text.lower():
				self.valide = max(self.valide, scenario.exactly)
			elif phrase.lower() in text.lower():
				self.valide = max(self.valide, scenario.contains)
		return self.valide
		
		