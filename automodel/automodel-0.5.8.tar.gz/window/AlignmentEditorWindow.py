#Boa:MiniFrame:AlignmentEditorWindow

import wx
import wx.richtext

def create(parent):
    return AlignmentEditorWindow(parent)

[wxID_ALIGNMENTEDITORWINDOW, wxID_ALIGNMENTEDITORWINDOWBUTTONSAVE, 
 wxID_ALIGNMENTEDITORWINDOWTEXTCTRLOFALIGNMENT, 
] = [wx.NewId() for _init_ctrls in range(3)]

class AlignmentEditorWindow(wx.MiniFrame):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.MiniFrame.__init__(self, id=wxID_ALIGNMENTEDITORWINDOW,
              name=u'AlignmentEditorWindow', parent=prnt, pos=wx.Point(368,
              209), size=wx.Size(707, 482), style=wx.DEFAULT_FRAME_STYLE,
              title=u'Alignment Editor')
        self.SetClientSize(wx.Size(707, 482))

        self.TextCtrlOfAlignment = wx.richtext.RichTextCtrl(id=wxID_ALIGNMENTEDITORWINDOWTEXTCTRLOFALIGNMENT,
              parent=self, pos=wx.Point(0, 48), size=wx.Size(712, 432),
              style=wx.richtext.RE_MULTILINE, value=u'')
        self.TextCtrlOfAlignment.SetLabel(u'')
        self.TextCtrlOfAlignment.SetAutoLayout(False)
        self.TextCtrlOfAlignment.SetName(u'TextCtrlOfAlignment')

        self.ButtonSave = wx.Button(id=wxID_ALIGNMENTEDITORWINDOWBUTTONSAVE,
              label=u'Save...', name=u'ButtonSave', parent=self,
              pos=wx.Point(10, 12), size=wx.Size(85, 27), style=0)

    def __init__(self, parent):
        self._init_ctrls(parent)
