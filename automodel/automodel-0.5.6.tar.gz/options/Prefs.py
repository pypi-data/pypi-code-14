import os
class Prefs(object):
	"""docstring for Prefs"""
	
	def __init__(self):
		self.myprefs = {
		"ServerIP" : "200.20.229.25",
		#"ServerIP" : "127.0.0.1",
		# "ServerIP" : "192.168.0.103",
		"ServerPort" : 18861,
		"Online" : True,
		"PDBFolder" : os.getenv("HOME") + "/pdb/",

		}

	def __new__(cls, *args, **kwargs): #Implements a singleton class.
		if not hasattr(cls, '_instance'):
			cls._instance = super(Prefs, cls).__new__(cls, *args, **kwargs)
		return cls._instance

	def get_setting(self, setting_name):
		return self.myprefs[setting_name]

	def set_setting(self, setting_name, data):
		self.myprefs[setting_name] = data
		
