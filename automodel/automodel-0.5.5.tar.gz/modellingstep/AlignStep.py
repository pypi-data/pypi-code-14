from ModellingStep import ModellingStep
import os
import wx
from wx.lib.pubsub import Publisher
from modellingfile.AlignFile import AlignFile

class AlignStep(ModellingStep):
	"""docstring for AlignStep"""
	def __init__(self, client_instance, workdir, template, pir_sequence_file):
		super(AlignStep, self).__init__(client_instance, workdir)
		self.__list_of_files_should_send__ = (pir_sequence_file, template)
		self.str_seq = None
		self.ali_ali = None
		self.ali_pap = None

	def __get_back_new_files__(self):
		self.str_seq = self.workdir + "str.seq"
		self.ali_ali = self.workdir + "ali.ali"
		# self.ali_pap = self.workdir + "ali.pap"
		self.__client_instance__.receive_file(self.str_seq)
		self.__client_instance__.receive_file(self.ali_ali)
		# self.__client_instance__.receive_file(self.ali_pap)

	def __run_my_step__(self):
		self.__client_instance__.align(self.__list_of_files_should_send__[0], self.__list_of_files_should_send__[1])

	def run(self):
		try:
			super(AlignStep, self).run()
			print "fim deste step"
			self.__normalize_align_file__()
			wx.CallAfter(Publisher().sendMessage, "OnAlinharButtonDone", None)
		except Exception, e:
			wx.CallAfter(Publisher().sendMessage, "my_error", ["Nao foi possivel realizar o alinhamento. Verifique a integridade do Template e da sequencia target.", e])

	def set_my_alignment(self,my_alignment_file):
		self.__copy_file_for_dir__(my_alignment_file, self.workdir + os.path.basename(my_alignment_file))
		self.ali_ali = self.workdir + os.path.basename(my_alignment_file)

	def __normalize_align_file__(self):
		aliali_for_modification = AlignFile(self.ali_ali)
		aliali_for_modification.copy_heteroatoms(0,1)
		aliali_for_modification.write_changes()
		aliali_for_modification.close()