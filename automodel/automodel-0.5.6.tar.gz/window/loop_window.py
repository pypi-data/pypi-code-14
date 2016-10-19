#Boa:Dialog:Refinamento_de_Loop

import wx
from modellingfile.pdb_file import *

def create(parent):
    return Refinamento_de_Loop(parent)

[wxID_REFINAMENTO_DE_LOOP, wxID_REFINAMENTO_DE_LOOPCANCELAR, 
 wxID_REFINAMENTO_DE_LOOPCHOICEDORESIDUOFINAL, 
 wxID_REFINAMENTO_DE_LOOPCHOICEDORESIDUOINICIAL, wxID_REFINAMENTO_DE_LOOPOK, 
 wxID_REFINAMENTO_DE_LOOPSTATICTEXT1, wxID_REFINAMENTO_DE_LOOPSTATICTEXT2, 
] = [wx.NewId() for _init_ctrls in range(7)]

class Refinamento_de_Loop(wx.Dialog):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Dialog.__init__(self, id=wxID_REFINAMENTO_DE_LOOP,
              name=u'Refinamento_de_Loop', parent=prnt, pos=wx.Point(334, 305),
              size=wx.Size(309, 147), style=wx.DEFAULT_DIALOG_STYLE,
              title=u'Loop Refinement')
        self.SetClientSize(wx.Size(309, 147))

        self.ChoicedoResiduoInicial = wx.Choice(choices=self.possible_residues(),
              id=wxID_REFINAMENTO_DE_LOOPCHOICEDORESIDUOINICIAL,
              name=u'ChoicedoResiduoInicial', parent=self, pos=wx.Point(160,
              30), size=wx.Size(80, 27), style=0)
        self.ChoicedoResiduoInicial.SetHelpText(u'')

        self.ChoicedoResiduoFinal = wx.Choice(choices=self.possible_residues(),
              id=wxID_REFINAMENTO_DE_LOOPCHOICEDORESIDUOFINAL,
              name=u'ChoicedoResiduoFinal', parent=self, pos=wx.Point(160, 62),
              size=wx.Size(80, 27), style=0)

        self.staticText1 = wx.StaticText(id=wxID_REFINAMENTO_DE_LOOPSTATICTEXT1,
              label=u'Start Residue', name='staticText1', parent=self,
              pos=wx.Point(30, 36), size=wx.Size(95, 17), style=0)

        self.staticText2 = wx.StaticText(id=wxID_REFINAMENTO_DE_LOOPSTATICTEXT2,
              label=u'End Residue', name='staticText2', parent=self,
              pos=wx.Point(32, 66), size=wx.Size(87, 17), style=0)

        self.Cancelar = wx.Button(id=wxID_REFINAMENTO_DE_LOOPCANCELAR,
              label=u'Cancel', name=u'Cancel', parent=self, pos=wx.Point(70,
              110), size=wx.Size(77, 27), style=0)
        self.Cancelar.Bind(wx.EVT_BUTTON, self.OnCancelarButton,
              id=wxID_REFINAMENTO_DE_LOOPCANCELAR)

        self.Ok = wx.Button(id=wxID_REFINAMENTO_DE_LOOPOK, label=u'Ok',
              name=u'Ok', parent=self, pos=wx.Point(156, 110), size=wx.Size(77,
              27), style=0)
        self.Ok.Bind(wx.EVT_BUTTON, self.OnOkButton,
              id=wxID_REFINAMENTO_DE_LOOPOK)

    def __init__(self, parent, generated_model):
    # def __init__(self, parent):
        # self.generated_model = generated_model
        self.pdb_file = self.__load_pdb_file__(generated_model)
        self.parent = parent
        self._init_ctrls(parent)

    def possible_residues(self):
      residue_list = []
      for residue_number in range(self.__set_choices_start__() ,self.__set_choices_end__()):
        residue_list.append(str(residue_number))
      return residue_list

    def __set_choices_start__(self):
      try:
        return self.pdb_file.start_residue()
      except:
        print "error at start"

    def __set_choices_end__(self):
      try:
        return self.pdb_file.end_residue()
      except:
        print "error at end"

    def __load_pdb_file__(self,pdb_file):
        pdb = None
        try:
          pdb = Pdb_File(pdb_file)
        except IOError:
          return pdb
        else:
          return pdb

    def OnCancelarButton(self, event):
        self.Destroy()

    def OnOkButton(self, event):
        loop_start = self.ChoicedoResiduoInicial.GetStringSelection()
        # print loop_start
        loop_end = self.ChoicedoResiduoFinal.GetStringSelection()
        self.parent.send_loop_refinament(loop_start,loop_end)
        self.Destroy()
