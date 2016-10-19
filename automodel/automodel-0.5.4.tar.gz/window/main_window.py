#Boa:Frame:Frame1

import wx
import wx.lib.hyperlink
import wx.animate
from wx.lib.pubsub import Publisher
import os
import thread
import socket
from window.change_het_window import ChangeHetWindow
# from window.sequence_window import sequence_window
from window.SelectAutoModelMode import SelectAutoModelMode
from window.automatic_align_window import alinhar_sequencia_sem_buscar_template as align_window
from window.automatic_modeling_window import modelar_sem_alinhar as modeling_window
from window.loop_window import *
from window.sequence_window import MiniFrame1 as MiniFrame1 
from window.AlterarCadeiasEHeteroatomos import  AlterarCadeiasEHeteroatomos
from window.SelectTemplate_Window import SelectTemplate_Window
from window.AboutAutoModel import AboutAutoModel
from network.Clientold import Clientold
# from network.client import Client
from modellingstep.PrepareBeforeStartModelling import PrepareBeforeStartModelling
from modellingstep.FindTemplatesStep import FindTemplatesStep
from modellingstep.AlignStep import AlignStep
from modellingstep.ModelStep import ModelStep
from modellingstep.EvaluateStep import EvaluateStep
from modellingstep.EvaluateProcheckStep import EvaluateProcheckStep
from modellingstep.LoopModelStep import LoopModelStep
from modellingstep.EvaluateAfterLoopRefinamentStep import EvaluateAfterLoopRefinamentStep
from automodelexception.automodel_error import AutoModelError
from options.Prefs import Prefs

from window.TextEditorWindow import TextEditor as TextEditorWindow
from window.ImageViewerWindow import ImageViewer as ImageViewerWindow

log_error = []
def create(parent):
    return Frame1(parent)

[wxID_FRAME1, wxID_FRAME1ABOUTAUTOMODELLINK, wxID_FRAME1ABRIRPASTABUTTON, 
 wxID_FRAME1ALINHAR, wxID_FRAME1BOTAOABRIRARQUIVOFASTA, 
 wxID_FRAME1BOTAOABRIRDOALINHAMENTOFINALPAP, 
 wxID_FRAME1BOTAOABRIRDOALINHAMENTOFINALPIR, 
 wxID_FRAME1BOTAOABRIRDOALINHARPDB, wxID_FRAME1BOTAOABRIRDOARQUIVOINICIAL, 
 wxID_FRAME1BOTAOABRIRDOCARREGARPAP, wxID_FRAME1BOTAOABRIRDOCARREGARPIR, 
 wxID_FRAME1BOTAOABRIRDOCARREGARPRF, 
 wxID_FRAME1BOTAOABRIRDOMODELARALINHAMENTOPAP, 
 wxID_FRAME1BOTAOABRIRDOMODELARALINHAMENTOPIR, 
 wxID_FRAME1BOTAOABRIRDOMODELARPDB, wxID_FRAME1BOTAOABRIRDOMODELARRESULTADO, 
 wxID_FRAME1BOTAOABRIRDOSCOREDOPE, wxID_FRAME1BUSCARTEMPLATE, 
 wxID_FRAME1BUTTON2, wxID_FRAME1CAPTURAR_ARQUIVOS_PARA_ALINHAR, 
 wxID_FRAME1CAPTURAR_ARQUIVOS_PARA_MODELAGEM, wxID_FRAME1COMPARARMODELOS, 
 wxID_FRAME1EDITDOALINHAMENTOFINALPAP, wxID_FRAME1EDITDOALINHAMENTOFINALPIR, 
 wxID_FRAME1EDITDOALINHARPDB, wxID_FRAME1EDITDOARQUIVOINICIAL, 
 wxID_FRAME1EDITDOCAMINHOARQUIVOFASTA, wxID_FRAME1EDITDOCARREGARPAP, 
 wxID_FRAME1EDITDOCARREGARPIR, wxID_FRAME1EDITDOCARREGARPRF, 
 wxID_FRAME1EDITDOMODELARALINHAMENTOPAP, 
 wxID_FRAME1EDITDOMODELARALINHAMENTOPIR, wxID_FRAME1EDITDOMODELARPDB, 
 wxID_FRAME1EDITDOMODELARRESULTADO, wxID_FRAME1EDITDOSCOREDOPE, 
 wxID_FRAME1ESCOLHERUMPDB, wxID_FRAME1FIGURADETRABALHANDO, 
 wxID_FRAME1MANUALAUTOMODELLINK, wxID_FRAME1MODELAR, 
 wxID_FRAME1MODIFICARTEMPLATE, wxID_FRAME1MUDARHETEROATOMO, 
 wxID_FRAME1PROCHECK, wxID_FRAME1REFINARLOOPS, wxID_FRAME1RESETBUTTON, 
 wxID_FRAME1SALVARRESULTADOS, wxID_FRAME1SCROLLEDWINDOW1, 
 wxID_FRAME1STATICBOX1, wxID_FRAME1STATICBOX10, wxID_FRAME1STATICBOX11, 
 wxID_FRAME1STATICBOX2, wxID_FRAME1STATICBOX3, wxID_FRAME1STATICBOX4, 
 wxID_FRAME1STATICBOX5, wxID_FRAME1STATICBOX6, wxID_FRAME1STATICBOX7, 
 wxID_FRAME1STATICBOX8, wxID_FRAME1STATICBOX9, wxID_FRAME1STATICTEXT1, 
 wxID_FRAME1STATICTEXT11, wxID_FRAME1STATICTEXT12, wxID_FRAME1STATICTEXT13, 
 wxID_FRAME1STATICTEXT14, wxID_FRAME1STATICTEXT2, wxID_FRAME1STATICTEXT3, 
 wxID_FRAME1STATICTEXT4, wxID_FRAME1STATICTEXT5, wxID_FRAME1STATICTEXT6, 
 wxID_FRAME1STATICTEXT7, wxID_FRAME1STATICTEXT8, wxID_FRAME1STATICTEXT9, 
 wxID_FRAME1VERSAOPARATESTE, 
] = [wx.NewId() for _init_ctrls in range(71)]

[wxID_FRAME1TIMER1, wxID_FRAME1TIMER2, 
] = [wx.NewId() for _init_utils in range(2)]

