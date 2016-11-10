# -*- coding: utf-8 -*-


from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_QSlidersWidget(object):
    def setupUi(self, QSlidersWidget):
        QSlidersWidget.setObjectName("QSlidersWidget")
        QSlidersWidget.resize(653, 388)
        self.gridLayout = QtWidgets.QGridLayout(QSlidersWidget)
        self.gridLayout.setObjectName("gridLayout")
        self.imageView = ImageView(QSlidersWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.imageView.sizePolicy().hasHeightForWidth())
        self.imageView.setSizePolicy(sizePolicy)
        self.imageView.setObjectName("imageView")
        self.gridLayout.addWidget(self.imageView, 1, 1, 1, 1)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.timeSlider = QtWidgets.QSlider(QSlidersWidget)
        self.timeSlider.setOrientation(QtCore.Qt.Vertical)
        self.timeSlider.setInvertedAppearance(True)
        self.timeSlider.setInvertedControls(False)
        self.timeSlider.setTickPosition(QtWidgets.QSlider.NoTicks)
        self.timeSlider.setObjectName("timeSlider")
        self.verticalLayout_2.addWidget(self.timeSlider)
        self.gridLayout.addLayout(self.verticalLayout_2, 1, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.twothSlider = QtWidgets.QSlider(QSlidersWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.twothSlider.sizePolicy().hasHeightForWidth())
        self.twothSlider.setSizePolicy(sizePolicy)
        self.twothSlider.setOrientation(QtCore.Qt.Horizontal)
        self.twothSlider.setObjectName("twothSlider")
        self.horizontalLayout.addWidget(self.twothSlider)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 1, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.timeEdit = QtWidgets.QLineEdit(QSlidersWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.timeEdit.sizePolicy().hasHeightForWidth())
        self.timeEdit.setSizePolicy(sizePolicy)
        self.timeEdit.setMaximumSize(QtCore.QSize(75, 75))
        self.timeEdit.setMaxLength(10)
        self.timeEdit.setObjectName("timeEdit")
        self.horizontalLayout_2.addWidget(self.timeEdit)
        self.twothEdit = QtWidgets.QLineEdit(QSlidersWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.twothEdit.sizePolicy().hasHeightForWidth())
        self.twothEdit.setSizePolicy(sizePolicy)
        self.twothEdit.setMaximumSize(QtCore.QSize(75, 75))
        self.twothEdit.setMaxLength(10)
        self.twothEdit.setObjectName("twothEdit")
        self.horizontalLayout_2.addWidget(self.twothEdit)
        self.gridLayout.addLayout(self.horizontalLayout_2, 0, 0, 1, 1)

        self.retranslateUi(QSlidersWidget)
        QtCore.QMetaObject.connectSlotsByName(QSlidersWidget)

    def retranslateUi(self, QSlidersWidget):
        _translate = QtCore.QCoreApplication.translate
        QSlidersWidget.setWindowTitle(_translate("QSlidersWidget", "Form"))

from medved.imageview import ImageView

