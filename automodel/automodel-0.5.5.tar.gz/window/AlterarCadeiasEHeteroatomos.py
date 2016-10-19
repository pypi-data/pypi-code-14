# -*- coding: iso-8859-1 -*-
import os
from wintools.wintools import *
from modellingfile.PDB2 import *
from modellingfile.seq import *

class AlterarCadeiasEHeteroatomos(subwintools):
    def __init__(self, parent, id,  arquivoentrada, arquivoSeq_Ali):
        self.pdbfile = pdb(arquivoentrada)
        self.arquivoSeq_Ali = arquivoSeq_Ali
        self.PastaModels = os.path.dirname(arquivoentrada)
        self.Chain = self.pdbfile.chains()
        self.Heteroatomos = self.pdbfile.HetatomsInPDB()
        self.listadeChain = {}
        self.listadeChain = self.ListaDeChainEHeteroatomos(self.Chain)
        self.ChainSelecionadas = self.pdbfile.chains()
        self.statictext = {}
        self.NumeroDeMonomeros = 1

        self.listadeheteroatomos = self.Heteroatomos
        self.button = {}
        self.checkbox = {}
        self.radio = {}
        wx.Dialog.__init__(self, parent, id, 'Selecting Chains and Heteroatoms',  size=(self.CalcularOValorXdaJanela(self.Chain),340)) #Cria o frame
        panel = wx.Panel(self, -1,  size=(self.CalcularOValorXdaJanela(self.Chain),340))
        self.createMuchButtons(panel)
        panel.SetBackgroundColour("LightGray")
        self.createManyRadios(panel)
        self.createCheckBox(panel)
        self.createText(panel)
        self.parent = parent
    def replicarSequencia(self, arquivoSeq_Ali, numerodevezes):
        seq = sequencia(arquivoSeq_Ali, 1)
        arquivoSeq_AliNovo = file(os.path.dirname(arquivoSeq_Ali) + os.sep + "seq.ali2",  "w")
        for i in range(0, seq.tamanho()):
            if i != 2: #onde esta a sequencia
                arquivoSeq_AliNovo.write(seq.conteudodasequencia()[i])
            else:
                  arquivoSeq_AliNovo.write((numerodevezes-1)*(seq.conteudodasequencia()[i][0:len(seq.conteudodasequencia()[2])-1]+ os.sep)+(seq.conteudodasequencia()[i]))
        arquivoSeq_AliNovo.close()
        os.rename(arquivoSeq_Ali, arquivoSeq_Ali + ".old" )
        os.rename(os.path.dirname(arquivoSeq_Ali) + os.sep + "seq.ali2", arquivoSeq_Ali)

    def textData(self):#labels
        return(("Select the chains and heteroatoms", (20, 10)), ("to be used in alignment:", (20, 23)))

    def ListaDeChainEHeteroatomos(self, Chain):
        DicionarioDeChainComHetereoatmos = {}
        for eachChain in Chain:
            Lista = self.pdbfile.HetatomsInChain(eachChain)
            DicionarioDeChainComHetereoatmos[eachChain] = Lista
        return DicionarioDeChainComHetereoatmos

    def CalcularOValorXdaJanela(self,  Chain):
        return(280+140*len(Chain))

    def buttonData(self):
        return(("Ok",self.ok, (self.CalcularOValorXdaJanela(self.Chain)-100,280)),
                    ("Cancel",self.Cancelar, (self.CalcularOValorXdaJanela(self.Chain)-200,280)) )
    def radioData(self):
        return(("Monomer",  (self.CalcularOValorXdaJanela(self.Chain)-400, 270)), ("Dimer",  (self.CalcularOValorXdaJanela(self.Chain)-300, 270)), ("Trimer",  (self.CalcularOValorXdaJanela(self.Chain)-400, 290)), ("Tetramer",  (self.CalcularOValorXdaJanela(self.Chain)-300, 290)) )

    def checkboxdata(self):
        Lista = []
        posX = 40
        Lista.append(('Chain',  self.Chain, (posX, 50),   self.checkboxChain))
        for eachChain in self.Chain:
            heteroatomos = self.pdbfile.HetatomsInChain(eachChain)
            nome = "Chain " + eachChain
            posX = posX + 100
            Lista.append((nome,  heteroatomos, (posX,  50),  self.checkboxheteroatomo))
        return(Lista)

    def createCheckBox(self, panel):
            for eachList in self.checkboxdata():
                posX = eachList[2][0]
                posY = eachList[2][1]
                posYold = posY
                check = {}
                for eachElemento in eachList[1]:
                    posY = posY + 30;
                    check[eachElemento] = self.buidOneCheckbox(panel,  eachElemento,  posX+len(eachList[0]),  posY)
                    check[eachElemento].SetValue(True)
                    self.Bind(wx.EVT_CHECKBOX,  eachList[3], check[eachElemento] )
                if eachList[0] != "Chain":
                    self.checkbox[eachList[0]] = check

                wx.StaticBox(panel,  -1, eachList[0], (posX, posYold), (len(eachList[0])*12, posY-posYold+28))

    def buidOneCheckbox(self, panel,  Elemento,  posX,  posY):
            checkbox = wx.CheckBox(panel,  -1,  Elemento,  (posX ,  posY))
            return checkbox
    def checkboxChain(self, event):
        NomeDaCheckbox = 'Chain ' + event.GetEventObject().GetLabel()
        if(event.IsChecked()):
            self.ChainSelecionadas.append(event.GetEventObject().GetLabel())
            for eachHeteroatomo in self.checkbox[NomeDaCheckbox]:
                 self.checkbox[NomeDaCheckbox][eachHeteroatomo].Enable(True)
        else:
            self.ChainSelecionadas.remove(event.GetEventObject().GetLabel())
            for eachHeteroatomo in self.checkbox[NomeDaCheckbox]:
                self.checkbox[NomeDaCheckbox][eachHeteroatomo].Enable(False)
    def checkboxheteroatomo(self,  event):
           for eachChain in self.Chain:
                Nome = "Chain " + eachChain
                for eachHeteroatomo in self.checkbox[Nome]:
                    if (event.GetEventObject() == self.checkbox[Nome][eachHeteroatomo]):
                        if(event.IsChecked()):
                            self.listadeChain[eachChain].append(eachHeteroatomo)
                        else:
                            self.listadeChain[eachChain].remove(eachHeteroatomo)
    def ok(self,panel):
        if(self.ChainSelecionadas != []):
            pdbnovo = self.pdbfile.const(self.listadeChain,  self.ChainSelecionadas)
            arq = file(self.pdbfile.Nome()  , 'w')
            arq.write(pdbnovo)
            arq.close()
            self.replicarSequencia(self.arquivoSeq_Ali, self.NumeroDeMonomeros)

            self.Destroy()
        else:
            print("ExcecaoLR")
    def Cancelar(self, event):
        self.Destroy()
    def OnRadio(self, event):
        NomeDoRadio = event.GetEventObject().GetLabel()
        if NomeDoRadio == "Monomer":
            self.NumeroDeMonomeros = 1
        elif NomeDoRadio == "Dimer":
            self.NumeroDeMonomeros = 2
        elif NomeDoRadio == "Trimer":
            self.NumeroDeMonomeros = 3
        else:
            self.NumeroDeMonomeros = 4



# if __name__ == '__main__':
#    app = wx.PySimpleApp()
#    frame = AlterarChainEHeteroatomos(None,-1,  "/tmp/tmpx6oilt/1myn.pdb","/tmp/tmpx6oilt/seq.ali")
#    frame.Show()
#    app.MainLoop()

