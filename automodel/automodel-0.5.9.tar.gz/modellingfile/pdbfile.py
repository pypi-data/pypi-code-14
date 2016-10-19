import re
import os
class pdbfile:
#  string file, chains;
    def __init__(self, arq):
        self.nomedoarq = arq
        self.file = file(arq, 'r')
        
        self.FileInList = self.file.readlines()        
    def Nome(self):
        return(self.file.name)
    def NomedaEstrutura(self):
        PrimeiraLinha = self.FileInList[0]
        if "HEADER" in PrimeiraLinha:
            return PrimeiraLinha[62:66].lower()
        else:
            print("Excecao: Arquivo PDB fora do Padrao")
    def nomedoarquivo(self):
        return(self.nomedoarq)
    def chains(self):
        List = []
        for i in self.LinhasOndeTemEscritoChain():
            texto = self.FileInList[i]
            if "CHAIN:" in texto:
                ChainPositionInTheString = texto.find(":") + 2
                if ";" in texto:
                    EndPositionInTheString = texto.find(";")
                else:
                    EndPositionInTheString = len(texto)-1                
                for j in range(ChainPositionInTheString,  EndPositionInTheString):
                    if texto[j] not in [' ',','] and texto[j] not in List:
                        List.append(texto[j])            
               
            else:
                #excecao
                print("error")
        return(List)
    def LinhasOndeTemEscritoChain(self):
        Linhas = []
        Contador = 0
        for i in self.FileInList: 

            if "CHAIN:" in i:
                Linhas.append(Contador)
            Contador+=1 
        return(Linhas)
    
    def hetatm(self):
        for i in self.FileInList:
            if  i.startswith("HETATM"):
                return(True)
        return(False)
        
    def hoh(self):
        return "HOH" in self.HetatomsInPDB()

    def HetatomsInPDB(self):
        if self.hetatm():
            List = []
            for i in self.FileInList:
                if ("HETATM" in i) and not ("REMARK" in i):
                    #Line = filter(None, re.split(" ", i))
                    if not i[17:20].replace(" ", "") in List:
                        List.append(i[17:20].replace(" ", ""))
            return(List)
        else:
            return []
            
    def ChangeHetatoms(self, Cadeia, Hetoriginal, Hetnovo):
        if self.hetatm():
            for linha in self.FileInList:
                if ("HETATM" in linha) and not ("REMARK" in linha):
                    if linha[17:20].strip() == Hetoriginal and linha[21] in Cadeia:
                        new_line = self.__type_line__(linha) + self.__serial_line__(linha) + self.__atom_name__(linha) + self.__altLoc__(linha) + self.__resName__(Hetnovo) + " " + self.__chainId__(linha) + self.__resSeq__(linha) +\
                        self.__iCode__(linha) + 3*" " + self.__xyz__(linha) + self.__occupancy__(linha) + self.__tempFactor__(linha) + 10*" " + self.__element__(linha) + self.__charge__(linha) + "\n"
                        self.FileInList[self.FileInList.index(linha)] = new_line
                        # print new_line

    def __type_line__(self,line):
        return(line[0:6])

    def __serial_line__(self,line):
        return(line[6:11])

    def __atom_name__(self,line):
        return(line[11:16])

    def __altLoc__(self,line):
        return(line[17])

    def __resName__(self,Hetnovo):
        if len(Hetnovo) == 3:
            return Hetnovo
        else:
            return " " + Hetnovo

    def __chainId__(self,line):
        return(line[21])

    def __resSeq__(self,line):
        return(line[22:26])

    def __iCode__(self,line):
        return line[27]

    def __xyz__(self, line):
        return(line[30:54])

    def __occupancy__(self, line):
        return line[54:60]

    def __tempFactor__(self,line):
        return line[60:66]

    def __element__(self,line):
        return line[76:78]

    def __charge__(self,line):
        return line[78:80]

    def write(self):
        tmpfile = file(self.nomedoarq + ".tmp", "w")
        for selectedline in self.FileInList:
            tmpfile.write(selectedline)
        tmpfile.close()
        self.file.close()
        os.remove(self.nomedoarq)
        os.rename(tmpfile.name,self.nomedoarq)
        self.file = file(self.nomedoarq, "r")
        self.FileInList = self.file.readlines()
    
    def HetatomsInChain(self,  chain):
        if self.hetatm():
            List = []
            for i in self.FileInList:
                if ("HETATM" in i) and not ("REMARK" in i):
                    if ((not i[17:20].replace(" ", "") in List) and (chain == i[21])):
                        List.append(i[17:20].replace(" ", ""))
            return(List)
        else:
            print("excecao")

    def close(self):
        self.file.close()