class Frame1(wx.Frame):
    def _init_utils(self):
        # generated method, don't edit
        self.timer1 = wx.Timer(id=wxID_FRAME1TIMER1, owner=self)

        self.timer2 = wx.Timer(id=wxID_FRAME1TIMER2, owner=self)

    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Frame.__init__(self, id=wxID_FRAME1, name='', parent=prnt,
              pos=wx.Point(168, 62), size=wx.Size(963, 674),
              style=wx.DEFAULT_FRAME_STYLE, title='AutoModel')
        self._init_utils()
        self.SetClientSize(wx.Size(963, 674))

        self.scrolledWindow1 = wx.ScrolledWindow(id=wxID_FRAME1SCROLLEDWINDOW1,
              name='scrolledWindow1', parent=self, pos=wx.Point(0, 0),
              size=wx.Size(963, 674), style=wx.HSCROLL | wx.VSCROLL)
        self.scrolledWindow1.SetThemeEnabled(True)
        self.scrolledWindow1.SetAutoLayout(False)
        self.scrolledWindow1.Enable(True)
        self.scrolledWindow1.SetLabel(u'')

        self.staticBox1 = wx.StaticBox(id=wxID_FRAME1STATICBOX1,
              label=u'Select Target Sequence', name='staticBox1',
              parent=self.scrolledWindow1, pos=wx.Point(16, 24),
              size=wx.Size(440, 96), style=0)

        self.staticText1 = wx.StaticText(id=wxID_FRAME1STATICTEXT1,
              label=u'From\nFasta File', name='staticText1',
              parent=self.scrolledWindow1, pos=wx.Point(24, 48),
              size=wx.Size(100, 32), style=0)

        self.EditdoCaminhoArquivoFasta = wx.TextCtrl(id=wxID_FRAME1EDITDOCAMINHOARQUIVOFASTA,
              name=u'EditdoCaminhoArquivoFasta', parent=self.scrolledWindow1,
              pos=wx.Point(120, 48), size=wx.Size(240, 24), style=0, value=u'')
        self.EditdoCaminhoArquivoFasta.Enable(True)
        self.EditdoCaminhoArquivoFasta.SetEditable(False)

        self.BotaoAbrirArquivoFasta = wx.Button(id=wxID_FRAME1BOTAOABRIRARQUIVOFASTA,
              label=u'Open', name=u'BotaoAbrirArquivoFasta',
              parent=self.scrolledWindow1, pos=wx.Point(368, 48),
              size=wx.Size(80, 24), style=0)
        self.BotaoAbrirArquivoFasta.Bind(wx.EVT_BUTTON,
              self.OnBotaoAbrirArquivoFasta,
              id=wxID_FRAME1BOTAOABRIRARQUIVOFASTA)

        self.button2 = wx.Button(id=wxID_FRAME1BUTTON2,
              label=u'Enter the sequence manually', name='button2',
              parent=self.scrolledWindow1, pos=wx.Point(128, 80),
              size=wx.Size(224, 32), style=0)
        self.button2.SetAutoLayout(True)
        self.button2.Bind(wx.EVT_BUTTON, self.OnButton2Button,
              id=wxID_FRAME1BUTTON2)

        self.staticBox2 = wx.StaticBox(id=wxID_FRAME1STATICBOX2, label=u'',
              name='staticBox2', parent=self.scrolledWindow1, pos=wx.Point(464,
              24), size=wx.Size(476, 196), style=0)
        self.staticBox2.SetAutoLayout(False)

        self.staticText2 = wx.StaticText(id=wxID_FRAME1STATICTEXT2,
              label=u'Preliminary\nAlignment (PIR)', name='staticText2',
              parent=self.scrolledWindow1, pos=wx.Point(472, 48),
              size=wx.Size(182, 32), style=0)

        self.EditdoCarregarPIR = wx.TextCtrl(id=wxID_FRAME1EDITDOCARREGARPIR,
              name=u'EditdoCarregarPIR', parent=self.scrolledWindow1,
              pos=wx.Point(584, 56), size=wx.Size(256, 24), style=0, value=u'')
        self.EditdoCarregarPIR.SetEditable(False)

        self.BotaoAbrirdoCarregarPIR = wx.Button(id=wxID_FRAME1BOTAOABRIRDOCARREGARPIR,
              label=u'Open', name=u'BotaoAbrirdoCarregarPIR',
              parent=self.scrolledWindow1, pos=wx.Point(848, 56),
              size=wx.Size(80, 24), style=0)
        self.BotaoAbrirdoCarregarPIR.Enable(False)
        self.BotaoAbrirdoCarregarPIR.Bind(wx.EVT_BUTTON,
              self.Action_of_Abrir_Buttons,
              id=wxID_FRAME1BOTAOABRIRDOCARREGARPIR)

        self.BotaoAbrirdoCarregarPAP = wx.Button(id=wxID_FRAME1BOTAOABRIRDOCARREGARPAP,
              label=u'Open', name=u'BotaoAbrirdoCarregarPAP',
              parent=self.scrolledWindow1, pos=wx.Point(848, 101),
              size=wx.Size(80, 24), style=0)
        self.BotaoAbrirdoCarregarPAP.Enable(False)
        self.BotaoAbrirdoCarregarPAP.Bind(wx.EVT_BUTTON,
              self.Action_of_Abrir_Buttons,
              id=wxID_FRAME1BOTAOABRIRDOCARREGARPAP)

        self.staticText3 = wx.StaticText(id=wxID_FRAME1STATICTEXT3,
              label=u'Preliminary\nAlignment (PAP):', name='staticText3',
              parent=self.scrolledWindow1, pos=wx.Point(472, 93),
              size=wx.Size(189, 32), style=0)

        self.staticText4 = wx.StaticText(id=wxID_FRAME1STATICTEXT4,
              label=u'Preliminary\nAlignment (PRF):', name='staticText4',
              parent=self.scrolledWindow1, pos=wx.Point(472, 137),
              size=wx.Size(120, 39), style=0)

        self.EditdoCarregarPAP = wx.TextCtrl(id=wxID_FRAME1EDITDOCARREGARPAP,
              name=u'EditdoCarregarPAP', parent=self.scrolledWindow1,
              pos=wx.Point(584, 101), size=wx.Size(256, 24), style=0,
              value=u'')
        self.EditdoCarregarPAP.SetEditable(False)

        self.BotaoAbrirdoCarregarPRF = wx.Button(id=wxID_FRAME1BOTAOABRIRDOCARREGARPRF,
              label=u'Open', name=u'BotaoAbrirdoCarregarPRF',
              parent=self.scrolledWindow1, pos=wx.Point(848, 141),
              size=wx.Size(80, 24), style=0)
        self.BotaoAbrirdoCarregarPRF.Enable(False)
        self.BotaoAbrirdoCarregarPRF.Bind(wx.EVT_BUTTON,
              self.Action_of_Abrir_Buttons,
              id=wxID_FRAME1BOTAOABRIRDOCARREGARPRF)

        self.BuscarTemplate = wx.Button(id=wxID_FRAME1BUSCARTEMPLATE,
              label=u'   From\nDatabase', name=u'BuscarTemplate',
              parent=self.scrolledWindow1, pos=wx.Point(72, 139),
              size=wx.Size(104, 72), style=0)
        self.BuscarTemplate.SetAutoLayout(False)
        self.BuscarTemplate.Enable(False)
        self.BuscarTemplate.Bind(wx.EVT_BUTTON, self.OnCarregarButton,
              id=wxID_FRAME1BUSCARTEMPLATE)

        self.staticBox3 = wx.StaticBox(id=wxID_FRAME1STATICBOX3,
              label=u'Model Evaluation', name='staticBox3',
              parent=self.scrolledWindow1, pos=wx.Point(8, 549),
              size=wx.Size(688, 104), style=0)

        self.staticBox4 = wx.StaticBox(id=wxID_FRAME1STATICBOX4,
              label=u'Loading Target Sequence and Template Selection',
              name='staticBox4', parent=self.scrolledWindow1, pos=wx.Point(8,
              8), size=wx.Size(944, 224), style=0)

        self.staticText6 = wx.StaticText(id=wxID_FRAME1STATICTEXT6,
              label=u'Template Selected (PDB):', name='staticText6',
              parent=self.scrolledWindow1, pos=wx.Point(352, 383),
              size=wx.Size(183, 17), style=0)

        self.staticText7 = wx.StaticText(id=wxID_FRAME1STATICTEXT7,
              label=u'Template Selected (PDB):', name='staticText7',
              parent=self.scrolledWindow1, pos=wx.Point(360, 256),
              size=wx.Size(168, 32), style=0)

        self.staticText8 = wx.StaticText(id=wxID_FRAME1STATICTEXT8,
              label=u'Alingment (PIR):', name='staticText8',
              parent=self.scrolledWindow1, pos=wx.Point(384, 426),
              size=wx.Size(148, 17), style=0)

        # self.staticText9 = wx.StaticText(id=wxID_FRAME1STATICTEXT9,
        #       label=u'Alingnment (PAP):', name='staticText9',
        #       parent=self.scrolledWindow1, pos=wx.Point(384, 468),
        #       size=wx.Size(153, 17), style=0)

        self.EditdoAlinharPDB = wx.TextCtrl(id=wxID_FRAME1EDITDOALINHARPDB,
              name=u'EditdoAlinharPDB', parent=self.scrolledWindow1,
              pos=wx.Point(584, 184), size=wx.Size(254, 24), style=0,
              value=u'')
        self.EditdoAlinharPDB.SetEditable(False)

        self.EditdoArquivoInicial = wx.TextCtrl(id=wxID_FRAME1EDITDOARQUIVOINICIAL,
              name=u'EditdoArquivoInicial', parent=self.scrolledWindow1,
              pos=wx.Point(536, 250), size=wx.Size(256, 24), style=0,
              value=u'')
        self.EditdoArquivoInicial.SetEditable(False)

        self.EditdoCarregarPRF = wx.TextCtrl(id=wxID_FRAME1EDITDOCARREGARPRF,
              name=u'EditdoCarregarPRF', parent=self.scrolledWindow1,
              pos=wx.Point(584, 141), size=wx.Size(256, 24), style=0,
              value=u'')
        self.EditdoCarregarPRF.SetEditable(False)

        self.EditdoAlinhamentoFinalPIR = wx.TextCtrl(id=wxID_FRAME1EDITDOALINHAMENTOFINALPIR,
              name=u'EditdoAlinhamentoFinalPIR', parent=self.scrolledWindow1,
              pos=wx.Point(536, 288), size=wx.Size(256, 24), style=0,
              value=u'')
        self.EditdoAlinhamentoFinalPIR.SetEditable(False)

        # self.EditdoAlinhamentoFinalPAP = wx.TextCtrl(id=wxID_FRAME1EDITDOALINHAMENTOFINALPAP,
        #       name=u'EditdoAlinhamentoFinalPAP', parent=self.scrolledWindow1,
        #       pos=wx.Point(536, 328), size=wx.Size(256, 24), style=0,
        #       value=u'')
        # self.EditdoAlinhamentoFinalPAP.SetEditable(False)

        self.BotaoAbrirdoAlinharPDB = wx.Button(id=wxID_FRAME1BOTAOABRIRDOALINHARPDB,
              label=u'Open', name=u'BotaoAbrirdoAlinharPDB',
              parent=self.scrolledWindow1, pos=wx.Point(848, 184),
              size=wx.Size(80, 24), style=0)
        self.BotaoAbrirdoAlinharPDB.Enable(False)
        self.BotaoAbrirdoAlinharPDB.Bind(wx.EVT_BUTTON,
              self.Action_of_Abrir_Buttons,
              id=wxID_FRAME1BOTAOABRIRDOALINHARPDB)

        self.staticBox6 = wx.StaticBox(id=wxID_FRAME1STATICBOX6,
              label=u'Alignment', name='staticBox6',
              parent=self.scrolledWindow1, pos=wx.Point(8, 232),
              size=wx.Size(944, 136), style=0)

        self.BotaoAbrirdoArquivoInicial = wx.Button(id=wxID_FRAME1BOTAOABRIRDOARQUIVOINICIAL,
              label=u'Open', name=u'BotaoAbrirdoArquivoInicial',
              parent=self.scrolledWindow1, pos=wx.Point(816, 248),
              size=wx.Size(80, 24), style=0)
        self.BotaoAbrirdoArquivoInicial.Enable(False)
        self.BotaoAbrirdoArquivoInicial.Bind(wx.EVT_BUTTON,
              self.Action_of_Abrir_Buttons,
              id=wxID_FRAME1BOTAOABRIRDOARQUIVOINICIAL)

        self.BotaoAbrirdoAlinhamentoFinalPIR = wx.Button(id=wxID_FRAME1BOTAOABRIRDOALINHAMENTOFINALPIR,
              label=u'Open', name=u'BotaoAbrirdoAlinhamentoFinalPIR',
              parent=self.scrolledWindow1, pos=wx.Point(817, 288),
              size=wx.Size(80, 24), style=0)
        self.BotaoAbrirdoAlinhamentoFinalPIR.Enable(False)
        self.BotaoAbrirdoAlinhamentoFinalPIR.Bind(wx.EVT_BUTTON,
              self.Action_of_Abrir_Buttons,
              id=wxID_FRAME1BOTAOABRIRDOALINHAMENTOFINALPIR)

        # self.BotaoAbrirdoAlinhamentoFinalPAP = wx.Button(id=wxID_FRAME1BOTAOABRIRDOALINHAMENTOFINALPAP,
        #       label=u'Open', name=u'BotaoAbrirdoAlinhamentoFinalPAP',
        #       parent=self.scrolledWindow1, pos=wx.Point(816, 328),
        #       size=wx.Size(80, 24), style=0)
        # self.BotaoAbrirdoAlinhamentoFinalPAP.Enable(False)
        # self.BotaoAbrirdoAlinhamentoFinalPAP.Bind(wx.EVT_BUTTON,
        #       self.Action_of_Abrir_Buttons,
        #       id=wxID_FRAME1BOTAOABRIRDOALINHAMENTOFINALPAP)

        self.ModificarTemplate = wx.Button(id=wxID_FRAME1MODIFICARTEMPLATE,
              label=u'Edit Template', name=u'ModificarTemplate',
              parent=self.scrolledWindow1, pos=wx.Point(132, 269),
              size=wx.Size(104, 72), style=0)
        self.ModificarTemplate.SetAutoLayout(False)
        self.ModificarTemplate.Enable(False)
        self.ModificarTemplate.Bind(wx.EVT_BUTTON,
              self.OnModificarTemplateButton, id=wxID_FRAME1MODIFICARTEMPLATE)

        self.Alinhar = wx.Button(id=wxID_FRAME1ALINHAR, label=u'Align',
              name=u'Alinhar', parent=self.scrolledWindow1, pos=wx.Point(240,
              269), size=wx.Size(104, 72), style=0)
        self.Alinhar.SetAutoLayout(False)
        self.Alinhar.Enable(False)
        self.Alinhar.Bind(wx.EVT_BUTTON, self.OnAlinharButton,
              id=wxID_FRAME1ALINHAR)

        self.Modelar = wx.Button(id=wxID_FRAME1MODELAR, label=u'Model',
              name=u'Modelar', parent=self.scrolledWindow1, pos=wx.Point(235,
              383), size=wx.Size(104, 72), style=0)
        self.Modelar.Enable(False)
        self.Modelar.Bind(wx.EVT_BUTTON, self.OnModelarButton,
              id=wxID_FRAME1MODELAR)

        self.MudarHeteroatomo = wx.Button(id=wxID_FRAME1MUDARHETEROATOMO,
              label=u'      Change\n Heteroatoms', name=u'MudarHeteroatomo',
              parent=self.scrolledWindow1, pos=wx.Point(128, 383),
              size=wx.Size(104, 72), style=0)
        self.MudarHeteroatomo.Enable(False)
        self.MudarHeteroatomo.Bind(wx.EVT_BUTTON, self.OnMudarHeteroatomoButton,
              id=wxID_FRAME1MUDARHETEROATOMO)

        self.EditdoModelarPDB = wx.TextCtrl(id=wxID_FRAME1EDITDOMODELARPDB,
              name=u'EditdoModelarPDB', parent=self.scrolledWindow1,
              pos=wx.Point(536, 383), size=wx.Size(256, 24), style=0,
              value=u'')
        self.EditdoModelarPDB.SetEditable(False)

        self.EditdoModelarAlinhamentoPIR = wx.TextCtrl(id=wxID_FRAME1EDITDOMODELARALINHAMENTOPIR,
              name=u'EditdoModelarAlinhamentoPIR', parent=self.scrolledWindow1,
              pos=wx.Point(536, 426), size=wx.Size(256, 24), style=0,
              value=u'')
        self.EditdoModelarAlinhamentoPIR.SetEditable(False)

        # self.EditdoModelarAlinhamentoPAP = wx.TextCtrl(id=wxID_FRAME1EDITDOMODELARALINHAMENTOPAP,
        #       name=u'EditdoModelarAlinhamentoPAP', parent=self.scrolledWindow1,
        #       pos=wx.Point(536, 468), size=wx.Size(256, 24), style=0,
        #       value=u'')
        # self.EditdoModelarAlinhamentoPAP.SetEditable(False)

        self.SalvarResultados = wx.Button(id=wxID_FRAME1SALVARRESULTADOS,
              label=u'Save Results', name=u'SalvarResultados',
              parent=self.scrolledWindow1, pos=wx.Point(236, 464),
              size=wx.Size(104, 72), style=0)
        self.SalvarResultados.Enable(False)
        self.SalvarResultados.Bind(wx.EVT_BUTTON, self.OnSalvarResultadosButton,
              id=wxID_FRAME1SALVARRESULTADOS)

        self.BotaoAbrirdoModelarPDB = wx.Button(id=wxID_FRAME1BOTAOABRIRDOMODELARPDB,
              label=u'Open', name=u'BotaoAbrirdoModelarPDB',
              parent=self.scrolledWindow1, pos=wx.Point(816, 383),
              size=wx.Size(80, 24), style=0)
        self.BotaoAbrirdoModelarPDB.Enable(False)
        self.BotaoAbrirdoModelarPDB.Bind(wx.EVT_BUTTON,
              self.Action_of_Abrir_Buttons,
              id=wxID_FRAME1BOTAOABRIRDOMODELARPDB)

        self.BotaoAbrirdoModelarAlinhamentoPIR = wx.Button(id=wxID_FRAME1BOTAOABRIRDOMODELARALINHAMENTOPIR,
              label=u'Open', name=u'BotaoAbrirdoModelarAlinhamentoPIR',
              parent=self.scrolledWindow1, pos=wx.Point(816, 426),
              size=wx.Size(80, 24), style=0)
        self.BotaoAbrirdoModelarAlinhamentoPIR.Enable(False)
        self.BotaoAbrirdoModelarAlinhamentoPIR.Bind(wx.EVT_BUTTON,
              self.Action_of_Abrir_Buttons,
              id=wxID_FRAME1BOTAOABRIRDOMODELARALINHAMENTOPIR)

        self.staticText11 = wx.StaticText(id=wxID_FRAME1STATICTEXT11,
              label=u'Template\nSelected (PDB):', name='staticText11',
              parent=self.scrolledWindow1, pos=wx.Point(472, 176),
              size=wx.Size(162, 48), style=0)

        self.staticText14 = wx.StaticText(id=wxID_FRAME1STATICTEXT14,
              label=u'Alignment (PIR):', name='staticText14',
              parent=self.scrolledWindow1, pos=wx.Point(392, 288),
              size=wx.Size(156, 32), style=0)

        # self.staticText13 = wx.StaticText(id=wxID_FRAME1STATICTEXT13,
        #       label=u'Alignment (PAP):', name='staticText13',
        #       parent=self.scrolledWindow1, pos=wx.Point(392, 328),
        #       size=wx.Size(156, 40), style=0)

        self.staticBox5 = wx.StaticBox(id=wxID_FRAME1STATICBOX5,
              label=u'Select Template', name='staticBox5',
              parent=self.scrolledWindow1, pos=wx.Point(16, 120),
              size=wx.Size(440, 100), style=0)

        self.FiguradeTrabalhando = wx.animate.GIFAnimationCtrl(filename='ampulheta.gif',
              id=wxID_FRAME1FIGURADETRABALHANDO, name=u'FiguradeTrabalhando',
              parent=self.scrolledWindow1, pos=wx.Point(888, 564),
              size=wx.Size(100, 100),
              style=wx.animate.AN_FIT_ANIMATION|wx.NO_BORDER)

        self.EscolherUmPDB = wx.Button(id=wxID_FRAME1ESCOLHERUMPDB,
              label=u'From PDB File', name=u'EscolherUmPDB',
              parent=self.scrolledWindow1, pos=wx.Point(296, 139),
              size=wx.Size(104, 72), style=0)
        self.EscolherUmPDB.SetAutoLayout(False)
        self.EscolherUmPDB.Enable(False)
        self.EscolherUmPDB.Bind(wx.EVT_BUTTON, self.OnEscolherUmPDBButton,
              id=wxID_FRAME1ESCOLHERUMPDB)

        self.staticBox7 = wx.StaticBox(id=wxID_FRAME1STATICBOX7, label=u'',
              name='staticBox7', parent=self.scrolledWindow1, pos=wx.Point(232,
              120), size=wx.Size(224, 100), style=0)

        self.staticBox8 = wx.StaticBox(id=wxID_FRAME1STATICBOX8,
              label=u'Modeling', name='staticBox8', parent=self.scrolledWindow1,
              pos=wx.Point(8, 367), size=wx.Size(944, 184), style=0)

        self.staticText12 = wx.StaticText(id=wxID_FRAME1STATICTEXT12,
              label=u'Obtained Model:', name='staticText12',
              parent=self.scrolledWindow1, pos=wx.Point(384, 511),
              size=wx.Size(136, 17), style=0)

        self.BotaoAbrirdoModelarResultado = wx.Button(id=wxID_FRAME1BOTAOABRIRDOMODELARRESULTADO,
              label=u'Open', name=u'BotaoAbrirdoModelarResultado',
              parent=self.scrolledWindow1, pos=wx.Point(816, 511),
              size=wx.Size(80, 24), style=0)
        self.BotaoAbrirdoModelarResultado.Enable(False)
        self.BotaoAbrirdoModelarResultado.Bind(wx.EVT_BUTTON,
              self.OnBotaoAbrirdoModelarResultado,
              id=wxID_FRAME1BOTAOABRIRDOMODELARRESULTADO)

        self.PROCHECK = wx.Button(id=wxID_FRAME1PROCHECK, label=u'Evaluate',
              name=u'PROCHECK', parent=self.scrolledWindow1, pos=wx.Point(16,
              567), size=wx.Size(104, 72), style=0)
        self.PROCHECK.Enable(False)
        self.PROCHECK.Bind(wx.EVT_BUTTON, self.OnPROCHECKButton,
              id=wxID_FRAME1PROCHECK)

        # self.BotaoAbrirdoModelarAlinhamentoPAP = wx.Button(id=wxID_FRAME1BOTAOABRIRDOMODELARALINHAMENTOPAP,
        #       label=u'Open', name='BotaoAbrirdoModelarAlinhamentoPAP',
        #       parent=self.scrolledWindow1, pos=wx.Point(816, 468),
        #       size=wx.Size(80, 24), style=0)
        # self.BotaoAbrirdoModelarAlinhamentoPAP.Enable(False)
        # self.BotaoAbrirdoModelarAlinhamentoPAP.Bind(wx.EVT_BUTTON,
        #       self.Action_of_Abrir_Buttons,
        #       id=wxID_FRAME1BOTAOABRIRDOMODELARALINHAMENTOPAP)

        self.ResetButton = wx.Button(id=wxID_FRAME1RESETBUTTON, label=u'Reset',
              name=u'ResetButton', parent=self.scrolledWindow1,
              pos=wx.Point(788, 568), size=wx.Size(94, 72), style=0)
        self.ResetButton.Enable(True)
        self.ResetButton.Bind(wx.EVT_BUTTON, self.OnResetButtonButton,
              id=wxID_FRAME1RESETBUTTON)

        self.capturar_arquivos_para_alinhar = wx.Button(id=wxID_FRAME1CAPTURAR_ARQUIVOS_PARA_ALINHAR,
              label=u'      Fast\nAlignment',
              name=u'capturar_arquivos_para_alinhar',
              parent=self.scrolledWindow1, pos=wx.Point(14, 269),
              size=wx.Size(104, 72), style=0)
        self.capturar_arquivos_para_alinhar.Bind(wx.EVT_BUTTON,
              self.OnCapturar_arquivos_para_alinharButton,
              id=wxID_FRAME1CAPTURAR_ARQUIVOS_PARA_ALINHAR)

        self.capturar_arquivos_para_modelagem = wx.Button(id=wxID_FRAME1CAPTURAR_ARQUIVOS_PARA_MODELAGEM,
              label=u'Fast Modeling', name=u'capturar_arquivos_para_modelagem',
              parent=self.scrolledWindow1, pos=wx.Point(14, 423),
              size=wx.Size(104, 72), style=0)
        self.capturar_arquivos_para_modelagem.Bind(wx.EVT_BUTTON,
              self.OnCapturar_arquivos_para_modelagemButton,
              id=wxID_FRAME1CAPTURAR_ARQUIVOS_PARA_MODELAGEM)

        self.staticBox9 = wx.StaticBox(id=wxID_FRAME1STATICBOX9, label=u'',
              name='staticBox9', parent=self.scrolledWindow1, pos=wx.Point(128,
              232), size=wx.Size(824, 136), style=0)

        self.staticBox10 = wx.StaticBox(id=wxID_FRAME1STATICBOX10, label=u'',
              name='staticBox10', parent=self.scrolledWindow1, pos=wx.Point(120,
              368), size=wx.Size(832, 183), style=0)

        self.RefinarLoops = wx.Button(id=wxID_FRAME1REFINARLOOPS,
              label=u'Refine Loops', name=u'RefinarLoops',
              parent=self.scrolledWindow1, pos=wx.Point(130, 464),
              size=wx.Size(104, 72), style=0)
        self.RefinarLoops.Enable(False)
        self.RefinarLoops.Bind(wx.EVT_BUTTON, self.OnRefinarLoopsButton,
              id=wxID_FRAME1REFINARLOOPS)

        self.VersaoParaTeste = wx.StaticText(id=wxID_FRAME1VERSAOPARATESTE,
              label=u'Test Version v. 0.50M', name=u'VersaoParaTeste',
              parent=self.scrolledWindow1, pos=wx.Point(310, 650),
              size=wx.Size(126, 25), style=0)

        self.CompararModelos = wx.Button(id=wxID_FRAME1COMPARARMODELOS,
              label=u'Compare\n  Models', name=u'CompararModelos',
              parent=self.scrolledWindow1, pos=wx.Point(120, 568),
              size=wx.Size(104, 72), style=0)
        self.CompararModelos.Enable(False)
        self.CompararModelos.Bind(wx.EVT_BUTTON, self.OnCompararModelosButton,
              id=wxID_FRAME1COMPARARMODELOS)

        self.EditdoModelarResultado = wx.Choice(choices=[],
              id=wxID_FRAME1EDITDOMODELARRESULTADO,
              name=u'EditdoModelarResultado', parent=self.scrolledWindow1,
              pos=wx.Point(536, 512), size=wx.Size(264, 27), style=0)
        self.EditdoModelarResultado.Bind(wx.EVT_CHOICE,
              self.OnEditdoModelarResultadoChoice,
              id=wxID_FRAME1EDITDOMODELARRESULTADO)

        self.AbrirPastaButton = wx.Button(id=wxID_FRAME1ABRIRPASTABUTTON,
              label=u'   Work\nDirectory', name=u'AbrirPastaButton',
              parent=self.scrolledWindow1, pos=wx.Point(704, 568),
              size=wx.Size(85, 72), style=0)
        self.AbrirPastaButton.Bind(wx.EVT_BUTTON, self.OnAbrirPastaButtonButton,
              id=wxID_FRAME1ABRIRPASTABUTTON)

        self.staticBox11 = wx.StaticBox(id=wxID_FRAME1STATICBOX11,
              label=u'Tools', name='staticBox11', parent=self.scrolledWindow1,
              pos=wx.Point(696, 552), size=wx.Size(258, 100), style=0)

        self.AboutAutoModelLink = wx.lib.agw.hyperlink.HyperLinkCtrl(URL="http://www.wxpython.org/",
              id=wxID_FRAME1ABOUTAUTOMODELLINK, label=u'About AutoModel',
              name=u'AboutAutoModelLink', parent=self.scrolledWindow1,
              pos=wx.Point(800, 656), size=wx.Size(112, 17), style=0)
        self.AboutAutoModelLink.AutoBrowse(False)
        self.AboutAutoModelLink.Bind(wx.lib.hyperlink.EVT_HYPERLINK_LEFT,
              self.OnAboutAutoModelLinkHyperlinkLeft)

        self.manualAutoModelLink = wx.lib.agw.hyperlink.HyperLinkCtrl(URL="file://" + os.getcwd() + "/manual/AutoModel.pdf",
              id=wxID_FRAME1MANUALAUTOMODELLINK, label=u"User's Manual",
              name=u'manualAutoModelLink', parent=self.scrolledWindow1,
              pos=wx.Point(688, 656), size=wx.Size(93, 17), style=0)
        self.manualAutoModelLink.Bind(wx.EVT_LEFT_DOWN,
              self.OnManualAutoModelLinkLeftDown)

        self.staticText5 = wx.StaticText(id=wxID_FRAME1STATICTEXT5,
              label=u'DOPE Score:', name='staticText5',
              parent=self.scrolledWindow1, pos=wx.Point(232, 580),
              size=wx.Size(153, 17), style=0)

        self.EditdoScoreDope = wx.TextCtrl(id=wxID_FRAME1EDITDOSCOREDOPE,
              name=u'EditdoScoreDope', parent=self.scrolledWindow1,
              pos=wx.Point(328, 580), size=wx.Size(272, 24), style=0,
              value=u'')
        self.EditdoScoreDope.SetEditable(False)

        self.BotaoAbrirdoScoreDope = wx.Button(id=wxID_FRAME1BOTAOABRIRDOSCOREDOPE,
              label=u'Open', name=u'BotaoAbrirdoScoreDope',
              parent=self.scrolledWindow1, pos=wx.Point(608, 580),
              size=wx.Size(80, 24), style=0)
        self.BotaoAbrirdoScoreDope.Enable(False)
        self.BotaoAbrirdoScoreDope.Bind(wx.EVT_BUTTON,
              self.OnBotaoAbrirdoScoreDopeButton,
              id=wxID_FRAME1BOTAOABRIRDOSCOREDOPE)

    def __init__(self, parent):
        self._init_ctrls(parent)
        self.prefs = Prefs()
        selectAutoModelMode = SelectAutoModelMode(self)
        selectAutoModelMode.ShowModal()
        if self.prefs.get_setting("Online"):
          from network.client import Client
        else:
          from network.clientX import Client
        try:
          self.client_instance = Client()
          self.show_window_send_serial()
          self.client_instance.disconnect()
        except socket.error, e:
          error = AutoModelError("Unable connect with the server. Check your internet connection or try again later.")
          error.log(e)
          self.Destroy()
        else:
        	self.clientold = Clientold()
        	font = wx.Font(18, wx.DECORATIVE, wx.ITALIC, wx.NORMAL)
        	self.VersaoParaTeste.SetFont(font)
        	self.VersaoParaTeste.SetForegroundColour(wx.RED)
        	self.PrepareBeforeStartModelling = PrepareBeforeStartModelling()
        	self.workdir = self.PrepareBeforeStartModelling.get_workdir()
        	self.FindTemplatesStep = FindTemplatesStep(self.client_instance, self.workdir)

        # old_list = self.EditdoModelarResultado.choices

    def show_window_send_serial(self):
        edit = wx.TextEntryDialog(None, "To use AutoModel is necessary to obtain a license key from the program Modeller.\nTo obtain this key access http://www.salilab.org/modeller/accelrys.html and enter the key in the field below:","Text Entry", "", style=wx.OK|wx.CANCEL)
        if edit.ShowModal() == wx.ID_OK:
          key = edit.GetValue()
          if self.client_instance.check_serial(key):
            edit.Destroy()
          else:
            wx.MessageBox("You entered a wrong key.\nObtain more information in http://www.salilab.org/modeller/accelrys.html", 'Oops', wx.OK | wx.ICON_ERROR)
            edit.Destroy()
            self.show_window_send_serial()
        else: 
          edit.Destroy()
          self.Destroy()

         
