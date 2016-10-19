#Boa:Dialog:modelar_sem_alinhar

import wx

def create(parent):
    return modelar_sem_alinhar(parent)

[wxID_MODELAR_SEM_ALINHAR, wxID_MODELAR_SEM_ALINHARBUTTONALINHAMENTO, 
 wxID_MODELAR_SEM_ALINHARBUTTONCANCELAR, wxID_MODELAR_SEM_ALINHARBUTTONOK, 
 wxID_MODELAR_SEM_ALINHARBUTTONPDB, wxID_MODELAR_SEM_ALINHARSTATICTEXT1, 
 wxID_MODELAR_SEM_ALINHARSTATICTEXT2, wxID_MODELAR_SEM_ALINHARSTATICTEXT3, 
 wxID_MODELAR_SEM_ALINHARTEXTCTRLALINHAMENTO, 
 wxID_MODELAR_SEM_ALINHARTEXTCTRLPDB, 
] = [wx.NewId() for _init_ctrls in range(10)]

class modelar_sem_alinhar(wx.Dialog):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Dialog.__init__(self, id=wxID_MODELAR_SEM_ALINHAR,
              name=u'modelar_sem_alinhar', parent=prnt, pos=wx.Point(473, 329),
              size=wx.Size(525, 189), style=wx.DEFAULT_DIALOG_STYLE,
              title=u'Modelar Template')
        self.SetClientSize(wx.Size(525, 189))

        self.buttonPDB = wx.Button(id=wxID_MODELAR_SEM_ALINHARBUTTONPDB,
              label=u'Open...', name=u'buttonPDB', parent=self,
              pos=wx.Point(432, 40), size=wx.Size(85, 32), style=0)
        self.buttonPDB.Bind(wx.EVT_BUTTON, self.OnButtonPDBButton,
              id=wxID_MODELAR_SEM_ALINHARBUTTONPDB)

        self.buttonAlinhamento = wx.Button(id=wxID_MODELAR_SEM_ALINHARBUTTONALINHAMENTO,
              label=u'Open...', name=u'buttonAlinhamento', parent=self,
              pos=wx.Point(432, 88), size=wx.Size(85, 32), style=0)
        self.buttonAlinhamento.Bind(wx.EVT_BUTTON,
              self.OnButtonAlinhamentoButton,
              id=wxID_MODELAR_SEM_ALINHARBUTTONALINHAMENTO)

        self.buttonOK = wx.Button(id=wxID_MODELAR_SEM_ALINHARBUTTONOK,
              label=u'OK', name=u'buttonOK', parent=self, pos=wx.Point(280,
              152), size=wx.Size(85, 32), style=0)
        self.buttonOK.Bind(wx.EVT_BUTTON, self.OnButtonOKButton,
              id=wxID_MODELAR_SEM_ALINHARBUTTONOK)

        self.buttonCancelar = wx.Button(id=wxID_MODELAR_SEM_ALINHARBUTTONCANCELAR,
              label=u'Cancel', name=u'buttonCancelar', parent=self,
              pos=wx.Point(180, 152), size=wx.Size(85, 31), style=0)
        self.buttonCancelar.Bind(wx.EVT_BUTTON, self.OnButtonCancelarButton,
              id=wxID_MODELAR_SEM_ALINHARBUTTONCANCELAR)

        self.textCtrlPDB = wx.TextCtrl(id=wxID_MODELAR_SEM_ALINHARTEXTCTRLPDB,
              name=u'textCtrlPDB', parent=self, pos=wx.Point(96, 40),
              size=wx.Size(328, 32), style=0, value=u'')

        self.textCtrlAlinhamento = wx.TextCtrl(id=wxID_MODELAR_SEM_ALINHARTEXTCTRLALINHAMENTO,
              name=u'textCtrlAlinhamento', parent=self, pos=wx.Point(96, 88),
              size=wx.Size(328, 32), style=0, value=u'')

        self.staticText1 = wx.StaticText(id=wxID_MODELAR_SEM_ALINHARSTATICTEXT1,
              label=u'To make modelling is necessary of Template in the PDB format and of alignment file.',
              name='staticText1', parent=self, pos=wx.Point(8, 8),
              size=wx.Size(504, 40), style=0)

        self.staticText2 = wx.StaticText(id=wxID_MODELAR_SEM_ALINHARSTATICTEXT2,
              label=u'PDB:', name='staticText2', parent=self, pos=wx.Point(8,
              48), size=wx.Size(29, 15), style=0)

        self.staticText3 = wx.StaticText(id=wxID_MODELAR_SEM_ALINHARSTATICTEXT3,
              label=u'Alingment:', name='staticText3', parent=self,
              pos=wx.Point(8, 96), size=wx.Size(81, 15), style=0)

    def __init__(self, parent):
        # self.parent = parent
        self._init_ctrls(parent)
        # self.client_instance = client_instance
        self.ok = False

    def OnButtonPDBButton(self, event):
        arquivo_do_pdb = wx.FileSelector("Select the template in PDB format", default_path="", default_filename="", default_extension="", wildcard="*.pdb", flags=0, parent=None, x=-1, y=-1)
        self.textCtrlPDB.SetValue(arquivo_do_pdb)

    def OnButtonAlinhamentoButton(self, event):
        arquivo_de_alinhamento = wx.FileSelector("Select the alignment file", default_path="", default_filename="", default_extension="", wildcard="*.*", flags=0, parent=None, x=-1, y=-1)
        self.textCtrlAlinhamento.SetValue(arquivo_de_alinhamento)

    def OnButtonOKButton(self, event):
        # self.client_instance.connect_with_server()
        # self.client_instance.send_pdb_file_for_the_server2(self.textCtrlPDB.GetValue())
        # self.client_instance.copy_file_in(self.textCtrlAlinhamento.GetValue(), self.client_instance.get_workdir() + "models/ali.ali")
        # self.client_instance.checkpoint = "align_templates"
        # self.parent.MudarHeteroatomo.Enable(True)
        # self.parent.Modelar.Enable(True)
        # self.parent.default_pathway_modelar = False
        self.alignment_filename = self.textCtrlAlinhamento.GetValue()
        self.template_filename = self.textCtrlPDB.GetValue()
        self.ok = True
        self.Close()

    def OnButtonCancelarButton(self, event):
        self.Close()

    def get_alignment_filename(self):
        return self.alignment_filename

    def get_template_filename(self):
        return self.template_filename