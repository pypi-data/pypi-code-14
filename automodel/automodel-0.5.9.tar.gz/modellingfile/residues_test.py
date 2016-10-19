import unittest
import tempfile
from should_dsl import *
from residues import TabelaDeTiposdeResiduos
table_folder = './'

class ResiduesTableTest(unittest.TestCase):
	def setUp(self):
	  self.table = TabelaDeTiposdeResiduos(table_folder + 'Ions.txt')
	  self.table_of_cofators = TabelaDeTiposdeResiduos(table_folder + 'Cofatores.txt')
		
	# def test_generate_list(self):
	#   x = {'MG': ('MG', '$', 'magnesium ion\r\n'), 'CO': ('CMO CO', 'b', 'CO ligand for heme\r\n'), 'SOD': ('NA SOD', 'I', 'Sodium\r\n'), 'PPI1': ('PPI', 'f', 'Inorganic phosphate\r\n'), 'O2': ('OXY O2', 'o', 'O2 ligand for heme\r\n'), 'ZN2': ('ZN ZN2', 'z', 'Zinc, +2\r\n'), 'CAL': ('CA CAL', '3', 'calcium ion, +2\r\n'), 'MP_2': ('MP_', '2', 'Methylphosphate, diaonic\r\n'), 'TIP3': ('HOH H2O OH2 MOH WAT', 'w', 'water\r\n'), 'MP_1': ('MP_', '1', 'Methylphosphate, anionic\r\n'), 'DMPA': ('DMP', 'm', 'Dimethylphosphate, neutral\r\n'), 'MP_0': ('MP_', '0', 'Methylphosphate, neutral\r\n'), 'DUM': ('DUM', '#', 'DUMMY ATOM\r\n')}
	#   self.table.CriarLista() |should| equal_to(x)

	def test_list_all_heteroatoms(self):
		self.table.ListadeTodosHeteroatomos() |should| equal_to(['MG', 'CO', 'SOD', 'PPI1', 'O2', 'ZN2', 'CAL', 'MP_2', 'TIP3', 'MP_1', 'DMPA', 'MP_0', 'DUM'])

	def test_possibles_names_of_one_residue(self):
		self.table.PossiveisNomes("TIP3") |should| equal_to(['HOH', 'H2O', 'OH2', 'MOH', 'WAT'])
		
	def test_if_list_contain_a_residue(self):
		self.table.Contem("HOH") |should| equal_to(True)

	def test_if_list_contain_a_residue_under_another_name(self):
		self.table.Contem("WAT") |should| equal_to(True)

	def test_if_list_contain_a_residue(self):
		self.table.Contem("TIP3") |should| equal_to(True)

	def test_if_list_no_contain_a_residue(self):
		self.table.Contem("DUM2") |should| equal_to(False)

	def test_list_contain_CHARMM_name(self):
		self.table.ContemCHARMM("DUM") |should| equal_to(True)

	def test_list_no_contain_CHARMM_name(self):
		self.table.ContemCHARMM("DUM2") |should| equal_to(False)

	def test_name_of_residue(self):
		self.table.NomeDe("DUM") |should| equal_to("DUMMY ATOM")

	def test_residue_symbol(self):
		self.table.SimboloDe("TIP3") |should| equal_to("w")

	def test_residue_symbol_of_NAD(self):
		self.table_of_cofators.SimboloDoHeteroatomo("NAD") |should| equal_to("n")

	def  test_heteroatom_symbol(self):
		self.table.SimboloDoHeteroatomo("HOH") |should| equal_to("w")

	def  test_Zinc_symbol(self):
		self.table.SimboloDoHeteroatomo("ZN") |should| equal_to("z")

	def test_unknown_heteroatom_symbol(self):
		self.table.SimboloDoHeteroatomo("DUM2") |should| equal_to(".")

	def test_list_containing_the_residue(self):
		self.table.ListaTotalqueContem("HOH") |should| equal_to(['water (TIP3)', 'magnesium ion (MG)', 'CO ligand for heme (CO)', 'Sodiu (SOD)', 'Inorganic phosphate (PPI1)', 'O2 ligand for heme (O2)', 'Zinc, +2 (ZN2)', 'calcium ion, +2 (CAL)', 'Methylphosphate, diaonic (MP_2)', 'Methylphosphate, anionic (MP_1)', 'Dimethylphosphate, neutral (DMPA)', 'Methylphosphate, neutral (MP_0)', 'DUMMY ATOM (DUM)'])

	def test_get_CHARMM_of_name(self):
		self.table.PegarCHARMMdaString('water (TIP3)') |should| equal_to('TIP3')

if __name__ == '__main__':
    unittest.main()
		
		
#
#a = TabelaDeTiposdeResiduos("/joao/Alpha/src/Ions.txt")
#print a.ListadeTodosHeteroatomos()
#print a.Contem("HOH")
#print a.PossiveisNomes("TIP3") 
#print a.SimboloDe("CMO")
#print a.ListaTotalqueContem("TIP3")
#print a.SimboloDoHeteroatomo("HOH")