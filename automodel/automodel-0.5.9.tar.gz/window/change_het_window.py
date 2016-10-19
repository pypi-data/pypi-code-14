from wintools.wintools import *
from modellingfile.residues import *
from modellingfile.AlignFile import *
from modellingfile.pdbfile import *
import os
import sys
class ChangeHetWindow(subwintools):
	"""docstring for ChangeHetWindow"""
	def __init__(self, parent, id,  arquivoentrada):
		self.arquivoentrada = arquivoentrada
		self.Ions = TabelaDeTiposdeResiduos(os.path.dirname(os.path.realpath(sys.argv[0])) + "/Ions.txt")
		self.Cofatores = TabelaDeTiposdeResiduos(os.path.dirname(os.path.realpath(sys.argv[0])) + "/Cofatores.txt")
		self.pdbfile = pdbfile(arquivoentrada)
		self.pulldown_list = {}
		self.alifile = AlignFile(os.path.dirname(arquivoentrada) + "/ali.ali")
		self.Cadeias = self.pdbfile.chains()

		self.button = {} 
		wx.Dialog.__init__(self, parent, id, 'Changing Heteroatom',  size=(550,340))
		panel = wx.Panel(self, -1,  size=(550,340))
		self.panel = panel
		self.statictext = {}
		self.createText(panel)
		self.createMuchButtons(panel)
		self.parent = parent
		self.list_of_pull_downs = self.load_pull_down()

	def textData(self):
		list_of_text_data = [("Use the combobox below to change the heteroatoms of their respective chains.\nLocked combobox are heteroatoms that are not possible to change.", (20, 10))]
		posY = 45
		posYincrement = 40
		for selectedChain in self.Cadeias:
			list_of_text_data.append(("Chain " + selectedChain, (20, posY)))
			posY += posYincrement
		return list_of_text_data

	def list_of_possibles_residues(self, residue):
		if self.Ions.Contem(residue):
			return self.Ions.ListaTotalqueContem(residue)
		elif self.Cofatores.Contem(residue):
			return self.Cofatores.ListaTotalqueContem(residue)

	def symbol_of_residue(self, residue):
		if self.Ions.Contem(residue):
			return self.Ions.SimboloDe(residue)
		elif self.Cofatores.Contem(residue):
			return self.Cofatores.SimboloDe(residue)

	def symbol_of_heteroatom(self, heteroatom):
		if self.Ions.Contem(heteroatom):
			return self.Ions.SimboloDoHeteroatomo(heteroatom)
		elif self.Cofatores.Contem(heteroatom):
			return self.Cofatores.SimboloDoHeteroatomo(heteroatom)

	def residue_of_heteroatom(self, heteroatom):
		if self.Ions.Contem(heteroatom):
			return self.Ions.PossiveisNomes(heteroatom)[0]
		elif self.Cofatores.Contem(heteroatom):
			return self.Cofatores.PossiveisNomes(heteroatom)[0]

	def load_pull_down(self):
		dictionary_of_heteroatoms = {}
		posY = 45
		posYincrement = 40
		posX = 85
		posXincrement = 65
		for selectedChain in self.Cadeias:
			dictionary_of_heteroatoms[selectedChain] = {}
			for selectedHeteroatom in self.pdbfile.HetatomsInChain(selectedChain):
				if self.list_of_possibles_residues(selectedHeteroatom):
					dictionary_of_heteroatoms[selectedChain][selectedHeteroatom] = self.createOnePullDown(self.panel, posX,posY, self.list_of_possibles_residues(selectedHeteroatom))
				else:
					dictionary_of_heteroatoms[selectedChain][selectedHeteroatom] = self.createOnePullDown(self.panel, posX,posY, [selectedHeteroatom])
					dictionary_of_heteroatoms[selectedChain][selectedHeteroatom].Enable(False)
				posX += posXincrement
			posX = 85
			posY += posYincrement
		return dictionary_of_heteroatoms

	def buttonData(self):
		return(("Ok",self.ok, (100,280)),
				("Cancel",self.OnCloseWindow, (12,280)),)


	def ok(self,event):
		for selectedChain in self.Cadeias:
			for selectedHeteroatom in self.pdbfile.HetatomsInChain(selectedChain):	
				if self.list_of_pull_downs[selectedChain][selectedHeteroatom].Enabled:
					selection = self.list_of_pull_downs[selectedChain][selectedHeteroatom].GetStringSelection()

					self.change_heteroatom_of_align(selectedChain,selectedHeteroatom, selection)

					# print selectedHeteroatom + " "+  selection

					self.change_heteroatom_of_pdb(selectedChain, selectedHeteroatom, selection)
		self.alifile.write_changes()
		# self.alifile.__replace_files__()

		self.alifile.close()
		self.pdbfile.write()
		self.pdbfile.close()
		self.Destroy()

		


	def change_heteroatom_of_align(self,chain,heteroatom, string_selection):
		residue = self.get_residue_of_string_selection(string_selection)
		new_heteroatom = self.symbol_of_residue(residue)
		old_heteroatom = self.symbol_of_heteroatom(heteroatom)

		print old_heteroatom + "(" + heteroatom + ")" + "->" + new_heteroatom
		self.alifile.select_sequence(1)
		chain_number = self.Cadeias.index(chain) + 1
		self.alifile.change_heteroatom_of_chain(chain_number,old_heteroatom,new_heteroatom)
		self.alifile.select_sequence(2)
		self.alifile.change_heteroatom_of_chain(chain_number,old_heteroatom,new_heteroatom)

	def change_heteroatom_of_pdb(self,chain,old_heteroatom, new_heteroatom):
		residue = self.get_residue_of_string_selection(new_heteroatom)
		residue = self.residue_of_heteroatom(residue)
		self.pdbfile.ChangeHetatoms(chain,old_heteroatom,residue)

	def get_residue_of_string_selection(self, string_selection):
		return string_selection.split()[-1].replace("(", "").replace(")","")