#Carga inicio
    def OnBotaoAbrirArquivoFasta(self, event):
		arquivodasequencia = wx.FileSelector("Select a file in FASTA Format", default_path="", default_filename="", default_extension="", wildcard="*.*", flags=0, parent=None, x=-1, y=-1)
		if arquivodasequencia:
			self.FindTemplatesStep.set_fasta_file(arquivodasequencia)
			self.EditdoCaminhoArquivoFasta.SetValue(arquivodasequencia)
			self.EscolherUmPDB.Enable(True)
			self.BuscarTemplate.Enable(True)

    def OnCarregarButton(self, event):
        self.FiguradeTrabalhando.Play()
        Publisher().subscribe(self.onFindTemplatesStepDone, "onFindTemplatesStepDone")
        thread.start_new_thread(self.FindTemplatesStep.run, ())

    def onFindTemplatesStepDone(self, event):
        self.FiguradeTrabalhando.Stop()
        try:
          build_profilePIR = self.FindTemplatesStep.build_profilePIR
          frame2 = SelectTemplate_Window(self, -1,  build_profilePIR)
          frame2.ShowModal()
        except IndexError, e:
          wx.MessageBox("There no similar sequence was found", 'Oops', wx.OK | wx.ICON_ERROR)
        else:
          if frame2.out():
              template_id = frame2.out()[1][4:8]              
              self.FiguradeTrabalhando.Play()
              Publisher().subscribe(self.onChooseTemplateDone, "onChooseTemplateDone")
              thread.start_new_thread(self.FindTemplatesStep.select_template, (template_id,))  

    def onChooseTemplateDone(self, event):
        self.Alinhar.Enable()
        self.ModificarTemplate.Enable()
        self.FiguradeTrabalhando.Stop()

        self.EditdoCarregarPIR.SetValue(self.FindTemplatesStep.build_profilePIR)
        self.EditdoCarregarPAP.SetValue(self.FindTemplatesStep.build_profilePAP)
        self.EditdoCarregarPRF.SetValue(self.FindTemplatesStep.build_profilePRF)
        self.EditdoAlinharPDB.SetValue(self.FindTemplatesStep.get_template_filename())
        button_list = [self.ResetButton, self.BotaoAbrirdoCarregarPIR, self.BotaoAbrirdoCarregarPAP, self.BotaoAbrirdoCarregarPRF, self.BotaoAbrirdoAlinharPDB]
        for eachButton in button_list:
            eachButton.Enable(True)

    def Action_of_Abrir_Buttons(self, event):
        button_obj = event.GetEventObject()
        button_name = button_obj.GetName()
        # self.clientold.open_txt_file(eval("self.Edit" + button_name[10:] + ".GetValue()"))
        template_load_window = TextEditorWindow(self, eval("self.Edit" + button_name[10:] + ".GetValue()"))
        template_load_window.Show()
        # try:
          # self.clientold.open_txt_file(eval("self.Edit" + button_name[10:] + ".GetValue()"))
        # except Exception, e:
        #   self.choose_text_editor(eval("self.Edit" + button_name[10:] + ".GetValue()"))

    def OnEscolherUmPDBButton(self, event):
        template_filename = wx.FileSelector("Select a file in PDB format", default_path="", default_filename="", default_extension="", wildcard="*.pdb", flags=0, parent=None, x=-1, y=-1)
        if template_filename:
        	self.FindTemplatesStep.set_my_template(template_filename)
        	self.ModificarTemplate.Enable(True)
        	self.Alinhar.Enable(True)
        	self.EditdoAlinharPDB.SetValue(self.FindTemplatesStep.get_template_filename())
        	self.BotaoAbrirdoAlinharPDB.Enable(True)

    def OnButton2Button(self, event):
        template_load_window = MiniFrame1(self)
        template_load_window.Show()

    def OnButton2ButtonDone(self, filename):
		self.FindTemplatesStep.set_fasta_file(filename)
		self.EditdoCaminhoArquivoFasta.SetValue(filename)
		self.EscolherUmPDB.Enable(True)
		self.BuscarTemplate.Enable(True)


