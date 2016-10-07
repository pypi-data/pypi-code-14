from builtins import super

from PyQt4 import QtCore, QtGui
from tempfile import NamedTemporaryFile

import tecplot as tp
import simple_plot_creator_ui

class ExampleApp(QtGui.QWidget, simple_plot_creator_ui.Ui_Form):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.createFunction = None
        self.uiInitialized = False   # Disable UI callbacks while programmatically setting up controls
        self.setupUi(self)           # execute ui file layout

        self.idim = 10
        self.jdim = 10
        self.kdim = 10
        self.setupLocalUi()          # local customizations
        self.uiInitialized = True

    def setupLocalUi(self):
        self.rectangularZonePushButton.clicked.connect(self.createRectangularZone)
        self.sphericalZonePushButton.clicked.connect(self.createSphericalZone)
        self.cylindricalZonePushButton.clicked.connect(self.createCylindricalZone)
        self.iDimSlider.setMinimum(3)
        self.iDimSlider.setMaximum(150)
        self.iDimSlider.setTracking(False)
        self.iDimSlider.valueChanged.connect(self.iDimChanged)
        self.iDimSlider.setValue(self.idim)
        self.jDimSlider.setMinimum(3)
        self.jDimSlider.setMaximum(150)
        self.jDimSlider.setTracking(False)
        self.jDimSlider.valueChanged.connect(self.jDimChanged)
        self.jDimSlider.setValue(self.jdim)
        self.kDimSlider.setMinimum(3)
        self.kDimSlider.setMaximum(150)
        self.kDimSlider.setTracking(False)
        self.kDimSlider.valueChanged.connect(self.kDimChanged)
        self.kDimSlider.setValue(self.kdim)

        self.imageLabel.setBackgroundRole(QtGui.QPalette.Base)

    def showResult(self):
        with NamedTemporaryFile(suffix='.png') as ftmp:
            tp.export_image(ftmp.name)
            image = QtGui.QImage(ftmp.name)
            self.imageLabel.setPixmap(QtGui.QPixmap.fromImage(image))
        self.scaleFactor = 1.0
        self.imageLabel.adjustSize()

    def setStyleAndDisplay(self):
        tp.macro.execute_command("$!FIELDMAP [1]  SURFACES{SURFACESTOPLOT = BOUNDARYFACES}")
        tp.macro.execute_command("$!FIELDLAYERS SHOWMESH = YES")
        self.showResult()

    def createRectangularZone(self):
        tp.new_layout()
        tp.macro.execute_command("$!CreateRectangularZone IMax  = %d JMax  = %d KMax  = %d " % ( self.idim, self.jdim, self.kdim))
        self.setStyleAndDisplay()
        self.createFunction = self.createRectangularZone
        self.kDimSlider.setEnabled(True)
        self.kDimLabel.setEnabled(True)

    def createSphericalZone(self):
        tp.new_layout()
        tp.macro.execute_command("$!CreateSphericalZone IMax  = %d JMax  = %d " % ( self.idim, self.jdim))
        self.setStyleAndDisplay()
        self.createFunction = self.createSphericalZone
        self.kDimSlider.setEnabled(False)
        self.kDimLabel.setEnabled(False)

    def createCylindricalZone(self):
        tp.new_layout()
        tp.macro.execute_command("$!CreateCircularZone IMax  = %d JMax  = %d KMax  = %d " % ( self.idim, self.jdim, self.kdim))
        self.setStyleAndDisplay()
        self.createFunction = self.createCylindricalZone
        self.kDimSlider.setEnabled(True)
        self.kDimLabel.setEnabled(True)

    def iDimChanged(self):
        if self.uiInitialized and self.createFunction != None:
            dim = self.iDimSlider.value()
            self.idim = dim
            self.createFunction()

    def jDimChanged(self):
        if self.uiInitialized and self.createFunction != None:
            dim = self.jDimSlider.value()
            self.jdim = dim
            self.createFunction()

    def kDimChanged(self):
        if self.uiInitialized and self.createFunction != None:
            dim = self.kDimSlider.value()
            self.kdim = dim
            self.createFunction()

if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    myWidget = ExampleApp()
    myWidget.show()
    ret = app.exec_()
    tp.session.stop()
    sys.exit(ret)
