from ModellingStep import ModellingStep
import os
import wx
from wx.lib.pubsub import Publisher

class ModelStep(ModellingStep):
	"""docstring for ModelStep"""
	def __init__(self, client_instance, workdir, template, ali_ali):
		super(ModelStep, self).__init__(client_instance, workdir)
		self.model = None
		self.__list_of_files_should_send__ = (ali_ali, template)

	def __get_back_new_files__(self):
		self.model = self.workdir + self.model_name
		self.__client_instance__.receive_file(self.model)

	def __run_my_step__(self):
		self.model_name = self.__client_instance__.model(self.__list_of_files_should_send__[0], self.__list_of_files_should_send__[1])

	def run(self):
		try:
			super(ModelStep, self).run()
			wx.CallAfter(Publisher().sendMessage, "OnModelarButtonDone", None)
			
		except Exception, e:
			wx.CallAfter(Publisher().sendMessage, "my_error", ["Nao foi possivel realizar a modelagem. Verifique a integridade do alinhamento e do template.", e])