#!/usr/bin/env python3

__version__ = "0.1.2"

from PyQt4 import QtCore, QtGui

try:
    from linkbot_serialid_tool.dialog import Ui_Dialog
except:
    from dialog import Ui_Dialog

import linkbot3 as linkbot
import sys
import time

class StartQT4(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.setWindowTitle('Linkbot Serial-ID Tool')

        self.ui.buttonBox.accepted.connect(self.accepted)
        self.ui.buttonBox.clicked.connect(self.buttonBoxClicked)
        self.ui.getId_pushButton.clicked.connect(self.getCurrentId)
        self.ui.selectAll_pushButton.clicked.connect(
            self.ui.serialId_lineEdit.selectAll)
        self.ui.serialId_lineEdit.returnPressed.connect(
            self.programCurrentSerialId)

    def accepted(self):
        try:
            self.programCurrentSerialId()
            sys.exit(0)
        except Exception as e:
            QtGui.QMessageBox.warning(self, "Error: ", str(e))

    def buttonBoxClicked(self, button):
        role = self.ui.buttonBox.buttonRole(button)
        try:
            if role == self.ui.buttonBox.RejectRole:
                sys.exit(0)
            elif role == self.ui.buttonBox.ResetRole:
                self.ui.serialId_lineEdit.setText('')
            elif role == self.ui.buttonBox.ApplyRole:
                self.programCurrentSerialId()
        except Exception as e:
            QtGui.QMessageBox.warning(self, "Error: ", str(e))

    def programCurrentSerialId(self):
        try:
            l = linkbot.CLinkbot('LOCL')
        except:
            try:
                linkbot.config(use_sfp=True)
                l = linkbot.CLinkbot('LOCL')
            except Exception as e:
                QtGui.QMessageBox.warning(self, "Error: ", str(e))
                return
        
        newId = self.ui.serialId_lineEdit.text().upper()
        if len(newId) != 4:
            raise Exception("Serial IDs must be 4 characters long.")
        l._set_serial_id(newId)
        l.setBuzzerFrequency(440)
        time.sleep(0.5)
        l.setBuzzerFrequency(0)
        self.ui.serialId_lineEdit.selectAll()

    def getCurrentId(self):
        try:
            l = linkbot.CLinkbot('LOCL')
            QtGui.QMessageBox.information(self, "Serial ID", "Serial ID: " + l.get_serial_id())
        except Exception as e:
            try:
                # Try using SFP
                linkbot.config(use_sfp = True)
                l = linkbot.CLinkbot('LOCL')
                QtGui.QMessageBox.information(self, "Serial ID", "Serial ID: " + l.get_serial_id())
            except Exception as e2:
                QtGui.QMessageBox.warning(
                    self,
                    "Warning", 
                    "Could not get the Linkbot's serial ID. Is the Linkbot plugged "
                    "in?\n\n" + str(e) + str(e2))

def main():
    app = QtGui.QApplication(sys.argv)
    myapp = StartQT4()
    myapp.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
