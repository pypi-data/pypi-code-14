'''
--------------------------------------------------------------------------
Copyright (C) 2016 Lukasz Laba <lukaszlab@o2.pl>

File version 0.7 date 2016-10-04

This file is part of SeePy.
SeePy is a python script visualisation tool.
http://seepy.org/

SeePy is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

SeePy is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Foobar; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
--------------------------------------------------------------------------
'''

import sys
import os
import subprocess
import traceback
import idlelib
import re
import codecs

from PyQt4 import QtCore, QtGui

import mistune

from pycore.Code import Code
from pycore.Shell import Shell
APP_PATH = os.path.dirname(os.path.abspath(__file__))

_appname = 'SeePy'
_version = '0.4.3 (4rd beta)'

class Main(QtGui.QMainWindow):

    def __init__(self):
        QtGui.QMainWindow.__init__(self, None)
        self.initUI()

    def initUI(self):
        # -- Main Toolbar --
        newAction = QtGui.QAction(QtGui.QIcon(abspath("icons/new.png")),"New",self)
        newAction.setShortcut("Ctrl+N")
        newAction.setStatusTip("Create new *.py script from template and set it as watched")
        newAction.triggered.connect(self.New)

        openAction = QtGui.QAction(QtGui.QIcon(abspath("icons/open.png")),"Open",self)
        openAction.setStatusTip("Open existing *.py script and set it as watched")
        openAction.setShortcut("Ctrl+O")
        openAction.triggered.connect(self.Open)
        
        saveAction = QtGui.QAction(QtGui.QIcon(abspath("icons/save.png")),"Save changes",self)
        saveAction.setStatusTip("Save changes to script file")
        saveAction.setShortcut("Ctrl+s")
        saveAction.triggered.connect(self.Save)

        savecopyAction = QtGui.QAction(QtGui.QIcon(abspath("icons/saveas.png")),"Save copy as",self)
        savecopyAction.setStatusTip("Save current script copy as same name and set it as watched")
        savecopyAction.triggered.connect(self.SaveCopy)

        reloadAction = QtGui.QAction(QtGui.QIcon(abspath("icons/reload.png")),"Reload",self)
        reloadAction.setStatusTip("Reload watched *.py script")
        reloadAction.setShortcut("F5")
        reloadAction.triggered.connect(self.Reload)

        editAction = QtGui.QAction(QtGui.QIcon(abspath("icons/edit.png")),"Edit",self)
        editAction.setStatusTip("It opens to edit current *.py script in standart Python IDLE")
        editAction.setShortcut("Ctrl+E")
        editAction.triggered.connect(self.Edit)

        showhtmlAction = QtGui.QAction(QtGui.QIcon(abspath("icons/showhtml.png")),"Show report as HTML",self)
        showhtmlAction.setStatusTip("It shows report as HTML code")
        showhtmlAction.triggered.connect(self.ShowHTML)

        showmarkdownAction = QtGui.QAction(QtGui.QIcon(abspath("icons/showmarkdown.png")),"Show report as Markdown",self)
        showmarkdownAction.setStatusTip("It shows report as Markdown code")
        showmarkdownAction.triggered.connect(self.ShowMarkdown)

        showsourceAction = QtGui.QAction(QtGui.QIcon(abspath("icons/showsource.png")),"Show python source",self)
        showsourceAction.setStatusTip("It shows python source code")
        showsourceAction.triggered.connect(self.ShowSource)
        
        showseepyAction = QtGui.QAction(QtGui.QIcon(abspath("icons/showseepy.png")),"Back to SeePy report",self)
        showseepyAction.setStatusTip("Back to SeePy report")
        showseepyAction.triggered.connect(self.ShowSeepy)

        previewmarkdownAction = QtGui.QAction(QtGui.QIcon(abspath("icons/previewmarkdown.png")),"Preview some Markdown",self)
        previewmarkdownAction.setStatusTip("You can preview some Markdown document - it not change watched *.py script")
        previewmarkdownAction.triggered.connect(self.PreviewMarkdown)

        savemarkdownAction = QtGui.QAction(QtGui.QIcon(abspath("icons/savemarkdown.png")),"Save report as Markdown file",self)
        savemarkdownAction.setStatusTip("Save report as Markdown file")
        savemarkdownAction.triggered.connect(self.SaveMarkdown)

        printAction = QtGui.QAction(QtGui.QIcon(abspath("icons/print.png")),"Print document",self)
        printAction.setStatusTip("Print document")
        printAction.setShortcut("Ctrl+P")
        printAction.triggered.connect(self.Print)

        helpAction = QtGui.QAction(QtGui.QIcon(abspath("icons/help.png")),"Help",self)
        helpAction.setStatusTip("Help information")
        helpAction.setShortcut("F1")
        helpAction.triggered.connect(self.Help)

        aboutAction = QtGui.QAction(QtGui.QIcon(abspath("icons/about.png")),"About SeePy",self)
        aboutAction.setStatusTip("SeePy project information")
        aboutAction.triggered.connect(self.About)

        tutorialAction = QtGui.QAction(QtGui.QIcon(abspath("icons/tutorial.png")),"Tutorial",self)
        tutorialAction.setStatusTip("Open tutorial script")
        tutorialAction.triggered.connect(self.Tutorial)

        syntaxAction = QtGui.QAction(QtGui.QIcon(abspath("icons/syntax.png")),"Syntax help",self)
        syntaxAction.setStatusTip("Show SeePy syntax help")
        syntaxAction.setShortcut("F2")
        syntaxAction.triggered.connect(self.Syntax)
        
        floatprecisionAction = QtGui.QAction(QtGui.QIcon(" "),"Float precision",self)
        floatprecisionAction.setStatusTip("Set float display precision")
        floatprecisionAction.triggered.connect(self.Floatprecision)
        
        self.watchRadioButton = QtGui.QRadioButton('watch script', self)
        self.watchRadioButton.setStatusTip("If active report will be reloaded after script file change")
        
        self.toolbar = self.addToolBar("Main")
        self.toolbar.addAction(newAction)
        self.toolbar.addAction(openAction)
        self.toolbar.addAction(saveAction)
        self.toolbar.addSeparator()
        self.toolbar.addAction(reloadAction)
        self.toolbar.addWidget(self.watchRadioButton)
        self.toolbar.addSeparator()
        self.toolbar.addAction(editAction)
        self.toolbar.addSeparator()
        self.toolbar.addAction(printAction)
        self.toolbar.addAction(savemarkdownAction)
        self.toolbar.addSeparator()
        self.toolbar.addAction(showsourceAction)
        self.toolbar.addAction(showhtmlAction)
        self.toolbar.addAction(showmarkdownAction)
        self.toolbar.addAction(showseepyAction)
        self.toolbar.addSeparator()
        self.toolbar.addAction(previewmarkdownAction)
        self.toolbar.addSeparator()
        self.toolbar.addAction(syntaxAction)
        self.toolbar.addSeparator()
        
        self.toolbar_light = self.addToolBar("Light")
        self.toolbar_light.addAction(saveAction)
        self.toolbar_light.addAction(savecopyAction)
        self.toolbar_light.addAction(printAction)
        self.toolbar_light.setVisible(False)

        # -- Text Browser --
        self.textBrowser = QtGui.QTextBrowser(self)
        self.setCentralWidget(self.textBrowser)
        self.textBrowser.anchorClicked.connect(self.on_anchor_clicked)

        # -- Statusbar --
        self.status = self.statusBar()

        # --Window settings --
        self.setGeometry(100, 100, 720, 700)
        self.setWindowIcon(QtGui.QIcon("icons/logo.png"))
        self.show()

        # -- Menubar --
        self.menubar = self.menuBar()
        #---
        file = self.menubar.addMenu("File")
        file.addAction(newAction)
        file.addAction(openAction)
        file.addAction(saveAction)
        file.addAction(savecopyAction)
        file.addAction(printAction)
        #---
        export = self.menubar.addMenu("Script")
        export.addAction(reloadAction)
        export.addAction(editAction)
        export.addAction(showhtmlAction)
        export.addAction(showmarkdownAction)
        export.addAction(showmarkdownAction)
        export.addAction(showseepyAction)
        export.addAction(floatprecisionAction)
        #---
        info = self.menubar.addMenu("Info")
        info.addAction(aboutAction)
        info.addAction(helpAction)
        info.addAction(syntaxAction)
        info.addAction(tutorialAction)
        
    def closeEvent(self, event):
        Environment.delete_tmpfile() #Cleaning SeePy tmp files
        event.accept()

    def New(self):
        template_path = abspath('templates/x_newtemplate.py')
        ScriptCode.newFile(template_path, 'Save new script as', 'newScript.py')
        setWatcher()
        AppReload()

    def Open(self, file_path = None):
        if ScriptCode.script_path:
            Environment.delete_tmpfile() #Cleaning SeePy tmp files
        ScriptCode.openFile(file_path)
        setWatcher()
        AppReload()

    def Save(self):
        if ScriptCode.script_path :
            ScriptCode.savecode()
            QtGui.QMessageBox.information(None, 'Info', 'Saved to '+ ScriptCode.script_path)
        else:
            QtGui.QMessageBox.information(None, 'Info', 'Please create or open script first')
        
    def SaveCopy(self):
        if ScriptCode.script_path :
            newName = 'Copy_' + os.path.basename(ScriptCode.script_path)
            ScriptCode.newFile(ScriptCode.script_path, 'Save copy script as', newName)
            setWatcher()
            AppReload()
            QtGui.QMessageBox.information(None, 'Info', 'Saved to '+ ScriptCode.script_path)
        else:
            QtGui.QMessageBox.information(None, 'Info', 'Please create or open script first')

    def Reload(self):
        if ScriptCode.script_path :
            ScriptCode.reloadcode()
            AppReload()
        else:
            QtGui.QMessageBox.information(None, 'Info', 'Please create or open script first')

    def Edit(self):
        if ScriptCode.script_path :
            IDLEpath = vars(idlelib)['__path__'][0] + '/idle.pyw'
            subprocess.Popen(['python', IDLEpath, ScriptCode.script_path])
        else:
            QtGui.QMessageBox.information(None, 'Info', 'Please create or open script first')

    def ShowHTML(self):
        if ScriptCode.script_path :
            show_somecode(Environment.report_html)
        else:
            QtGui.QMessageBox.information(None, 'Info', 'Please create or open script first')

    def ShowSource(self):
        if ScriptCode.script_path :
            show_somecode(ScriptCode.code_oryginal)
        else:
            QtGui.QMessageBox.information(None, 'Info', 'Please create or open script first')

    def ShowMarkdown(self):
        if ScriptCode.script_path :
            show_somecode(Environment.report_markdown)
        else:
            QtGui.QMessageBox.information(None, 'Info', 'Please create or open script first')
            
    def ShowSeepy(self):
        if ScriptCode.script_path :
            self.textBrowser.setHtml(codecs.decode(Environment.report_html, 'utf-8'))
        else:
            QtGui.QMessageBox.information(None, 'Info', 'Please create or open script first')

    def PreviewMarkdown(self):
        #---asking for file path
        filename = QtGui.QFileDialog.getOpenFileName(caption = 'Open Marktdown document',
                                                directory = ScriptCode.savedir,
                                                filter = "Markdown document (*.md)")
        filename = str(filename)
        #---
        show_markdown_file(filename)

    def SaveMarkdown(self):
        if ScriptCode.script_path :
            initname = os.path.basename(ScriptCode.script_path).replace('.py', '.md')
            Environment.save_report_markdown(ScriptCode.savedir, initname)
        else:
            QtGui.QMessageBox.information(None, 'Info', 'Please create or open script first')

    def Print(self):
        dialog = QtGui.QPrintDialog()
        if dialog.exec_() == QtGui.QDialog.Accepted:
            self.textBrowser.document().print_(dialog.printer())

    def Help(self):
        show_markdown_file(abspath('memos/x_help.md'))

    def About(self):
        show_markdown_file(abspath('memos/x_about.md'))

    def Tutorial(self):
        tutorial_path = abspath('memos/x_tutorial.py')
        os.path.dirname(os.path.abspath(__file__))
        ScriptCode.newFile(tutorial_path, '', 'tmp_seepy_tutorial.py', os.path.dirname(tutorial_path))
        setWatcher()
        AppReload()
        self.Edit()

    def Syntax(self):
        show_markdown_file(abspath('memos/x_syntax.md'))
        
    def Floatprecision(self):
        if ScriptCode.script_path :
            #---asking for precision as int number
            value = QtGui.QInputDialog.getInteger(  None, 
                                                    'Float display precysion', 'Set the precison:',
                                                    value = Environment.float_display_precison,
                                                    min = 1, max = 9, step = 1)[0]
            #---
            Environment.float_display_precison = value
            AppReload()
        else:
            QtGui.QMessageBox.information(None, 'Info', 'Please create or open script first')
        
    def on_anchor_clicked(self,url):
        link = str(url.toString())
        line_id = link.split(';')[0]
        setvalues = link.split(';')[1]
        index = link.split(';')[2]
        scrol_value = myapp.textBrowser.verticalScrollBar().value()
        self.textBrowser.setSource(QtCore.QUrl())
        myapp.textBrowser.verticalScrollBar().setValue(scrol_value)
        tmp = ScriptCode.code_oryginal
        ScriptCode.editCode(line_id, setvalues, index)
        if AppReload():
            pass
        else:
            ScriptCode.code_oryginal = tmp
            