#Carga FIM
#Alinhamento INICIO


    def OnModificarTemplateButton(self, event):
        seq_ali = self.FindTemplatesStep.pir_sequence_file
        my_template = self.FindTemplatesStep.template
        print seq_ali
        print my_template
        try:
        	ModificarTemplateWindow = AlterarCadeiasEHeteroatomos(self, -1, my_template, seq_ali)
        	ModificarTemplateWindow.ShowModal()
        except Exception, e:
        	error = AutoModelError("There was a problem opening the template, please check out before continuing his consistency")
        	error.log(e)


    def OnAlinharButton(self, event):	
      self.FiguradeTrabalhando.Play()
      self.AlignStep = AlignStep(self.client_instance, self.workdir, self.FindTemplatesStep.template, self.FindTemplatesStep.pir_sequence_file)
      Publisher().subscribe(self.OnAlinharButtonDone, "OnAlinharButtonDone")
      thread.start_new_thread(self.AlignStep.run, ())
   
    def OnAlinharButtonDone(self, event):
      self.FiguradeTrabalhando.Stop()
      self.MudarHeteroatomo.Enable(True)
      self.Modelar.Enable(True)
      self.EditdoArquivoInicial.SetValue(self.FindTemplatesStep.get_template_filename())
      self.EditdoAlinhamentoFinalPIR.SetValue(self.AlignStep.ali_ali)
      # self.EditdoAlinhamentoFinalPAP.SetValue(self.AlignStep.ali_pap)
 
      button_list = [self.BotaoAbrirdoArquivoInicial,self.BotaoAbrirdoAlinhamentoFinalPIR]
      for eachButton in button_list:
         eachButton.Enable(True)

