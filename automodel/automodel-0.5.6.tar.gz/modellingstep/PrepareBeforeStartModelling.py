from ModellingStep import *
import os,tempfile

class PrepareBeforeStartModelling(ModellingStep):
	"""docstring for LoadMySequenceStep"""
	def __init__(self):
		self.myworkdir = self.__prepare_workdir__()
		print self.myworkdir

	def __prepare_workdir__(self):
		return tempfile.mkdtemp() + os.path.sep

	def get_workdir(self):
		return self.myworkdir

	# def load_fasta_file(self, fasta_file):
	# 	pass

		