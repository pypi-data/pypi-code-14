# -*- coding: utf-8 -*-


from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_WAbout(object):
    def setupUi(self, WAbout):
        WAbout.setObjectName("WAbout")
        WAbout.setWindowModality(QtCore.Qt.ApplicationModal)
        WAbout.resize(868, 664)
        self.verticalLayout = QtWidgets.QVBoxLayout(WAbout)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.label = QtWidgets.QLabel(WAbout)
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap(":/medeval"))
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.aboutLabel = QtWidgets.QLabel(WAbout)
        self.aboutLabel.setObjectName("aboutLabel")
        self.horizontalLayout_3.addWidget(self.aboutLabel)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem3)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem4)
        self.aboutQtButton = QtWidgets.QPushButton(WAbout)
        self.aboutQtButton.setObjectName("aboutQtButton")
        self.horizontalLayout.addWidget(self.aboutQtButton)
        self.closeButton = QtWidgets.QPushButton(WAbout)
        self.closeButton.setObjectName("closeButton")
        self.horizontalLayout.addWidget(self.closeButton)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(WAbout)
        QtCore.QMetaObject.connectSlotsByName(WAbout)

    def retranslateUi(self, WAbout):
        _translate = QtCore.QCoreApplication.translate
        WAbout.setWindowTitle(_translate("WAbout", "About MEDVED"))
        self.aboutLabel.setText(_translate("WAbout", "<html><head/><body><p>MEDVED (Modelation-Enhanced Viewer and EDitor)</p><p>(c) Vadim Dyadkin, 2016</p><p>This program is licensed under GPL v3</p><p>Mercurial repository: <a href=\"http://hg.3lp.cx/medved\"><span style=\" text-decoration: underline; color:#0057ae;\">http://hg.3lp.cx/medved</span></a></p><p>Mercurial hash: @</p><p>When you use this software, please quote the following reference:</p><p><a href=\"http://dx.doi.org/10.1107/S1600577516002411\"><span style=\" text-decoration: underline; color:#0057ae;\">http://dx.doi.org/10.1107/S2053273316008378</a></p></body></html>"))
        self.aboutQtButton.setText(_translate("WAbout", "About Qt"))
        self.closeButton.setText(_translate("WAbout", "Close"))

from . import resources_rc

