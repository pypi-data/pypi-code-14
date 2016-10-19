class Sequence:
    def __init__(self,sequence_file):
        self.sequence_file = self.load_file_into_memory(sequence_file)

    def structures_names(self):
            file_in_tuple = self.sequence_file.splitlines()
            structures_list = []
            for eachline in file_in_tuple:
                if eachline.startswith('>P1;'):
                    struct = eachline[4:len(eachline)]
                    structures_list.append(struct)
            return structures_list
    def getStrname(self,number):
        if len(self.structures_names()[number]) == 5:
            return self.structures_names()[number][0:-1]
        else:
            return self.structures_names()[number]
                    
        
#        if(os.path.exists(arquivo)):
#          arqr = file(arquivo, 'r')
#          xtrs = ""
#          while True:
#            line = arqr.readline()
#            if (line.startswith('>P1;') and not line.startswith('>P1;seq.ali')): #cuidado structure:
#                i = 4 #CUIDADO i = 10
#                if(xtrs != ""):
#                    xtrs = xtrs + ','
#                while(line[i] != '\n'): #cuidado :
#                    xtrs = xtrs + line[i]
#                    i = i + 1
#            if len(line) == 0:
#                break
#          arqr.close() 
#          return xtrs

    def load_file_into_memory(self,arq):
        try:
            arquivo = open(arq,"rb")
        except IOError:
            print "Erro ao abrir o arquivo"
        arquivo.seek(0,2)
        tamanho = arquivo.tell()
        arquivo.seek(0)
        buffer = arquivo.read(tamanho)
        arquivo.close()
        return buffer

#x = Sequence("/tmp/tmphtU2mm/models/ali.ali")
#print x.structures_names()
#print x.getStrname(0)
        
