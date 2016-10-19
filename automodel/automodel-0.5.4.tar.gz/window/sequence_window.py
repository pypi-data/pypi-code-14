#Boa:MiniFrame:MiniFrame1

import wx
import wx.richtext
#from loader import *
import os
import tempfile

def create(parent):
    return MiniFrame1(parent)

[wxID_MINIFRAME1, wxID_MINIFRAME1BUTTON1, wxID_MINIFRAME1BUTTON2,
 wxID_MINIFRAME1BUTTON3, wxID_MINIFRAME1RICHTEXTCTRL1,
 wxID_MINIFRAME1STATICTEXT1,
] = [wx.NewId() for _init_ctrls in range(6)]

class MiniFrame1(wx.MiniFrame):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.MiniFrame.__init__(self, id=wxID_MINIFRAME1, name='', parent=prnt,
              pos=wx.Point(261, 262), size=wx.Size(776, 480),
              style=wx.DEFAULT_FRAME_STYLE, title='Load Target Sequence')
        self.SetClientSize(wx.Size(776, 480))

        self.staticText1 = wx.StaticText(id=wxID_MINIFRAME1STATICTEXT1,
              label=u'Enter in the below camp the protein sequence (target sequence) that you wants to model',
              name='staticText1', parent=self, pos=wx.Point(40, 40),
              size=wx.Size(601, 15), style=0)

        self.button1 = wx.Button(id=wxID_MINIFRAME1BUTTON1, label=u'Save',
              name='button1', parent=self, pos=wx.Point(480, 400),
              size=wx.Size(85, 28), style=0)
        self.button1.Bind(wx.EVT_BUTTON, self.OnSalvarButton,
              id=wxID_MINIFRAME1BUTTON1)

        self.button2 = wx.Button(id=wxID_MINIFRAME1BUTTON2, label=u'Cancel',
              name='button2', parent=self, pos=wx.Point(336, 400),
              size=wx.Size(85, 28), style=0)
        self.button2.Bind(wx.EVT_BUTTON, self.OnCancelarButton,
              id=wxID_MINIFRAME1BUTTON2)

        self.button3 = wx.Button(id=wxID_MINIFRAME1BUTTON3, label=u'Clear',
              name='button3', parent=self, pos=wx.Point(192, 400),
              size=wx.Size(85, 28), style=0)
        self.button3.Bind(wx.EVT_BUTTON, self.OnLimparButton,
              id=wxID_MINIFRAME1BUTTON3)

        self.richTextCtrl1 = wx.richtext.RichTextCtrl(id=wxID_MINIFRAME1RICHTEXTCTRL1,
              parent=self, pos=wx.Point(32, 64), size=wx.Size(712, 224),
              style=wx.richtext.RE_MULTILINE, value=u'')
        self.richTextCtrl1.SetLabel(u'')

    def __init__(self, parent):
        self._init_ctrls(parent)
        self.parent = parent

    def OnLimparButton(self, event):
        self.richTextCtrl1.SetValue("")

    def OnSalvarButton(self, event):
		texto = self.richTextCtrl1.GetValue()
		pir = self.makefasta(texto)
		arquivo = self.buildfile(pir)
# self.parent.send_fasta_file(arquivo)
		self.fasta_filename = arquivo
		self.parent.OnButton2ButtonDone(arquivo)
		self.Destroy()

    def OnCancelarButton(self, event):
        self.Destroy()

    def makefasta(self,texto): #retorna, uma sequencia fasta ou somente cadeia, em formato PIR
		if texto.startswith('>'):
		    texto = texto.partition('\n')[2]
		retorno ='>seq.ali\n' + texto
		return(retorno)

    def buildfile(self,conteudo):
		arquivo = tempfile.mktemp()
		arq = file(arquivo, 'w')
		arq.write(conteudo)
		arq.close()
#		print arquivo
		return(arquivo)
#        if self.richTextCtrl1.GetValue() != "":
#            if getModellerPid() == 0:
#                #event.Skip()
#                texto =  self.richTextCtrl1.GetValue()
#                pir = makepir(texto)
#                self.parent.file = buildfile(pir)
#                self.parent.pasta = os.path.dirname(self.parent.file)
#                self.parent.PrepararDepoisdeLer(self.parent.file)
#                self.Destroy()
#            elif self.parent.FinalizarModeller():
#                #event.Skip()
#                texto =  self.richTextCtrl1.GetValue()
#                pir = makepir(texto)
#                self.parent.file = buildfile(pir)
#                self.parent.pasta = os.path.dirname(self.parent.file)
#                self.parent.PrepararDepoisdeLer(self.parent.file)
#                self.Destroy()
#
#        else:
#            dlg = wx.MessageBox("Nao foi digitado nada", caption="Alpha", style=wx.OK)

#parent = wx.App()
#main = MiniFrame1(parent,"/tmp")
#main.Show()

