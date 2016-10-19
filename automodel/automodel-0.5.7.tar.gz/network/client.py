import rpyc
# from server_test import server
import shutil
from modellingfile.file import file
from options.Prefs import Prefs
import os

class Client(object):
	"""docstring for Client"""
	def __init__(self):
		# self.__server__ = server()
		self.__preferences__ = Prefs()
		self.__server_adress__ = self.__preferences__.get_setting("ServerIP")
		self.__version__ = "0.40"
		self.__server_port__ = self.__preferences__.get_setting("ServerPort")
		self.myserial = ""

	def connect_with_server(self):
		self.__connection__ = rpyc.connect(self.__server_adress__, self.__server_port__)
		self.__server__ = self.__connection__.root

	def check_serial(self,serial):
		self.connect_with_server()
		self.myserial = serial
		return self.__server__.check_serial(serial)

	def send_file(self,file_name):
		sending_file = file(file_name, "r")
		buffer_file = sending_file.load_in_memory()
		sending_file.close()
		self.__server__.receive_file(os.path.basename(file_name), buffer_file)

	def find_templates(self):
		self.__server__.find_templates(self.myserial)

	def receive_file(self, name_of_file):
		buffer_file = self.__server__.send_file(name_of_file)
		my_file = file(name_of_file, "w")
		my_file.write(buffer_file)
		my_file.close()

	def get_pdb_from_server(self, pdb_name):
		buffer_file = self.__server__.send_template(pdb_name)
		return buffer_file

	def align(self,pir_sequence_file,template):
		self.__server__.align(pir_sequence_file,template)
		
	def model(self,ali_ali, template):
		return self.__server__.model(ali_ali, template)

	def evaluate(self,template,model_file,ali_ali_file):
		return self.__server__.evaluate(template,model_file,ali_ali_file)

	def evaluatePROCHECK(self, model_file):
		return self.__server__.evaluatePROCHECK(model_file)

	def loopmodel(self, model_file, start_residue, end_residue):
		return self.__server__.loopmodel(model_file, start_residue, end_residue)
	def evaluatelooprefinament(self, template,model_file,loopmodel, ali_ali_file):
		return self.__server__.evaluatelooprefinament(template,model_file,loopmodel, ali_ali_file)

	def disconnect(self):
		self.__connection__.close()

