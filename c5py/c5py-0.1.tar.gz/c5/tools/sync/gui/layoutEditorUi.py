# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'LayoutEditor.ui'
#
# Created: Fri Feb 24 10:45:00 2012
#      by: PyQt4 UI code generator 4.7.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_LayoutDialog(object):
    def setupUi(self, LayoutDialog):
        LayoutDialog.setObjectName("LayoutDialog")
        LayoutDialog.resize(401, 266)
        self.verticalLayout = QtGui.QVBoxLayout(LayoutDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.preview = LayoutPreview(LayoutDialog)
        self.preview.setObjectName("preview")
        self.verticalLayout.addWidget(self.preview)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lineEdit = QtGui.QLineEdit(LayoutDialog)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        self.pushButton = QtGui.QPushButton(LayoutDialog)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(LayoutDialog)
        QtCore.QMetaObject.connectSlotsByName(LayoutDialog)

    def retranslateUi(self, LayoutDialog):
        LayoutDialog.setWindowTitle(QtGui.QApplication.translate("LayoutDialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("LayoutDialog", "PushButton", None, QtGui.QApplication.UnicodeUTF8))

from layout_preview import LayoutPreview
