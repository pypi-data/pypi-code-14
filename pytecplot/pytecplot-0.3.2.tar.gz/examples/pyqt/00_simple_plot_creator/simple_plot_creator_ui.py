# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'simple_plot_creator.ui'
#
# Created: Fri Mar 18 15:32:50 2016
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(702, 719)
        self.imageLabel = QtGui.QLabel(Form)
        self.imageLabel.setGeometry(QtCore.QRect(72, 200, 551, 411))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.imageLabel.sizePolicy().hasHeightForWidth())
        self.imageLabel.setSizePolicy(sizePolicy)
        self.imageLabel.setText(_fromUtf8(""))
        self.imageLabel.setObjectName(_fromUtf8("imageLabel"))
        self.widget = QtGui.QWidget(Form)
        self.widget.setGeometry(QtCore.QRect(22, 30, 631, 87))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.horizontalLayout_4 = QtGui.QHBoxLayout(self.widget)
        self.horizontalLayout_4.setMargin(0)
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.rectangularZonePushButton = QtGui.QPushButton(self.widget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.rectangularZonePushButton.sizePolicy().hasHeightForWidth())
        self.rectangularZonePushButton.setSizePolicy(sizePolicy)
        self.rectangularZonePushButton.setObjectName(_fromUtf8("rectangularZonePushButton"))
        self.verticalLayout_2.addWidget(self.rectangularZonePushButton)
        self.cylindricalZonePushButton = QtGui.QPushButton(self.widget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cylindricalZonePushButton.sizePolicy().hasHeightForWidth())
        self.cylindricalZonePushButton.setSizePolicy(sizePolicy)
        self.cylindricalZonePushButton.setObjectName(_fromUtf8("cylindricalZonePushButton"))
        self.verticalLayout_2.addWidget(self.cylindricalZonePushButton)
        self.sphericalZonePushButton = QtGui.QPushButton(self.widget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sphericalZonePushButton.sizePolicy().hasHeightForWidth())
        self.sphericalZonePushButton.setSizePolicy(sizePolicy)
        self.sphericalZonePushButton.setObjectName(_fromUtf8("sphericalZonePushButton"))
        self.verticalLayout_2.addWidget(self.sphericalZonePushButton)
        self.horizontalLayout_4.addLayout(self.verticalLayout_2)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(self.widget)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.iDimSlider = QtGui.QSlider(self.widget)
        self.iDimSlider.setOrientation(QtCore.Qt.Horizontal)
        self.iDimSlider.setObjectName(_fromUtf8("iDimSlider"))
        self.horizontalLayout.addWidget(self.iDimSlider)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label_2 = QtGui.QLabel(self.widget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_2.addWidget(self.label_2)
        self.jDimSlider = QtGui.QSlider(self.widget)
        self.jDimSlider.setOrientation(QtCore.Qt.Horizontal)
        self.jDimSlider.setObjectName(_fromUtf8("jDimSlider"))
        self.horizontalLayout_2.addWidget(self.jDimSlider)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.kDimLabel = QtGui.QLabel(self.widget)
        self.kDimLabel.setObjectName(_fromUtf8("kDimLabel"))
        self.horizontalLayout_3.addWidget(self.kDimLabel)
        self.kDimSlider = QtGui.QSlider(self.widget)
        self.kDimSlider.setOrientation(QtCore.Qt.Horizontal)
        self.kDimSlider.setObjectName(_fromUtf8("kDimSlider"))
        self.horizontalLayout_3.addWidget(self.kDimSlider)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4.addLayout(self.verticalLayout)
        self.horizontalLayout_4.setStretch(0, 1)
        self.horizontalLayout_4.setStretch(1, 1)
        self.horizontalLayout_4.setStretch(2, 5)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.rectangularZonePushButton.setText(_translate("Form", "Rectangular Zone", None))
        self.cylindricalZonePushButton.setText(_translate("Form", "Cylindrical Zone", None))
        self.sphericalZonePushButton.setText(_translate("Form", "Spherical Zone", None))
        self.label.setText(_translate("Form", "I Dim:", None))
        self.label_2.setText(_translate("Form", "J Dim:", None))
        self.kDimLabel.setText(_translate("Form", "K Dim:", None))

