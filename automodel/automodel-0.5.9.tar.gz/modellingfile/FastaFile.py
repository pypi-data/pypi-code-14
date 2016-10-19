from file import file

class FastaFile(file):
	"""docstring for FastaFile"""
		
	def make_to_pir(self):
		filename = self.abspath() + "/seq.ali"
		pir_file = file(filename, "w")
		firstlines = '>P1;seq.ali\nsequence:seq.ali::::::::' + '\n'
		pir_file.write(firstlines)
		readlines = self.readlines()
		for eachLine in readlines[1:-1]:
			pir_file.write(eachLine.strip())
		lastline = readlines[-1].strip()
		modified_lastline = lastline.replace("\n","") + "*"
		pir_file.write(modified_lastline)
		return filename





