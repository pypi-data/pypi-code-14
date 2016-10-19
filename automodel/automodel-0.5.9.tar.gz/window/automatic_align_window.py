#Boa:Dialog:alinhar_sequencia_sem_buscar_template

import wx
import os

def create(parent):
    return alinhar_sequencia_sem_buscar_template(parent)

[wxID_ALINHAR_SEQUENCIA_SEM_BUSCAR_TEMPLATE, 
 wxID_ALINHAR_SEQUENCIA_SEM_BUSCAR_TEMPLATEBUTTONCANCELAR, 
 wxID_ALINHAR_SEQUENCIA_SEM_BUSCAR_TEMPLATEBUTTONOK, 
 wxID_ALINHAR_SEQUENCIA_SEM_BUSCAR_TEMPLATEBUTTONPDB, 
 wxID_ALINHAR_SEQUENCIA_SEM_BUSCAR_TEMPLATEBUTTONSEQUENCIA, 
 wxID_ALINHAR_SEQUENCIA_SEM_BUSCAR_TEMPLATESTATICTEXT1, 
 wxID_ALINHAR_SEQUENCIA_SEM_BUSCAR_TEMPLATESTATICTEXTPDB, 
 wxID_ALINHAR_SEQUENCIA_SEM_BUSCAR_TEMPLATESTATICTEXTSEQUENCIA, 
 wxID_ALINHAR_SEQUENCIA_SEM_BUSCAR_TEMPLATETEXTCTRLPDB, 
 wxID_ALINHAR_SEQUENCIA_SEM_BUSCAR_TEMPLATETEXTCTRLSEQUENCIA, 
] = [wx.NewId() for _init_ctrls in range(10)]

class alinhar_sequencia_sem_buscar_template(wx.Dialog):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Dialog.__init__(self, id=wxID_ALINHAR_SEQUENCIA_SEM_BUSCAR_TEMPLATE,
              name=u'alinhar_sequencia_sem_buscar_template', parent=prnt,
              pos=wx.Point(622, 371), size=wx.Size(521, 173),
              style=wx.DEFAULT_DIALOG_STYLE, title=u'Alinhar sequencia')
        self.SetClientSize(wx.Size(521, 173))

        self.staticText1 = wx.StaticText(id=wxID_ALINHAR_SEQUENCIA_SEM_BUSCAR_TEMPLATESTATICTEXT1,
              label=u'To make the alignment is necessary of the user sequence in FASTA format and the template protein in PDB format.',
              name='staticText1', parent=self, pos=wx.Point(16, 8),
              size=wx.Size(504, 32), style=0)

        self.textCtrlSequencia = wx.TextCtrl(id=wxID_ALINHAR_SEQUENCIA_SEM_BUSCAR_TEMPLATETEXTCTRLSEQUENCIA,
              name=u'textCtrlSequencia', parent=self, pos=wx.Point(104, 40),
              size=wx.Size(264, 33), style=0, value=u'')
        self.textCtrlSequencia.SetEditable(False)

        self.textCtrlPDB = wx.TextCtrl(id=wxID_ALINHAR_SEQUENCIA_SEM_BUSCAR_TEMPLATETEXTCTRLPDB,
              name=u'textCtrlPDB', parent=self, pos=wx.Point(104, 80),
              size=wx.Size(264, 33), style=0, value=u'')
        self.textCtrlPDB.SetEditable(False)

        self.buttonSequencia = wx.Button(id=wxID_ALINHAR_SEQUENCIA_SEM_BUSCAR_TEMPLATEBUTTONSEQUENCIA,
              label=u'Open...', name=u'buttonSequencia', parent=self,
              pos=wx.Point(376, 42), size=wx.Size(85, 27), style=0)
        self.buttonSequencia.Bind(wx.EVT_BUTTON, self.OnButtonSequenciaButton,
              id=wxID_ALINHAR_SEQUENCIA_SEM_BUSCAR_TEMPLATEBUTTONSEQUENCIA)

        self.buttonPDB = wx.Button(id=wxID_ALINHAR_SEQUENCIA_SEM_BUSCAR_TEMPLATEBUTTONPDB,
              label=u'Open...', name=u'buttonPDB', parent=self,
              pos=wx.Point(376, 83), size=wx.Size(85, 27), style=0)
        self.buttonPDB.Bind(wx.EVT_BUTTON, self.OnButtonPDBButton,
              id=wxID_ALINHAR_SEQUENCIA_SEM_BUSCAR_TEMPLATEBUTTONPDB)

        self.staticTextSequencia = wx.StaticText(id=wxID_ALINHAR_SEQUENCIA_SEM_BUSCAR_TEMPLATESTATICTEXTSEQUENCIA,
              label=u'Target Seq.:', name=u'staticTextSequencia', parent=self,
              pos=wx.Point(5, 48), size=wx.Size(100, 15), style=0)

        self.staticTextPDB = wx.StaticText(id=wxID_ALINHAR_SEQUENCIA_SEM_BUSCAR_TEMPLATESTATICTEXTPDB,
              label=u'PDB: ', name=u'staticTextPDB', parent=self,
              pos=wx.Point(28, 88), size=wx.Size(33, 15), style=0)

        self.buttonCancelar = wx.Button(id=wxID_ALINHAR_SEQUENCIA_SEM_BUSCAR_TEMPLATEBUTTONCANCELAR,
              label=u'Cancel', name=u'buttonCancelar', parent=self,
              pos=wx.Point(112, 120), size=wx.Size(85, 27), style=0)
        self.buttonCancelar.Bind(wx.EVT_BUTTON, self.OnButtonCancelarButton,
              id=wxID_ALINHAR_SEQUENCIA_SEM_BUSCAR_TEMPLATEBUTTONCANCELAR)

        self.buttonOK = wx.Button(id=wxID_ALINHAR_SEQUENCIA_SEM_BUSCAR_TEMPLATEBUTTONOK,
              label=u'OK', name=u'buttonOK', parent=self, pos=wx.Point(328,
              120), size=wx.Size(85, 27), style=0)
        self.buttonOK.Bind(wx.EVT_BUTTON, self.OnButtonOKButton,
              id=wxID_ALINHAR_SEQUENCIA_SEM_BUSCAR_TEMPLATEBUTTONOK)

    def __init__(self,parent):
        self._init_ctrls(parent)
        # self.client_instance = client_instance
        # self.parent = parent
        self.ok = False

    def OnButtonSequenciaButton(self, event):
        arquivo_da_sequencia = wx.FileSelector("Select the your (target) sequence", default_path="", default_filename="", default_extension="", wildcard="*.*", flags=0, parent=None, x=-1, y=-1)
        self.textCtrlSequencia.SetValue(arquivo_da_sequencia)

    def OnButtonPDBButton(self, event):
        arquivo_do_pdb = wx.FileSelector("Select the PDB of template protein", default_path="", default_filename="", default_extension="", wildcard="*.pdb", flags=0, parent=None, x=-1, y=-1)
        self.textCtrlPDB.SetValue(arquivo_do_pdb)

    def OnButtonCancelarButton(self, event):
        self.Close()

    def OnButtonOKButton(self, event):
        self.sequence_filename = self.textCtrlSequencia.GetValue()
        # self.parent.ModificarTemplate.Enable(True)
        # self.parent.Alinhar.Enable(True)
        self.template_filename  = self.textCtrlPDB.GetValue()
        self.ok = True
        # self.parent.default_pathway_alinhar = False
        self.Close()

    def get_sequence_filename(self):
        return self.sequence_filename

    def get_template_filename(self):
        return self.template_filename



if __name__ == '__main__':
  pass
