# -*- coding: iso-8859-1 -*-
import re

class sequencia():
    def __init__(self, arquivo, sequencianumero):
        self.sequencia = []
        self.abrir(arquivo, sequencianumero)
    def abrir(self, arquivo, sequencianumero):
        arquivo = file(arquivo, "r")
        contador = 0
        linha = ""
        while (contador < sequencianumero):
            linha = arquivo.readline()
            if linha.startswith(">P1;"):
                contador = contador+1
            #print linha
        self.sequencia.append(linha)
        while True:
            linha = arquivo.readline()
            self.sequencia.append(linha)
            if self.ehfimdasequencia(linha):
                break
    def ehfimdasequencia(self, linha):
        return("*" in linha)
    def conteudodasequencia(self):
        return(self.sequencia)
    def tamanho(self):
        return(len(self.sequencia))
    def cadeia(self):
        if "CHAIN" in self.sequencia[1]:
            linha2 = filter(None,  re.split(";",  self.sequencia[1]))
            return linha2[2].split()[-1]
        else:
            return("A")
    def nome(self):
        nome = filter(None,  re.split(";",  self.sequencia[0])[-1])
        return(nome[0:-1])
    def nomecomheteroatomo(self):
        return(filter(None,  re.split(";",  self.sequencia[0])[-1]))
    def heteroatomos(self):
        cadeiasencontradas = []
        for linha in range(2, self.tamanho()):
            for cadaletra in range(0, len(self.sequencia[linha])):
                if((self.sequencia[linha][cadaletra].islower() or self.sequencia[linha][cadaletra].isdigit() or not self.sequencia[linha][cadaletra].isalnum() ) and not ( self.sequencia[linha][cadaletra] in ["-","*",'\n',':'] or self.sequencia[linha][cadaletra] in cadeiasencontradas)):
                    cadeiasencontradas.append(self.sequencia[linha][cadaletra])
        return(cadeiasencontradas)

    def mudarheteroatomo(self, heteroatomooriginal,  novoheteroatomo):
        #novalinha = ""
        for cadalinha in range(2, self.tamanho()):
            novalinha = ""
            if heteroatomooriginal in self.sequencia[cadalinha]:
                for cadaletra in range(0, len(self.sequencia[cadalinha])):
                    if self.sequencia[cadalinha][cadaletra] != heteroatomooriginal:
                        novalinha = novalinha + self.sequencia[cadalinha][cadaletra]
                    else:
                        novalinha = novalinha + novoheteroatomo
                self.sequencia[cadalinha] = novalinha

    def conteudocompletodasequencia(self):
        pass

#testes

# a = sequencia("tests/models/seq.ali",1 )
# for i in range(0, a.tamanho()):
#     print a.conteudodasequencia()[2][0:len(a.conteudodasequencia()[2])-1] + "/" + a.conteudodasequencia()[2]
#     print "cadeia: " + a.cadeia()
#     print "Nome: " + a.nome()
#     print "Heteroatomos: " + str(a.heteroatomos())
#     a.mudarheteroatomo("w", "^")
#     print a.heteroatomos()
# for i in range(0, a.tamanho()):
#    print a.conteudodasequencia()[i]

