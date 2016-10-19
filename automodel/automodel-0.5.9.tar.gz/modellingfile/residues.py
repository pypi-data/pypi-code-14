# -*- coding: iso-8859-1 -*- 
import re
class TabelaDeTiposdeResiduos():
    def __init__(self, arquivo):
        #self.arquivo = 
        self.arquivo = self.lerarquivo(file(arquivo,  "r"))
        self.ListadeResiduos = self.CriarLista()
    def  lerarquivo(self,  arquivo):
        tupla = []
        while True:
            linha = arquivo.readline()
            if len(linha) == 0:
                break
            else:
                tupla.append(filter(None,  re.split("	",  linha)))
        return(tupla)
     
    def CriarLista(self):
        lista = {}
        for cadaLinha in self.arquivo:
             lista[cadaLinha[3]] = (cadaLinha[1],  cadaLinha[2],  cadaLinha[4])
        return(lista)
    def ListadeTodosHeteroatomos(self):
         return(self.ListadeResiduos.keys())
         
    def PossiveisNomes(self, Heteroatomo):
        return(self.ListadeResiduos[Heteroatomo][0].split())
         
    def Contem(self, Heteroatomo):
        for cadaHeteroatomo in self.ListadeTodosHeteroatomos():
            if Heteroatomo in self.PossiveisNomes(cadaHeteroatomo) or Heteroatomo == cadaHeteroatomo:
                return(True)
        return(False)
        #return(Heteroatomo in self.ListadeTodosHeteroatomos())
    
    def ContemCHARMM(self, Heteroatomo):
        return(Heteroatomo in self.ListadeTodosHeteroatomos())
    def NomeDe(self, Heteroatomo):
        return(self.ListadeResiduos[Heteroatomo][2].rstrip('\r\n'))
        
    def SimboloDe(self, Heteroatomo):
        return(self.ListadeResiduos[Heteroatomo][1])
        
    def SimboloDoHeteroatomo(self, Heteroatomo):
        try:
            return self.SimboloDe(Heteroatomo)
        except Exception, e:
            if self.Contem(Heteroatomo):
                for cadaCHARMM in self.ListadeResiduos:
                        if Heteroatomo in self.PossiveisNomes(cadaCHARMM):
                            return(self.SimboloDe(cadaCHARMM))
            return(".")
        
    def ListaTotalqueContem(self, Heteroatomo):
        Lista = []
        for cadaHeteroatomo in self.ListadeTodosHeteroatomos():
            Nome = self.NomeDe(cadaHeteroatomo) + " (" + cadaHeteroatomo + ")"
            if Heteroatomo not in self.PossiveisNomes(cadaHeteroatomo):                
                Lista.append(Nome)
            else:
                Lista.insert(0, Nome)
                #Lista.append(Nome)
        return(Lista)
    def PegarCHARMMdaString(self, string):
        return(string.split()[-1].replace("(", "").replace(")",""))

#
#a = TabelaDeTiposdeResiduos("/joao/Alpha/src/Ions.txt")
#print a.ListadeTodosHeteroatomos()
#print a.Contem("HOH")
#print a.PossiveisNomes("TIP3") 
#print a.SimboloDe("CMO")
#print a.ListaTotalqueContem("TIP3")
#print a.SimboloDoHeteroatomo("HOH")
