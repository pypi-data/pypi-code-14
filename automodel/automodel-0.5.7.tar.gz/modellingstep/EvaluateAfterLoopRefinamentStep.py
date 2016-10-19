from ModellingStep import ModellingStep
import os
import wx
from wx.lib.pubsub import Publisher

class EvaluateAfterLoopRefinamentStep(ModellingStep):
	"""docstring for EvaluateAfterLoopRefinamentStep"""
	def __init__(self,client_instance,workdir, template,model_file,loopmodel,ali_ali_file):
		super(EvaluateAfterLoopRefinamentStep, self).__init__(client_instance, workdir)
		self.__list_of_files_should_send__ = [template,model_file,loopmodel, ali_ali_file]

	def __get_back_new_files__(self):
		self.evaluateloop_jpg = self.workdir + self.evaluate_jpg_name
		self.__client_instance__.receive_file(self.evaluateloop_jpg)

	def __run_my_step__(self):
		self.evaluate_jpg_name = self.__client_instance__.evaluatelooprefinament(self.__list_of_files_should_send__[0], self.__list_of_files_should_send__[1], self.__list_of_files_should_send__[2], self.__list_of_files_should_send__[3])

	def run(self):
		super(EvaluateAfterLoopRefinamentStep, self).run()
		wx.CallAfter(Publisher().sendMessage, "EvaluateAfterLoopRefinamentStepDone", None)
