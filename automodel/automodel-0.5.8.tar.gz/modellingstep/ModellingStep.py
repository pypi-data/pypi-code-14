import shutil
from threading import *

class ModellingStep(object):
	"""docstring for ModellingStep"""
	def __init__(self, client_instance, workdir):
		self.__client_instance__ = client_instance
		self.workdir = workdir
		self.__list_of_files_should_send__ = ()

	def __copy_file_for_dir__(self, path_of_file, destination):
		shutil.copyfile(path_of_file, destination)

	def run(self):
		self.__client_instance__.connect_with_server()
		self.__send_files__()
		self.__run_my_step__()
		self.__get_back_new_files__()
		self.__client_instance__.disconnect()
		# wx.CallAfter(Publisher().sendMessage, "onChooseTemplateDone", None)

	def __get_back_new_files__(self):
		pass

	def __send_files__(self):
		for eachFile in self.__list_of_files_should_send__:
			self.__client_instance__.send_file(eachFile)

	def __run_my_step__(self):
		pass



