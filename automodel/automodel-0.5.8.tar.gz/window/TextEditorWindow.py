#Boa:Frame:TextEditor

import wx
import wx.richtext
import os

def create(parent):
    return TextEditor(parent)

[wxID_TEXTEDITOR, wxID_TEXTEDITORDECREASEFONTBUTTON, 
 wxID_TEXTEDITORINCREASEFONTBUTTON, wxID_TEXTEDITORPANEL1, 
 wxID_TEXTEDITORSAVE, wxID_TEXTEDITORSAVEAS, 
 wxID_TEXTEDITORTEXTCONTROLOFFILETEXT, 
] = [wx.NewId() for _init_ctrls in range(7)]

class TextEditor(wx.Frame):
    def _init_coll_gridSizer1_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.Save, 0, border=10, flag=wx.ALL)
        parent.AddWindow(self.SaveAs, 0, border=10, flag=wx.ALL)
        parent.AddSpacer(wx.Size(8, 8), border=0, flag=0)
        parent.AddWindow(self.IncreaseFontButton, 0, border=10, flag=wx.ALL)
        parent.AddWindow(self.DecreaseFontButton, 0, border=10, flag=wx.ALL)

    def _init_coll_boxSizer1_Items(self, parent):
        # generated method, don't edit

        parent.AddSizer(self.gridSizer1, 0, border=0, flag=0)
        parent.AddWindow(self.TextControlOfFileText, 1, border=10,
              flag=wx.ALL | wx.EXPAND)

    def _init_sizers(self):
        # generated method, don't edit
        self.boxSizer1 = wx.BoxSizer(orient=wx.VERTICAL)

        self.gridSizer1 = wx.GridSizer(cols=0, hgap=0, rows=1, vgap=0)

        self._init_coll_boxSizer1_Items(self.boxSizer1)
        self._init_coll_gridSizer1_Items(self.gridSizer1)

        self.panel1.SetSizer(self.boxSizer1)

    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Frame.__init__(self, id=wxID_TEXTEDITOR, name=u'TextEditor',
              parent=prnt, pos=wx.Point(361, 151), size=wx.Size(913, 597),
              style=wx.DEFAULT_FRAME_STYLE, title=u'AutoModel Text Editor')
        self.SetClientSize(wx.Size(913, 597))
        self.Bind(wx.EVT_CLOSE, self.OnTextEditorClose)

        self.panel1 = wx.Panel(id=wxID_TEXTEDITORPANEL1, name='panel1',
              parent=self, pos=wx.Point(0, 0), size=wx.Size(913, 597),
              style=wx.TAB_TRAVERSAL)

        self.TextControlOfFileText = wx.richtext.RichTextCtrl(id=wxID_TEXTEDITORTEXTCONTROLOFFILETEXT,
              parent=self.panel1, pos=wx.Point(10, 57), size=wx.Size(893, 530),
              style=wx.richtext.RE_MULTILINE, value=u'')
        self.TextControlOfFileText.SetLabel(u'')
        self.TextControlOfFileText.Bind(wx.EVT_CHAR,
              self.OnTextControlOfFileTextChar)

        self.Save = wx.Button(id=wxID_TEXTEDITORSAVE, label=u'Save',
              name=u'Save', parent=self.panel1, pos=wx.Point(10, 10),
              size=wx.Size(85, 27), style=0)
        self.Save.Bind(wx.EVT_BUTTON, self.OnSaveButton, id=wxID_TEXTEDITORSAVE)

        self.SaveAs = wx.Button(id=wxID_TEXTEDITORSAVEAS, label=u'Save As...',
              name=u'SaveAs', parent=self.panel1, pos=wx.Point(115, 10),
              size=wx.Size(85, 27), style=0)
        self.SaveAs.Bind(wx.EVT_BUTTON, self.OnSaveAsButton,
              id=wxID_TEXTEDITORSAVEAS)

        self.IncreaseFontButton = wx.Button(id=wxID_TEXTEDITORINCREASEFONTBUTTON,
              label=u'A+', name=u'IncreaseFontButton', parent=self.panel1,
              pos=wx.Point(325, 10), size=wx.Size(85, 27), style=0)
        self.IncreaseFontButton.Bind(wx.EVT_BUTTON,
              self.OnIncreaseFontButtonButton,
              id=wxID_TEXTEDITORINCREASEFONTBUTTON)

        self.DecreaseFontButton = wx.Button(id=wxID_TEXTEDITORDECREASEFONTBUTTON,
              label=u'A-', name=u'DecreaseFontButton', parent=self.panel1,
              pos=wx.Point(430, 10), size=wx.Size(85, 27), style=0)
        self.DecreaseFontButton.Bind(wx.EVT_BUTTON,
              self.OnDecreaseFontButtonButton,
              id=wxID_TEXTEDITORDECREASEFONTBUTTON)

        self._init_sizers()

    def __init__(self, parent, text_file_name):
        self._init_ctrls(parent)
        self.text_file_name = text_file_name
        self.text_file_read = file(text_file_name, "r")
        self.text_of_file = ""
        self.size_font = 9
        fonte = wx.Font(self.size_font,  wx.MODERN, wx.NORMAL,  True)
        self.TextControlOfFileText.SetFont(fonte)
        self.content_was_modified = False
        for Line in self.text_file_read.readlines():
          self.text_of_file = self.text_of_file + Line
        self.TextControlOfFileText.SetValue(self.text_of_file)
        self.SetTitle(os.path.basename(self.text_file_name))

    def OnSaveButton(self, event):
        self.__save__()

    def __save__(self):
        self.content_was_modified = False
        new_text = self.TextControlOfFileText.GetValue()
        self.text_file_read.close()
        text_file = file( self.text_file_name, "w")
        text_file.seek(0)
        text_file.write(new_text)
        text_file.close()
        self.text_file_read = file(self.text_file_name, "r")

    def OnSaveAsButton(self, event):
        new_text = self.TextControlOfFileText.GetValue()
        dialog = wx.FileDialog(None, "Save in", defaultFile= self.text_file_name,
          style=wx.FD_SAVE)
        if dialog.ShowModal() == wx.ID_OK:
            self.text_file_read.close()
            path_of_new_file = dialog.GetPath()
            new_file = file(path_of_new_file, "w")
            new_file.seek(0)
            new_file.write(new_text)
            new_file.close()
            self.text_file_name = path_of_new_file
            self.text_file_read = file(self.text_file_name, "r+")

    def OnTextEditorClose(self, event):
        new_text = self.TextControlOfFileText.GetValue()
        # print new_text
        # print self.text_of_file
        if self.content_was_modified:
          dlg = wx.MessageDialog(self,
               "Do want save the modifications?",
               "Confirm Exit", wx.YES|wx.NO|wx.ICON_QUESTION)
          result = dlg.ShowModal()
          if result == wx.ID_YES:
              self.__save__()
              self.Destroy()
          else:
              self.Destroy()
        else:
          self.Destroy()


    def OnIncreaseFontButtonButton(self, event):
       if self.size_font < 50:
          self.size_font = self.size_font + 1
          fonte = wx.Font(self.size_font,  wx.MODERN, wx.NORMAL,  True)
          self.TextControlOfFileText.SetFont(fonte)         

    def OnDecreaseFontButtonButton(self, event):
       if self.size_font > 0:
          self.size_font = self.size_font - 1
          fonte = wx.Font(self.size_font,  wx.MODERN, wx.NORMAL,  True)
          self.TextControlOfFileText.SetFont(fonte) 

    # def OnTextControlOfFileTextChar(self, event):
    #     self.content_was_modified = True

    def OnTextControlOfFileTextChar(self, event):
        self.content_was_modified = True
        event.Skip()
        



