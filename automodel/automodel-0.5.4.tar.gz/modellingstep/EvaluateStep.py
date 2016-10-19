from ModellingStep import ModellingStep
import os
import wx
from wx.lib.pubsub import Publisher

class EvaluateStep(ModellingStep):
	"""docstring for EvaluateStep"""
	def __init__(self,client_instance,workdir, template,model_file,ali_ali_file):
		super(EvaluateStep, self).__init__(client_instance, workdir)
		self.__list_of_files_should_send__ = [template,model_file,ali_ali_file]

	def __get_back_new_files__(self):
		self.evaluate_jpg = self.workdir + self.evaluate_jpg_name
		self.__client_instance__.receive_file(self.evaluate_jpg)

	def __run_my_step__(self):
		self.evaluate_jpg_name = self.__client_instance__.evaluate(self.__list_of_files_should_send__[0], self.__list_of_files_should_send__[1], self.__list_of_files_should_send__[2])

	def run(self):
		try:
			super(EvaluateStep, self).run()
			wx.CallAfter(Publisher().sendMessage, "OnAvaliarButtonDone", None)
			
		except Exception, e:
			wx.CallAfter(Publisher().sendMessage, "my_error", ["Nao foi possivel realizar a avaliacao por um erro interno do AutoModel", e])