#Alinhamento FIM
#Modelagem INICIO

    def OnMudarHeteroatomoButton(self, event):
        try:
          change_het_window_instance = ChangeHetWindow(self, -1, self.FindTemplatesStep.template)
          change_het_window_instance.ShowModal()
        except TypeError, e:
          error = AutoModelError("Not heteroatoms were found. If you selected heteroatoms in the window Change heteroatoms check the integrity of the Template file and the alignment file.")
          error.log(e)


    def OnModelarButton(self, event):
        self.FiguradeTrabalhando.Play()
        self.ModelStep = ModelStep(self.client_instance, self.workdir, self.FindTemplatesStep.template, self.AlignStep.ali_ali)

        Publisher().subscribe(self.OnModelarButtonDone, "OnModelarButtonDone")
        thread.start_new_thread(self.ModelStep.run, ())

    def OnModelarButtonDone(self,event):

#avaliar         
        self.EditdoModelarResultado.Clear()
        old_list = self.EditdoModelarResultado.GetItems()
        self.EditdoModelarResultado.Clear()
        self.EditdoModelarResultado.AppendItems([self.ModelStep.model] + old_list)
        self.EditdoModelarResultado.SetSelection(0)

        self.FiguradeTrabalhando.Play()
        result = self.EditdoModelarResultado.GetStringSelection()
        self.EvaluateStep = EvaluateStep(self.client_instance, self.workdir, self.FindTemplatesStep.template, result,self.AlignStep.ali_ali)
        Publisher().subscribe(self.OnAvaliarButtonDone, "OnAvaliarButtonDone")
        thread.start_new_thread(self.EvaluateStep.run, ())



    def OnSalvarResultadosButton(self, event):
        if os.path.exists(os.path.dirname(self.ModelStep.model)):
            arquivo = self.EditdoModelarResultado.GetStringSelection()
            dialog = wx.FileDialog(None, "Save the result in:", defaultFile= arquivo,  style=wx.FD_SAVE)
            if dialog.ShowModal() == wx.ID_OK:
                salvar = dialog.GetPath()
                self.clientold.save_result_in(self.ModelStep.model,salvar)

    def OnBotaoAbrirdoModelarResultado(self, event):
    	try:
    		self.clientold.open_result(self.EditdoModelarResultado.GetStringSelection())
    	except Exception, e:
    		self.choose_molecular_viewer(self.EditdoModelarResultado.GetStringSelection())
        

    def OnCloseWindow(self, event):
        pass

    def OnAvaliarButton(self, event):
        self.FiguradeTrabalhando.Play()
        result = self.EditdoModelarResultado.GetStringSelection()
        self.EvaluateStep = EvaluateStep(self.client_instance, self.workdir, self.FindTemplatesStep.template, result,self.AlignStep.ali_ali)
        Publisher().subscribe(self.OnAvaliarButtonDone, "OnAvaliarButtonDone")
        thread.start_new_thread(self.EvaluateStep.run, ())

    def OnAvaliarButtonDone(self, event):
        self.FiguradeTrabalhando.Stop()
        # self.EditDoPlot_profile.SetValue(self.EvaluateStep.evaluate_jpg)
        # self.AbrirdoEditPlotProfile.Enable(True)
        self.EditdoScoreDope.SetValue(self.EvaluateStep.evaluate_jpg)
        self.BotaoAbrirdoScoreDope.Enable(True)
        self.FiguradeTrabalhando.Stop()
        self.SalvarResultados.Enable(True)
        # self.Avaliar.Enable(True)
        self.PROCHECK.Enable(True)
        self.RefinarLoops.Enable(True)

        self.EditdoModelarPDB.SetValue(self.FindTemplatesStep.get_template_filename())
        self.EditdoModelarAlinhamentoPIR.SetValue(self.AlignStep.ali_ali)
        if(self.AlignStep.ali_pap != None):
          self.EditdoModelarAlinhamentoPAP.SetValue(self.AlignStep.ali_pap)
          self.BotaoAbrirdoModelarAlinhamentoPAP.Enable()
        self.EditdoModelarResultado.Clear()
        old_list = self.EditdoModelarResultado.GetItems()
        self.EditdoModelarResultado.Clear()
        self.EditdoModelarResultado.AppendItems([self.ModelStep.model] + old_list)
        self.EditdoModelarResultado.SetSelection(0)
        button_list = [self.BotaoAbrirdoModelarPDB,self.BotaoAbrirdoModelarAlinhamentoPIR,self.BotaoAbrirdoModelarResultado]
        for eachButton in button_list:
            eachButton.Enable(True)
        self.staticBox3.SetLabel("Evaluate " + os.path.basename(self.ModelStep.model))
        try:
          window = ImageViewerWindow(self,self.EvaluateStep.evaluate_jpg)          
          window.Show()
        except Exception, e:
          self.choose_image_viewer(self.EvaluateStep.evaluate_jpg)

    # def OnAbrirdoEditPlotProfileButton(self, event):
    #     try:
    #       self.clientold.open_plot_profile(self.EvaluateStep.evaluate_jpg)          
    #     except Exception, e:
    #       print e
    #       self.choose_image_viewer(self.EvaluateStep.evaluate_jpg)

    def OnPROCHECKButton(self, event):
        self.FiguradeTrabalhando.Play()
        result = self.EditdoModelarResultado.GetStringSelection()
        self.EvaluateProcheckStep = EvaluateProcheckStep(self.client_instance, self.workdir, result)
        Publisher().subscribe(self.OnPROCHECKButtonDone, "OnPROCHECKButtonDone")
        thread.start_new_thread(self.EvaluateProcheckStep.run, ())

    def OnPROCHECKButtonDone(self,event):
        self.FiguradeTrabalhando.Stop()
        self.clientold.open_procheck_folder(self.EvaluateProcheckStep.folder)

    def OnCapturar_arquivos_para_alinharButton(self, event):
        automatic_align_window = align_window(self)
        automatic_align_window.ShowModal()
        if automatic_align_window.ok == True:
            arquivodasequencia = automatic_align_window.get_sequence_filename()
            template_filename = automatic_align_window.get_template_filename()
            self.FindTemplatesStep.set_fasta_file(arquivodasequencia)
            self.EditdoCaminhoArquivoFasta.SetValue(arquivodasequencia)
            self.EscolherUmPDB.Enable(True)
            self.BuscarTemplate.Enable(True)

            self.FindTemplatesStep.set_my_template(template_filename)
            self.ModificarTemplate.Enable(True)
            self.Alinhar.Enable(True)
            self.EditdoAlinharPDB.SetValue(self.FindTemplatesStep.get_template_filename())
            self.BotaoAbrirdoAlinharPDB.Enable(True)
        
    def OnCapturar_arquivos_para_modelagemButton(self, event):
        automatic_modeling_window = modeling_window(self)
        automatic_modeling_window.ShowModal()
        if automatic_modeling_window.ok == True:
        	alignment_filename = automatic_modeling_window.get_alignment_filename()
        	template_filename = automatic_modeling_window.get_template_filename()
        	self.FindTemplatesStep.set_my_template_without_fasta_file(template_filename)
        	self.AlignStep = AlignStep(self.client_instance, self.workdir, self.FindTemplatesStep.template, None)
        	self.AlignStep.set_my_alignment(alignment_filename)

        	self.FiguradeTrabalhando.Stop()
        	self.MudarHeteroatomo.Enable(True)
        	self.Modelar.Enable(True)
        	self.EditdoArquivoInicial.SetValue(self.FindTemplatesStep.get_template_filename())
        	self.EditdoAlinhamentoFinalPIR.SetValue(self.AlignStep.ali_ali)
        	button_list = [self.BotaoAbrirdoArquivoInicial,self.BotaoAbrirdoAlinhamentoFinalPIR]
        	for eachButton in button_list:
        		eachButton.Enable(True)        	

    def OnRefinarLoopsButton(self, event):
        dialog = Refinamento_de_Loop(self,self.ModelStep.model)
        dialog.ShowModal()

    def OnAbrirdoRefinar_LoopsButton(self, event):
    	try:
    		self.clientold.open_result(self.LoopModelStep.loopmodel)
    	except Exception, e:
    		self.choose_molecular_viewer(self.LoopModelStep.loopmodel)        

    def OnCompararModelosButton(self, event):
        self.FiguradeTrabalhando.Play()
        self.EvaluateAfterLoopRefinamentStep = EvaluateAfterLoopRefinamentStep(self.client_instance, self.workdir, self.FindTemplatesStep.template,  self.ModelStep.model, self.LoopModelStep.loopmodel, self.AlignStep.ali_ali)
        Publisher().subscribe(self.EvaluateAfterLoopRefinamentStepDone, "EvaluateAfterLoopRefinamentStepDone")
        thread.start_new_thread(self.EvaluateAfterLoopRefinamentStep.run, ())

    def EvaluateAfterLoopRefinamentStepDone(self,event):
        self.CompararModelos.Enable(True)
        self.staticBox3.SetLabel("Evaluate " + os.path.basename(self.LoopModelStep.loopmodel))
        self.FiguradeTrabalhando.Stop()
        try:
          window = ImageViewerWindow(self,self.EvaluateAfterLoopRefinamentStep.evaluateloop_jpg)          
          window.Show()
        except Exception, e:
          self.choose_image_viewer(self.EvaluateAfterLoopRefinamentStep.evaluateloop_jpg)
     
    def send_loop_refinament(self, start_residue, end_residue):
        self.FiguradeTrabalhando.Play()
        self.LoopModelStep = LoopModelStep(self.client_instance, self.workdir, self.ModelStep.model)
        self.LoopModelStep.set_start_residue(start_residue)
        self.LoopModelStep.set_end_residue(end_residue)
        Publisher().subscribe(self.send_loop_refinamentDone, "send_loop_refinamentDone")
        thread.start_new_thread(self.LoopModelStep.run, ())

    def send_loop_refinamentDone(self, event):
        # self.FiguradeTrabalhando.Stop()
        self.CompararModelos.Enable(True)
        old_list = self.EditdoModelarResultado.GetItems()
        self.EditdoModelarResultado.Clear()
        self.EditdoModelarResultado.AppendItems([self.LoopModelStep.loopmodel] + old_list)
        self.EditdoModelarResultado.SetSelection(0)


        

        self.FiguradeTrabalhando.Play()
        self.EvaluateAfterLoopRefinamentStep = EvaluateAfterLoopRefinamentStep(self.client_instance, self.workdir, self.FindTemplatesStep.template,  self.ModelStep.model, self.LoopModelStep.loopmodel, self.AlignStep.ali_ali)
        Publisher().subscribe(self.EvaluateAfterLoopRefinamentStepDone, "EvaluateAfterLoopRefinamentStepDone")
        thread.start_new_thread(self.EvaluateAfterLoopRefinamentStep.run, ())

        # self.AbrirdoRefinar_Loops.Enable()
        # self.BotaoSalvarModeloRefinado.Enable(True)

    # def OnBotaoSalvarModeloRefinadoButton(self, event):
    #     if os.path.exists(os.path.dirname(self.LoopModelStep.loopmodel)):
    #         arquivo = self.LoopModelStep.loopmodel
    #         dialog = wx.FileDialog(None, "Salvar o resultado em:", defaultFile= arquivo,  style=wx.FD_SAVE)
    #         if dialog.ShowModal() == wx.ID_OK:
    #             salvar = dialog.GetPath()
    #             self.clientold.save_result_in(self.LoopModelStep.loopmodel,salvar)