def AppReload ():
    QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
    successruned = True
    try:
        ScriptCode.parse()
        Environment.run_parsed()
        #---
        scrol_value = myapp.textBrowser.verticalScrollBar().value()
        #---
        myapp.textBrowser.clear()
        myapp.textBrowser.setHtml(codecs.decode(Environment.report_html, 'utf-8'))
        myapp.textBrowser.reload()
        #---
        myapp.textBrowser.verticalScrollBar().setValue(scrol_value)
        #---
        QtGui.QApplication.restoreOverrideCursor()
    except Exception as e:
        successruned = False
        QtGui.QApplication.restoreOverrideCursor()
        QtGui.QMessageBox.information(None, 'Some problem - ' + str(e), str(traceback.format_exc()))
    #---
    myapp.setWindowTitle(_appname + ' ' + _version + ' - ' + os.path.basename(ScriptCode.script_path))
    return successruned

@QtCore.pyqtSlot(str)
def script_changed(path):
    if myapp.watchRadioButton.isChecked():
        ScriptCode.reloadcode()
        AppReload()

def setWatcher():
    global fs_watcher
    fs_watcher = None
    fs_watcher = QtCore.QFileSystemWatcher([ScriptCode.script_path])
    fs_watcher.connect(fs_watcher, QtCore.SIGNAL('fileChanged(QString)'), script_changed)

