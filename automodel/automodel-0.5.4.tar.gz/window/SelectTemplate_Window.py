import os
import wx
import wx.lib.agw.hyperlink as hl

from wintools.wintools import *
# from loader import *
from modellingfile.leitorprf import *
from modellingfile.seq import *
from modellingfile.fixpdb import *

from network.Clientold import Clientold
class SelectTemplate_Window(subwintools):#Subjanela de escolha de template
    def __init__(self, parent, id, arquivoBuild_ProfileAli):
        wx.Dialog.__init__(self, parent, id, 'Selecting a template protein',  size=(800,665))

        panel = wx.Panel(self, -1,  size=(800,665))
        panel.SetBackgroundColour("LightGray")
        self.statictext = {} #tupla para criacao de labels
        self.TextField = {} #tupla para criacao de campos de texto
        self.button = { } #tupla para a criacao de botoes
        self.profile = []
        self.profilepir = []
        self.createText(panel)
        self.createMuchButtons(panel)
        self.createTextFields(panel)


        texto = ""
        myseq = sequencia(arquivoBuild_ProfileAli, 1)
        for i in range(0, myseq.tamanho()):
                texto = texto + myseq.conteudodasequencia()[i]


        self.TextField["Target Sequence:"].SetValue(texto)
        fonte = wx.Font(9,  wx.MODERN, wx.NORMAL,  True)
        self.TextField["Target Sequence:"].SetFont(fonte)
        self.TextField["Selected Template:"].SetFont(fonte)
        self.Bind(wx.EVT_TEXT,self.OnTextinTemplate, self.TextField["Selected Template:"])
        self.button["Ok"].SetBackgroundColour("yellow")
        self.arquivoBuild_ProfileAli = arquivoBuild_ProfileAli
        self.parent = parent
        self.CreateAlinhamentoData(panel)
        self.RadiosDasEstruturas(panel)
        self.carregarPrimeiroRadio()
        self.result = None
        
        self.clientold = Clientold()

    def RadiosDasEstruturas(self, parent):
        arquivo = file(os.path.dirname(self.arquivoBuild_ProfileAli) + os.sep +"build_profile.prf", 'r')
        linha = arquivo.readline()
        while True:
            if not linha.startswith("#"):
                estrutura = estruturaprf(linha)
                if estrutura.Tipo() != "S":
                    self.profile.append(estrutura)
                linha = arquivo.readline()
                if linha == "":
                    break
            else:
                linha = arquivo.readline()

        for  i in range(0, len(self.profile)):
            for j in range(i, len(self.profile)):
                if self.profile[i].__str__() < self.profile[j].__str__():
                    temp = self.profile[i]
                    self.profile[i] = self.profile[j]
                    self.profile[j] = temp
        posX = 175
        posY = 298
        for estrutura in range(0, len(self.profile)):
            radio = wx.RadioButton(parent, -1, self.profile[estrutura].Nome(), pos = (posX, posY), name = self.profile[estrutura].Nome())
            myUrl = "http://pdb.org/pdb/explore/explore.do?structureId=" +  self.profile[estrutura].Nome()[0:4]
            self.Bind(wx.EVT_RADIOBUTTON,self.EventodosRadiosdeEstruturas, radio)
            myHl = hl.HyperLinkCtrl(parent, -1, "[?]", pos=(posX + 70, posY),
                                  URL=myUrl)
            myHl.SetToolTip(wx.ToolTip("Access on PDB.org"))
            posX = posX +100
            if estrutura == 4:
                posY = posY + 20
                posX = 175
            if estrutura >= 9:
                break
        for estrutura in range(1, len(self.profile)+2):
            self.profilepir.append(sequencia(self.arquivoBuild_ProfileAli,estrutura ))
        #self.TextField["Selected Template:"].SetValue(self.profilepir[1].nome())
    def carregarPrimeiroRadio(self):
                self.TextField["Start"].SetValue(self.profile[0].IniciodaEstrutura())
                self.TextField["End"].SetValue(self.profile[0].FimdaEstrutura())
                self.TextField["Quantity"].SetValue(self.profile[0].QuantidadedeResiduos())
                self.TextField["Identity"].SetValue(self.profile[0].Identidade())
                for estrutura in range(0, len(self.profilepir)):
                    #print self.profilepir[estrutura].nome().rsplit()[0]
                    if self.profilepir[estrutura].nome().rsplit()[0] == self.profile[0].Nome():
                        texto = ""
                        for i in range(0, self.profilepir[estrutura].tamanho()):
                           texto = texto + self.profilepir[estrutura].conteudodasequencia()[i]
                        self.TextField["Selected Template:"].SetValue(texto)
                        break
    def EventodosRadiosdeEstruturas(self, event):
        radioselecionado = event.GetEventObject()
        radioselecionado = radioselecionado.GetLabel()
        for inc in range(0, len(self.profile)):
            if radioselecionado == self.profile[inc].Nome():
                self.TextField["Start"].SetValue(self.profile[inc].IniciodaEstrutura())
                self.TextField["End"].SetValue(self.profile[inc].FimdaEstrutura())
                self.TextField["Quantity"].SetValue(self.profile[inc].QuantidadedeResiduos())
                self.TextField["Identity"].SetValue(self.profile[inc].Identidade())
                #print len(self.profilepir)
                for estrutura in range(0, len(self.profilepir)):
                    #print self.profilepir[estrutura].nome().rsplit()[0]
                    if self.profilepir[estrutura].nome().rsplit()[0] == radioselecionado:
                        texto = ""
                        for i in range(0, self.profilepir[estrutura].tamanho()):
                           texto = texto + self.profilepir[estrutura].conteudodasequencia()[i]
                        self.TextField["Selected Template:"].SetValue(texto)
                break
            else:
                pass
    def textData(self): #labels
        return(("Select below a protein that is used as a template:", (20, 20)),)

    def textFieldData(self): #campo de dados
        return(("Target Sequence:", (30, 40)),
                        ("Selected Template:", (30,350)))
    def alinhamentoData(self):
      return(["Start","End", "Quantity", "Identity"])

    def CreateAlinhamentoData(self,panel):
      posicaoY = 395
      posicaoX = 50
      for cadaParameto in self.alinhamentoData():
        static = wx.StaticText(panel, wx.NewId(), cadaParameto, pos=(posicaoX,posicaoY))
        self.TextField[cadaParameto] = wx.TextCtrl(panel, wx.NewId(), "", size=(40,30), pos=(posicaoX,posicaoY+18))
        posicaoY = posicaoY + 55
      wx.StaticBox(panel,  -1, "Alignment", (35, 375), (95, posicaoY-375))
      wx.StaticText(panel, wx.NewId(), "%", pos=(93, 585))
    def buttonData(self): #botoes
        return(("Ok",self.Alinhar, (520,610)),
                    ("Cancel",self.OnCloseWindow, (420,610)),
                    ("PIR Alignment",self.OnButtonOpenAli,(290,610)),
                    ("PAP Alignment ",self.OnButtonOpenPAP,(160,610)))

    def Alinhar(self,event):
        texto1 = self.TextField["Target Sequence:"].GetValue()
        texto2 = self.TextField["Selected Template:"].GetValue()
        self.result = [texto1,texto2]
        self.Destroy()