#-----------------------
    def choose_text_editor(self, arquivo):
        edit = wx.TextEntryDialog(None, "Enter the name of your text editor:","Text Entry", "kate", style=wx.OK|wx.CANCEL)
        if edit.ShowModal() == wx.ID_OK:
          editor = edit.GetValue()
          try:
            self.clientold.open_in_other_editor(editor, arquivo)
          except Exception, e:
            print e
            self.choose_text_editor(arquivo)

    def choose_molecular_viewer(self, arquivo):
        edit = wx.TextEntryDialog(None, "Enter the name of your molecular viewer software:","Text Entry", "vmd", style=wx.OK|wx.CANCEL)
        if edit.ShowModal() == wx.ID_OK:
          editor = edit.GetValue()
          try:
            self.clientold.open_in_other_editor(editor, arquivo)
          except Exception, e:
            print e
            self.choose_text_editor(arquivo)

    def choose_image_viewer(self, arquivo):
        edit = wx.TextEntryDialog(None, "Enter the name of your image viewer software (.jpg):","Text Entry", "eog", style=wx.OK|wx.CANCEL)
        if edit.ShowModal() == wx.ID_OK:
          editor = edit.GetValue()
          try:
            self.clientold.open_in_other_editor(editor, arquivo)
          except Exception, e:
            print e
            self.choose_text_editor(arquivo)

    def OnAbrirPastaButtonButton(self, event):
        self.clientold.open_procheck_folder(self.workdir)

    def OnEditdoModelarResultadoChoice(self, event):
        self.staticBox3.SetLabel("Evaluate " + os.path.basename(self.EditdoModelarResultado.GetStringSelection()))

    def OnManualAutoModelLinkLeftDown(self, event):
        event.Skip()

    def OnAboutAutoModelLinkHyperlinkLeft(self, event):
        aboutWindow = AboutAutoModel(self)
        aboutWindow.ShowModal()

    def OnBotaoAbrirdoScoreDopeButton(self, event):
        try:
          window = ImageViewerWindow(self,self.EvaluateStep.evaluate_jpg)          
          window.Show()
        except Exception, e:
          self.choose_image_viewer(self.EvaluateStep.evaluate_jpg)

    def OnResetButtonButton(self, event):
        self.FiguradeTrabalhando.Stop()
        for eachWidget in self.scrolledWindow1.GetChildren(): 
            if eachWidget.__class__ == wx._controls.Button:
                eachWidget.Enable(False)
            if eachWidget.__class__ == wx._controls.TextCtrl:
                eachWidget.Clear()
            if eachWidget.__class__ == wx._controls.Choice:
                eachWidget.Clear()
        self.ResetButton.Enable(True)
        self.BotaoAbrirArquivoFasta.Enable(True)
        self.button2.Enable(True)
        self.capturar_arquivos_para_alinhar.Enable(True)
        self.capturar_arquivos_para_modelagem.Enable(True)
        self.AbrirPastaButton.Enable(True)
        self.PrepareBeforeStartModelling = PrepareBeforeStartModelling()
        self.workdir = self.PrepareBeforeStartModelling.get_workdir()
        self.FindTemplatesStep = FindTemplatesStep(self.client_instance, self.workdir)
        self.staticBox3.SetLabel("Avaliacao de Modelo")
