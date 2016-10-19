import os
from options.Prefs import Prefs
class AutoModelMode(object):
	"""docstring for AutoModelMode"""
	def __init__(self):
		self.automodelSettings = Prefs()

	def online_mode(self):
		self.automodelSettings.set_setting("Online", True)
	
	def offline_mode(self):		
		self.automodelSettings.set_setting("Online", False)

	def offline_mode_is_ready(self):
		is_ready = True
		if not os.path.exists(self.automodelSettings.get_setting("PDBFolder")):
			is_ready = False
		if not os.path.exists("/usr/bin/procheck"):
			is_ready = False

		try:
			import modeller
			import pylab
		except ImportError, e:
			is_ready = False

		return is_ready

