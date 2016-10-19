from ModellingStep import ModellingStep
import os
import wx
from wx.lib.pubsub import Publisher

class LoopModelStep(ModellingStep):
	"""docstring for ModelStep"""
	def __init__(self, client_instance, workdir, model):
		super(LoopModelStep, self).__init__(client_instance, workdir)
		self.loopmodel = None
		self.start_residue = None
		self.end_residue = None
		self.__list_of_files_should_send__ = [model]

	def __get_back_new_files__(self):
		self.loopmodel = self.workdir + self.model_name
		self.__client_instance__.receive_file(self.loopmodel)

	def __run_my_step__(self):
		self.model_name = self.__client_instance__.loopmodel(self.__list_of_files_should_send__[0], self.start_residue, self.end_residue)

	def set_start_residue(self, position):
		self.start_residue = position

	def set_end_residue(self,position):
		self.end_residue = position

	def run(self):
		try:
			super(LoopModelStep, self).run()
			wx.CallAfter(Publisher().sendMessage, "send_loop_refinamentDone", None)
			
		except Exception, e:
			wx.CallAfter(Publisher().sendMessage, "my_error", ["Nao foi possivel realizar o refinamento. Verifique a integridade do modelo.", e])