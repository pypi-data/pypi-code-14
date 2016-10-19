import os

class file(file):
	def is_fasta(self):
		readlines = self.readline()
		first_line = readlines[0].decode()
		last_line = readlines[-1].decode()
		print last_line
		return first_line.startswith(">") and not last_line.endswith("*\n")

	def load_in_memory(self):
		self.seek(0,2)
		size = self.tell()
		self.seek(0)
		buffer = self.read(size)
		return buffer

	def abspath(self):
		return os.path.dirname(os.path.abspath(self.name))