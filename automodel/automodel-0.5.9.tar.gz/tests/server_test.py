import time
import tempfile
import os
import shutil

class server(object):
	"""docstring for server"""
	def __init__(self):
		time.sleep(1)
		self.workdir = tempfile.mkdtemp() + "/"
		print self.workdir


	def check_serial(self, serial):
		time.sleep(1)
		return True

	def receive_file(self, filename, buffer_file):
		received_file = file(self.workdir + os.path.basename(filename), "w")
		received_file.write(buffer_file)
		received_file.close()

	def find_templates(self,serial):
		pass

	def disconnect(self):
		pass

