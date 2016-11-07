from tkinter import *
import tkinter.font
import tkinter.messagebox

def get_screen_size(window):  
    return window.winfo_screenwidth(),window.winfo_screenheight()  
  
def get_window_size(window):  
    return window.winfo_reqwidth(),window.winfo_reqheight()  
  
def center_window(root):  
    root.update()
    curWidth = root.winfo_reqwidth()
    curHeight = root.winfo_height()
    scnWidth,scnHeight = root.maxsize()
    root.geometry('%dx%d+%d+%d'%(curWidth,curHeight,(scnWidth-curWidth)/2,(scnHeight-curHeight)/2))

class Dc_messagebox():
    def __init__(self, result, title_data = "", info_data = ""):
        self.root = Tk()
        self.root.resizable(False, False)
        self.root.title(title_data)
        frame = Frame(self.root)
        frame.pack()
        self.label_name3 = Label(frame, text="", fg="#00BFFF", bg="#FFFFFF")
        self.label_name3.config(font=tkinter.font.Font(family='Microsfot YaHei', size=24, weight=tkinter.font.BOLD))
        self.label_name3.pack(fill=BOTH)
        self.label_name = Label(frame, text=info_data, fg="#00BFFF", bg="#FFFFFF")
        self.label_name.config(font=tkinter.font.Font(family='Microsfot YaHei', size=48, weight=tkinter.font.BOLD))
        self.label_name.pack(fill = BOTH)
        self.label_name2 = Label(frame, text="", fg="#00BFFF", bg="#FFFFFF")
        self.label_name2.config(font=tkinter.font.Font(family='Microsfot YaHei', size=24, weight=tkinter.font.BOLD))
        self.label_name2.pack(fill=BOTH)
        buttonFrame = Frame(self.root)
        buttonFrame.pack(fill = X, side = BOTTOM)
        self.button_ok = Button(buttonFrame,text = "是", command = lambda:self.clickYes(result), fg="#FFFFFF", bg="#00BFFF", font=tkinter.font.Font(family = 'Microsfot YaHei',size = 24,weight = tkinter.font.BOLD))
        self.button_ok.pack(expand = True, fill = X, side = LEFT)
        self.button_cancel = Button(buttonFrame,text = "否", command = lambda:self.clickNo(result), fg="#FFFFFF", bg="#00BFFF", font=tkinter.font.Font(family = 'Microsfot YaHei',size = 24,weight = tkinter.font.BOLD))
        self.button_cancel.pack(expand = True, fill = X, side = RIGHT)
        center_window(self.root)
        self.root.mainloop()

    def clickYes(self, result):
        result.append(YES)
        self.root.destroy()

    def clickNo(self, result):
        result.append(NO)
        self.root.destroy()
