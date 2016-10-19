import unittest
import tempfile
from should_dsl import *
from pdbfile import pdbfile
import os
import shutil
pdb_folder = './tests/models/'

class PdbFileTest(unittest.TestCase):
	def setUp(self):
		self.path_pdb = pdb_folder + '1uij.pdb' 
		os.remove(self.path_pdb)
		shutil.copyfile(pdb_folder + '1uij2.pdb', self.path_pdb)
		self.pdb = pdbfile(self.path_pdb)
		self.pdb_1IKN = pdbfile(pdb_folder + '1IKN.pdb') #this pdb has a name in caps and the header is out of default
		self.pdb_1bdm = pdbfile(pdb_folder + '1bdm.pdb') #this pdb hasnt any heteroatms
		self.pdb_1civ = pdbfile(pdb_folder + '1civ.pdb') #this pdb hasnt  any HOH

	def test_pdb_has_a_name(self):
		self.pdb.Nome() |should| equal_to(pdb_folder + '1uij.pdb')

	def test_pdb_has_a_name_of_struct(self):
		self.pdb.NomedaEstrutura() |should| equal_to('1uij')

	def test_pdb_name_of_struct_is_case_sensitive(self):
		self.pdb_1IKN.NomedaEstrutura() |should| equal_to('1ikn')

	def test_pdb_has_a_name_of_file(self):
		self.pdb.nomedoarquivo() |should| equal_to(pdb_folder + '1uij.pdb')

	def test_pdb_name_of_file_is_case_sensitive(self):
		self.pdb_1IKN.nomedoarquivo() |should| equal_to(pdb_folder + '1IKN.pdb')

	def test_pbd_have_chains(self):
		self.pdb.chains() |should| equal_to(['A','B','C','D','E','F'])

	def test_pdb_has_the_header_out_of_default(self):
		self.pdb_1IKN.chains() |should| equal_to(['A','C','D'])

	def test_when_pdb_has_one_line_where_it_is_written_CHAIN(self):
		self.pdb.LinhasOndeTemEscritoChain() |should| equal_to([5])

	def test_when_pdb_has_many_lines_where_it_is_written_CHAIN(self):
		self.pdb_1IKN.LinhasOndeTemEscritoChain() |should| equal_to([4,10,16])

	def test_pdb_has_any_heteroatom(self):
		self.pdb.hetatm() |should| equal_to(True)

	def test_pdb_has_noany_heteroatom(self):
		self.pdb_1bdm.hetatm() |should| equal_to(False)

	def test_pdb_has_water(self):
		self.pdb.hoh() |should| equal_to(True)

	def test_pdb_hasnt_water(self):
		self.pdb_1bdm.hoh() |should| equal_to(False)

	def test_pdb_hasnt_water_but_it_has_heteroatom(self):
		self.pdb_1civ.hoh() |should| equal_to(False)

	def test_pdb_has_heteroatom(self):
		self.pdb.HetatomsInPDB() |should| equal_to(['HOH'])

	def test_if_pdb_hasnt_heteroatom_then_the_list_is_empty(self):
		self.pdb_1bdm.HetatomsInPDB() |should| equal_to([])

	def test_chain_of_pdb_has_heteroatom(self):
		self.pdb.HetatomsInChain("A") |should| equal_to(['HOH'])

	def test_change_heteroatom_of_pdb(self):
		self.pdb.ChangeHetatoms("A", "HOH", "CO")
		self.pdb.HetatomsInChain("A") |should| equal_to(['CO'])

	def test_write_pdb(self):
		self.pdb.ChangeHetatoms("A", "HOH", "ZN")
		self.pdb.write()
		self.pdb.close()
		pdb2 = pdbfile(self.path_pdb)
		pdb2.HetatomsInChain("A") |should| equal_to(['ZN'])

	def test_write_pdb_twice_with_heteroatom_with_two_letters(self):
		self.pdb.ChangeHetatoms("A", "HOH", "ZN")
		self.pdb.write()
		self.pdb.close()
		pdb2 = pdbfile(self.path_pdb)	
		pdb2.ChangeHetatoms("A", "ZN", "CO")	
		pdb2.write()	
		pdb2.HetatomsInChain("A") |should| equal_to(['CO'])

	def change_heteroatom_of_two_leters_for_three_leters(self):
		self.pdb.ChangeHetatoms("A", "HOH", "ZN")
		self.pdb.write()
		self.pdb.close()
		pdb2 = pdbfile(self.path_pdb)	
		pdb2.ChangeHetatoms("A", "ZN", "MP_")	
		pdb2.write()	
		pdb2.HetatomsInChain("A") |should| equal_to(['MP_'])
	# def test_pdb_is_builded(self):
	# 	pdb_modified = self.pdb.const({'A': ['HOH'], 'C': ['HOH'], 'D': ['HOH']},['A', 'C'])
	# 	file_temp = tempfile.mkstemp()
	# 	pdb_file_modified = file(file_temp[1],"w")
	# 	pdb_file_modified.write(pdb_modified)
	# 	pdb_file_modified.close()
	# 	pdb2 = pdb(file_temp[1])
	# 	pdb2.chains() |should| equal_to(['A', 'C'])	

	

if __name__ == '__main__':
    unittest.main()