#    def __del__(self):
#        return self.result
##        super.__del__()
#    def __str__(self):
#        return self.result
    def out(self):
        return self.result

    def OnButtonOpenAli(self, event): #Botoes de abertura de arquivos de textos
        try:
          self.clientold.open_txt_file(self.arquivoBuild_ProfileAli)
        except Exception, e:
          self.choose_text_editor(self.arquivoBuild_ProfileAli)

    def OnButtonOpenPAP(self, event): #Botoes de abertura de arquivos de textos
        arquivoPAP = os.path.dirname(self.arquivoBuild_ProfileAli) + os.sep +'build_profilePAP.ali'
        try:
          self.clientold.open_txt_file(arquivoPAP)
        except Exception, e:
          self.choose_text_editor(arquivoPAP)

    def OnTextinTemplate(self, event): #Verifica sem tem algum texto no campo Sequencia
        if(self.TextField["Selected Template:"].GetValue() != ""):
         self.button["Ok"].SetBackgroundColour("green")
        else:
         self.button["Ok"].SetBackgroundColour("yellow")


# if __name__ == '__main__':
    # app = wx.PySimpleApp()
    # arquivo = 'c:' + os.sep + 'build_profilePIR.ali'
    # frame = Automodel2(None,-1, arquivo)

    # frame.ShowModal()
   # app.MainLoop()


