import re

class estruturaprf():
    def __init__(self, estrutura):
        self.estrutura = estrutura
        self.estruturaparticionada = filter(None,  re.split(" ",  self.estrutura))
    def __str__(self):
        return float(self.estruturaparticionada[10])
    def Nome(self):
        return self.estruturaparticionada[1]
    def Tipo(self):
        return self.estruturaparticionada[2]
    def IniciodaEstrutura(self):
        return self.estruturaparticionada[5]
    def FimdaEstrutura(self):
        return self.estruturaparticionada[6]
    def QuantidadedeResiduos(self):
        return self.estruturaparticionada[9]
    def Identidade(self):
        return self.estruturaparticionada[10]


#if __name__ == '__main__':
#    teste = "4 1bdmA                                    X     1   318     1   325     1   310   309   45.    0.0     MKAPVRVAVTGAAGQIGYSLLFRIAAGEMLGDQPVILQLLEIPQAMKALEGVVMELEDCAFPLLAGLEATDDPDVAFKDADYALLVGAAP---------RLQVNGKIFTEQGRALAEVAKKDVKVLVVGNPANTNALIAYKNAPGLNPRNFTAMTRLDHNRAKAQLAKKTGTGVDRIRRMTVWGNHSSIMFPDL----FHAEVDGRPALELVDMEWYEKVFIPTVAQRGAAIIQARGASSAASAANAAIEHIRDWALGTPEGDWVSMA--VPSQGEYGIPEGIVYSFPVTA-KDGAYRVVEGLEINEFARKRMEITAQELLDEME----------"
#    
#    PAP = estruturaprf(teste)
#    print PAP.Nome()
#    print PAP.Tipo()
#    print PAP.IniciodaEstrutura()
#    print PAP.FimdaEstrutura()
#    print PAP.QuantidadedeResiduos()
#    print PAP.Identidade()


#    arquivo = file("/joao/Alpha/src/teste1/build_profile.prf", 'r')
#    profile = []
#    linha = arquivo.readline()
#    while True:    
#        if not linha.startswith("#"):
#            estrutura = estruturaprf(linha)
#            if estrutura.Tipo() != "S":
#                profile.append(estrutura)
#            linha = arquivo.readline()
#            if linha == "":
#                break
#        else:
#            linha = arquivo.readline()
#
#    for  i in range(0, len(profile)):
#        for j in range(i, len(profile)):
#            if profile[i].__str__() < profile[j].__str__():
#                temp = profile[i]
#                profile[i] = profile[j]
#                profile[j] = temp
#            
#            
#    for estrutura in range(1, len(profile)):
#        print profile[estrutura].Nome() + " " + profile[estrutura].Identidade()
