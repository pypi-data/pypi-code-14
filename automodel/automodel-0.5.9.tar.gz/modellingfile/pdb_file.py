class Pdb_File():
	"""docstring for Pdb_File"""
	def __init__(self, filename):
		# self.filename = filename
		self.pdb_file = file(filename, "r")
		self.pdb_cotent_in_list = self.pdb_file.readlines()

	def start_residue(self):
		pos = 1
		line = self.pdb_cotent_in_list[pos]
		while not line.startswith("ATOM"):
			pos = pos + 1
			line = self.pdb_cotent_in_list[pos]
		else:
			number_of_first_residue = line[22:26]
		return int(number_of_first_residue)

	def end_residue(self):
		pos = -1
		line = self.pdb_cotent_in_list[pos]
		while not line.startswith("TER"):
			pos = pos - 1
			line = self.pdb_cotent_in_list[pos]
		else:
			number_of_last_residue = line[22:26]
		return int(number_of_last_residue)