def show_somecode(code):
    code = "````\n" + code + "\n````"
    code_html = mistune.markdown(code)
    myapp.textBrowser.setHtml(codecs.decode(code_html, 'utf-8'))

def show_markdown(markdown):
    code_html = mistune.markdown(markdown)
    #myapp.textBrowser.setHtml(code_html)
    myapp.textBrowser.setHtml(codecs.decode(code_html, 'utf-8'))

def show_markdown_file(abspath):
    markdown = open(abspath, 'r').read()
    #----replaceing path to images inside markdown
    dir =  os.path.dirname(abspath)
    markdown = re.sub(  r'!\[(.+)\]\((.+)\)', 
                        r"![\1]({0}/\2)".format(os.path.join(dir, '')), 
                        markdown)
    #----
    show_markdown(markdown)

def abspath(relpath):
    return os.path.join(APP_PATH, relpath)

def main():
    global myapp
    global ScriptCode
    global Environment
    #--PyQt objects
    app = QtGui.QApplication(sys.argv)
    myapp = Main()
    #----
    ScriptCode = Code()
    Environment = Shell()
    #---assigning code to shell
    Environment.assign_code(ScriptCode)
    #---init script dir for open dialog
    ScriptCode.savedir = APP_PATH
    #---report end stamp
    ScriptCode.stamptext = 'Created with ' + _appname + ' ' + _version
    #---app start view
    myapp.setWindowTitle(_appname + ' ' + _version)
    show_markdown_file(abspath('memos/x_startpage.md'))
    #----runing options from argv
    if len(sys.argv) == 1:
        sys.argv.append(None)
        sys.argv.append(None)
    if len(sys.argv) == 2:
        sys.argv.append(None)
    if sys.argv[1]:   #if file path to open exist open it
        path_to_open = sys.argv[1]
        myapp.Open(path_to_open)
    if sys.argv[2] == '-f':   # opening as full mode if -f
        None
    if sys.argv[2] == '-l':   # opening as light mode if -l
        myapp.toolbar_light.setVisible(True)
        myapp.toolbar.setVisible(False)
        myapp.menubar.setVisible(False)
    #----runing QT 
    myapp.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()