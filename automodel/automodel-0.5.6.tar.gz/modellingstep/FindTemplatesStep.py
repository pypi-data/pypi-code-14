from ModellingStep import ModellingStep
import os
import wx
from wx.lib.pubsub import Publisher
from modellingfile.FastaFile import FastaFile


class FindTemplatesStep(ModellingStep):
	"""docstring for FindTemplatesStep"""

	def __init__(self, client_instance, workdir):
		super(FindTemplatesStep, self).__init__(client_instance, workdir)

		self.fasta_file = None
		self.template = None
		self.pir_sequence_file = None
		self.build_profilePAP = None
		self.build_profilePIR = None
		self.build_profilePRF = None
		self.template = None
		# self.build_profilePY = None

	def set_fasta_file(self, fasta_file):
		self.__copy_file_for_dir__(fasta_file, self.workdir + os.path.basename(fasta_file))
		self.fasta_file = self.workdir + os.path.basename(fasta_file)

	def set_my_template(self,my_template_file):
		self.__copy_file_for_dir__(my_template_file, self.workdir + (os.path.basename(my_template_file)).lower())
		self.template = self.workdir + (os.path.basename(my_template_file)).lower()
		self.__convert_fasta_to_pir__()

	def set_my_template_without_fasta_file(self,my_template_file):
		self.__copy_file_for_dir__(my_template_file, self.workdir + os.path.basename(my_template_file))
		self.template = self.workdir + os.path.basename(my_template_file)
		# self.__convert_fasta_to_pir__()

	def get_template_filename(self):
		return self.template

	def __convert_fasta_to_pir__(self):
		my_fasta_file = FastaFile(self.fasta_file, 'r')
		self.pir_sequence_file = my_fasta_file.make_to_pir()


	def run(self):
		self.__convert_fasta_to_pir__()
		super(FindTemplatesStep, self).run()
		wx.CallAfter(Publisher().sendMessage, "onFindTemplatesStepDone", None)

	def __get_back_new_files__(self):
		self.build_profilePAP = self.workdir + "build_profilePAP.ali"
		self.build_profilePIR = self.workdir + "build_profilePIR.ali"
		self.build_profilePRF = self.workdir + "build_profile.prf"
		self.__client_instance__.receive_file(self.build_profilePAP)
		self.__client_instance__.receive_file(self.build_profilePIR)
		self.__client_instance__.receive_file(self.build_profilePRF)

	def select_template(self, template_name):
		try:
			self.__client_instance__.connect_with_server()
			buffer_file = self.__client_instance__.get_pdb_from_server(template_name)
			self.template = self.workdir + template_name + ".pdb"
			template_file = file(self.template, "w")
			template_file.write(buffer_file)
			template_file.close()
			self.__client_instance__.disconnect()
			wx.CallAfter(Publisher().sendMessage, "onChooseTemplateDone", None)			
		except IOError, e:
			wx.CallAfter(Publisher().sendMessage, "my_error", ["Nao foi possivel realizar a Modelagem. Verifique a integridade do alinhamento e do template.", e])

	def __run_my_step__(self):
		self.__client_instance__.find_templates()

	def __send_files__(self):
		self.__client_instance__.send_file(self.pir_sequence_file)