#Boa:MiniFrame:SelectAutoModelMode


import wx
from model.AutoModelMode import AutoModelMode
from options.Prefs import Prefs

def create(parent):
    return SelectAutoModelMode(parent)

[wxID_SELECTAUTOMODELMODE, wxID_SELECTAUTOMODELMODEBUTTONOK, 
 wxID_SELECTAUTOMODELMODECANCELBUTTON, 
 wxID_SELECTAUTOMODELMODERADIOBUTTONCLIENTMODE, 
 wxID_SELECTAUTOMODELMODERADIOBUTTONOFFLINEMODE, 
 wxID_SELECTAUTOMODELMODESTATICBOX1, 
] = [wx.NewId() for _init_ctrls in range(6)]

class SelectAutoModelMode(wx.MiniFrame):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.MiniFrame.__init__(self, id=wxID_SELECTAUTOMODELMODE,
              name=u'SelectAutoModelMode', parent=prnt, pos=wx.Point(523, 420),
              size=wx.Size(400, 150), style=wx.DEFAULT_FRAME_STYLE,
              title=u'Select the AutoModel Mode')
        self.SetClientSize(wx.Size(400, 150))

        self.staticBox1 = wx.StaticBox(id=wxID_SELECTAUTOMODELMODESTATICBOX1,
              label=u'Select AutoModel Mode:', name='staticBox1', parent=self,
              pos=wx.Point(0, 0), size=wx.Size(400, 150), style=0)

        self.radioButtonClientMode = wx.RadioButton(id=wxID_SELECTAUTOMODELMODERADIOBUTTONCLIENTMODE,
              label=u'Client Mode', name=u'radioButtonClientMode', parent=self,
              pos=wx.Point(136, 56), size=wx.Size(107, 21), style=0)
        self.radioButtonClientMode.SetValue(True)
        self.radioButtonClientMode.Bind(wx.EVT_RADIOBUTTON,
              self.OnRadioButton1Radiobutton,
              id=wxID_SELECTAUTOMODELMODERADIOBUTTONCLIENTMODE)

        self.radioButtonOfflineMode = wx.RadioButton(id=wxID_SELECTAUTOMODELMODERADIOBUTTONOFFLINEMODE,
              label=u'Offline Mode', name=u'radioButtonOfflineMode',
              parent=self, pos=wx.Point(136, 80), size=wx.Size(107, 21),
              style=0)
        self.radioButtonOfflineMode.SetValue(False)
        self.radioButtonOfflineMode.Bind(wx.EVT_RADIOBUTTON,
              self.OnRadioButton2Radiobutton,
              id=wxID_SELECTAUTOMODELMODERADIOBUTTONOFFLINEMODE)

        self.buttonOk = wx.Button(id=wxID_SELECTAUTOMODELMODEBUTTONOK,
              label=u'Ok', name=u'buttonOk', parent=self, pos=wx.Point(192,
              116), size=wx.Size(85, 27), style=0)
        self.buttonOk.Bind(wx.EVT_BUTTON, self.OnButtonOkButton,
              id=wxID_SELECTAUTOMODELMODEBUTTONOK)

        self.cancelButton = wx.Button(id=wxID_SELECTAUTOMODELMODECANCELBUTTON,
              label=u'Cancel', name=u'cancelButton', parent=self,
              pos=wx.Point(88, 116), size=wx.Size(85, 27), style=0)
        self.cancelButton.Bind(wx.EVT_BUTTON, self.OnCancelButtonButton,
              id=wxID_SELECTAUTOMODELMODECANCELBUTTON)

    def __init__(self, parent):
        self._init_ctrls(parent)
        self.myMode = AutoModelMode()

    def OnRadioButton1Radiobutton(self, event):
        event.Skip()

    def OnRadioButton2Radiobutton(self, event):
        event.Skip()

    def OnButtonOkButton(self, event):
        if self.radioButtonClientMode:
            self.myMode.online_mode()
        else:
            self.myMode.offline_mode()

    def OnCancelButtonButton(self, event):
        self.myMode.offline_mode()