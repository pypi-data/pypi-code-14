import re
import os
from modellingfile.PDB2 import *
#arq = #nome do arquivo


class pdb2(pdb):
#  string file, chains;
    def __init__(self, arq):
        self.nomedoarq = arq
        self.file = file(arq, 'r')
        self.FileInList = self.file.readlines()


    
    def head(self):
        newFileInList = ""
        for i in self.FileInList:
            if not i[0:6]==("HETATM") and not i.startswith("ATOM") and not i.startswith("MASTER") and not i.startswith("TER") and not i.startswith("END") and not i.startswith("CONECT"):
                newFileInList = newFileInList + i
        return(newFileInList)
    def atom(self, cadeia, inicio):
        newFileInList = ""
        NumeroLinha = inicio+1
        for linha in self.FileInList:                
            if linha.startswith("ATOM") and linha[21] == cadeia:
                LinhaNova = linha[0:4]+" "*(7-len(str(NumeroLinha)))+str(NumeroLinha)+linha[11:(len(linha))]
                newFileInList = newFileInList + LinhaNova
                NumeroLinha = NumeroLinha+1                
        return(newFileInList);
        
    def hetatom(self, cadeia, inicio):
        newFileInList = ""
        NumeroLinha = inicio +1
        for linha in self.FileInList:
            if linha[0:6]==("HETATM") and linha[21] == cadeia:
                #print NumeroLinha
                LinhaNova = linha[0:6]+" "*(5-len(str(NumeroLinha)))+str(NumeroLinha)+linha[11:(len(linha))] #5
                newFileInList = newFileInList + LinhaNova
                NumeroLinha = NumeroLinha+1
        return(newFileInList);
    def fim(self, cadeia, inicio):
        newFileInList = ""
        NumeroLinha = inicio +1
        for linha in self.FileInList:
            if linha.startswith("TER") and linha[21] == cadeia:
                LinhaNova = linha[0:3]+" "*(8-len(str(NumeroLinha)))+str(NumeroLinha)+linha[11:(len(linha))]
                newFileInList = newFileInList + LinhaNova
                NumeroLinha = NumeroLinha+1
        return(newFileInList);    
    def conects(self):
        newFileInList = ""
        for linha in self.FileInList:
            if linha.startswith("CONECT"):
                newFileInList = newFileInList + linha
        return(newFileInList)
    def masters(self):
        newFileInList = ""
        for linha in self.FileInList:
            if linha.startswith("MASTER"):
                newFileInList = newFileInList + linha
        return(newFileInList)
    def ends(self):
        newFileInList = ""
        for linha in self.FileInList:
            if linha.startswith("END"):
                newFileInList = newFileInList + linha
        return(newFileInList)
    def construir(self):        
        newFileInList = self.head()
        inicio = 0
        
        for cadeia in self.chains():
            if newFileInList.splitlines()[-1][0:6]==("HETATM")  or newFileInList.splitlines()[-1].startswith("ATOM")   or newFileInList.splitlines()[-1].startswith("TER"): 
           # if newFileInList[-1].startswith("ATOM"):
                inicio = int(newFileInList.splitlines()[-1][6:11])
            else:
                inicio = 0
            newFileInList = newFileInList + self.atom(cadeia, inicio)
            inicio = int(newFileInList.splitlines()[-1][6:11])
            newFileInList = newFileInList + self.hetatom(cadeia, inicio)
            inicio = int(newFileInList.splitlines()[-1][6:11])
            newFileInList = newFileInList + self.fim(cadeia, inicio)
        inicio = int(newFileInList.splitlines()[-1][6:11])
        newFileInList = newFileInList + self.hetatom(" ", inicio)
        newFileInList = newFileInList + self.conects()
        newFileInList = newFileInList + self.masters()
        newFileInList = newFileInList + self.ends()
        
            #atoms
            #hetatoms
            #fim
        #hetatoms sem cadeia
        #fim
        return(newFileInList)

def fixpdb(arquivo):
  fix = pdb2(arquivo)
  arquivotemp = file(arquivo + ".tmp","w")
  arquivotemp.write(fix.construir())
  arquivotemp.close()
  os.rename(arquivo + ".tmp", arquivo)
#a = pdb2("1j36.pdb")
#print a.atom("A",0)
#x = file("/joao/Testes/teste.txt","w")
#x.write(a.construir())
#x.close()
#fixpdb("1j36.pdb")

