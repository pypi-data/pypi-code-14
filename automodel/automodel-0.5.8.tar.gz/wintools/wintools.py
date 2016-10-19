#Filename: wintools.py
#Criado Por Joao Luiz de Almeida Filho
#16-07-09
import wx

class padrao():
    def createText(self, panel):
        for eachLabel, eachPos in self.textData():
            self.createOneText(panel, eachLabel, eachPos)
    def createOneText(self, panel, label, pos):
	    self.statictext[label] = wx.StaticText(panel, wx.NewId(), label, pos)
    def createTextFields(self, panel):
        for eachLabel, eachPos in self.textFieldData():
            self.createCaptionedText(panel, eachLabel, eachPos)  
    def createCaptionedText(self, panel, label, pos):
        static = wx.StaticText(panel, wx.NewId(), label, pos)
        static.SetBackgroundColour("White")
        textPos = (pos[0] + 130, pos[1])    
        if((label != "Target Sequence:") and (label != "Selected Template:") and (label != "Sequencia: ")):
            self.TextField[label] =  wx.TextCtrl(panel, wx.NewId(), "", size=(300,-1), pos=textPos)
        else:
            if(label != "Sequencia: "):
                self.TextField[label] = wx.TextCtrl(panel, wx.NewId(), "", style=wx.TE_MULTILINE, pos=textPos, size=(600, 250))
            else:
                self.TextField[label] = wx.TextCtrl(panel, wx.NewId(), "", style=wx.TE_MULTILINE, pos=textPos, size=(300, 250))
    def createManyRadios(self, panel):
        for eachLabel, eachPos in self.radioData():
           self.radio[eachLabel] = self.buildOneRadio(panel, eachLabel, eachPos)
           self.Bind(wx.EVT_RADIOBUTTON, self.OnRadio, self.radio[eachLabel])

    def createMuchButtons(self,panel):
        for eachLabel, eachHandler, eachPos in self.buttonData():
            self.button[eachLabel] = self.buildOneButton(panel, eachLabel, eachHandler, eachPos)
    def buildOneButton(self, parent, label, handler, pos=(0,0)):
        button = wx.Button(parent, -1, label, pos)
        self.Bind(wx.EVT_BUTTON, handler, button)
        return button
    def buildOneRadio(self,parent, label, pos=(0,0)):
        radio = wx.RadioButton(parent, -1, label, pos = pos, name = label)
        return radio
    def OnCloseWindow(self, event):
        self.Destroy()	
    def createOnePullDown(self, panel,posX, posY,   list):
        pulldown = wx.Choice(panel, -1,  pos = (posX, posY), size=(65,-1),   choices = list)
        pulldown.SetSelection(0)
        return pulldown

	    
class wintools(padrao, wx.Frame):
	pass
class subwintools(padrao, wx.Dialog):
	pass
#End of wintools

