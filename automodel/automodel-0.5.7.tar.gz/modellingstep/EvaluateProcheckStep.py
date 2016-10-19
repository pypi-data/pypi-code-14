from ModellingStep import ModellingStep
import os
import wx
from wx.lib.pubsub import Publisher
import zipfile

class EvaluateProcheckStep(ModellingStep):
	"""docstring for EvaluateProcheckStep"""
	def __init__(self,client_instance,workdir, model_file):
		super(EvaluateProcheckStep, self).__init__(client_instance, workdir)
		self.__list_of_files_should_send__ = [model_file]

	def __get_back_new_files__(self):
		self.procheck_zip_file = self.workdir + self.procheck_zip_file
		self.__client_instance__.receive_file(self.procheck_zip_file)

	def __run_my_step__(self):
		self.procheck_zip_file = self.__client_instance__.evaluatePROCHECK(self.__list_of_files_should_send__[0])

	def __unzipper__(self,folder,zipped_file):
		zipz = zipped_file
		zipf = zipfile.ZipFile(zipz, "r" )
		zipf.extractall(folder)
		return folder

	def run(self):
		try:
			super(EvaluateProcheckStep, self).run()
			zip_folder = self.workdir + "avaliacao_procheck/"
			self.folder = zip_folder
			self.__unzipper__(zip_folder, self.procheck_zip_file)

			wx.CallAfter(Publisher().sendMessage, "OnPROCHECKButtonDone", None)
		except Exception, e:
			wx.CallAfter(Publisher().sendMessage, "my_error", ["Nao foi possivel realizar a avaliacao por um erro interno do AutoModel", e])