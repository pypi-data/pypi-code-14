#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
from PyQt5 import QtCore, QtGui, QtWidgets
from pyqtgraph import dockarea
from .ui.ui_wmedeval import Ui_MEDeval
from .ui.ui_wabout import Ui_WAbout
from .plotwidget import PlotWidget
from .wsliders import WSliders


FOURIER_COMPONENTS = 'Real', 'Imaginary', 'Amplitude', 'Phase',


class WAbout(QtWidgets.QDialog, Ui_WAbout):
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent=parent)
        self._parent = parent
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon(':/medved'))
        # noinspection PyCallByClass,PyTypeChecker
        QtCore.QTimer.singleShot(0.1, lambda: self.resize(0, 0))

    @QtCore.pyqtSlot()
    def on_closeButton_clicked(self):
        self.close()

    @QtCore.pyqtSlot()
    def on_aboutQtButton_clicked(self):
        # noinspection PyCallByClass,PyTypeChecker,PyArgumentList
        QtWidgets.QMessageBox.aboutQt(self)


class QWMEDeval(QtWidgets.QMainWindow, Ui_MEDeval):
    closeEventSignal = QtCore.pyqtSignal()
    chosenDirSignal = QtCore.pyqtSignal(str)
    cancelLoadSignal = QtCore.pyqtSignal()
    updateFourierPlot = QtCore.pyqtSignal()
    updateDataPlot = QtCore.pyqtSignal()

    def __init__(self, settings, parent):
        super().__init__()
        self.controller = parent
        self.settings = settings
        self.setupUi()
        self.connectSignals()

    # noinspection PyUnresolvedReferences
    def connectSignals(self):
        self.dataSliders.timeSlider.valueChanged.connect(self.showCurrentDataTreeItem)
        self.fourierSliders.timeSlider.valueChanged.connect(self.showCurrentFourierTreeItem)

    def setupUi(self, *args, **kwargs):
        Ui_MEDeval.setupUi(self, self)
        self.setDataDocks()
        self.setFourierDocks()
        self.setCentralWidget(self.tabWidget)
        self.toolBar.addSeparator()
        self.wlEdit = QtWidgets.QLineEdit()
        self.wlEdit.setValidator(QtGui.QDoubleValidator())
        self.wlEdit.setMaximumWidth(200)
        self.toolBar.insertWidget(self.actionD, self.wlEdit)
        self.wabout = WAbout(self)

    def setDataDocks(self):
        self.dataDock = dockarea.DockArea()
        plotDock = dockarea.Dock('1D data view')
        self.dataPlot = PlotWidget(plotDock)
        plotDock.addWidget(self.dataPlot)
        slidersDock = dockarea.Dock('2D data view')
        self.dataSliders = WSliders(self.dataPlot, self)
        slidersDock.addWidget(self.dataSliders)
        dataTreeDock = dockarea.Dock('Data tree view')
        self.dataTree.setHeaderLabel('Patterns')
        dataTreeDock.addWidget(self.dataTree)
        self.dataDock.addDock(dataTreeDock)
        self.dataDock.addDock(slidersDock, 'right', dataTreeDock)
        self.dataDock.addDock(plotDock, 'bottom', slidersDock)
        self.tabWidget.addTab(self.dataDock, 'Data')

    def setFourierDocks(self):
        self.fourierDock = dockarea.DockArea()
        plotDock = dockarea.Dock('1D Fourier view')
        self.fourierPlot = PlotWidget(plotDock)
        plotDock.addWidget(self.fourierPlot)
        slidersDock = dockarea.Dock('2D Fourier view')
        self.fourierSliders = WSliders(self.fourierPlot, self)
        slidersDock.addWidget(self.fourierSliders)
        fourierTreeDock = dockarea.Dock('Fourier tree view')
        self.fourierTree.setHeaderLabel('Patterns')
        fourierTreeDock.addWidget(self.fourierTree)
        self.fourierDock.addDock(fourierTreeDock)
        self.fourierDock.addDock(slidersDock, 'right', fourierTreeDock)
        self.fourierDock.addDock(plotDock, 'bottom', slidersDock)
        self.tabWidget.addTab(self.fourierDock, 'Fourier')

    def saveSettings(self):
        s = self.settings
        s.setValue('WMedved/Geometry', self.saveGeometry())
        s.setValue('WMedved/State', self.saveState())
        s.setValue('WMedved/lastdir', self.lastdir)
        s.setValue('WMedved/dataDockState', json.dumps(self.dataDock.saveState()))
        s.setValue('WMedved/fourierDockState', json.dumps(self.fourierDock.saveState()))

    def loadSettings(self):
        s = self.settings
        self.restoreGeometry(s.value('WMedved/Geometry', QtCore.QByteArray()))
        self.restoreState(s.value('WMedved/State', QtCore.QByteArray()))
        self.lastdir = s.value('WMedved/lastdir', '')
        dockState = s.value('WMedved/dataDockState', None)
        if dockState:
            self.dataDock.restoreState(json.loads(dockState))
        dockState = s.value('WMedved/fourierDockState', None)
        if dockState:
            self.fourierDock.restoreState(json.loads(dockState))
        # noinspection PyCallByClass,PyTypeChecker
        QtCore.QTimer.singleShot(50, lambda: self.tabWidget.setCurrentIndex(1))
        # noinspection PyCallByClass,PyTypeChecker
        QtCore.QTimer.singleShot(100, lambda: self.tabWidget.setCurrentIndex(0))

    def closeEvent(self, event):
        self.closeEventSignal.emit()
        QtWidgets.QMainWindow.closeEvent(self, event)

    def finishedLoad(self, t, ft, d, fd, dire, files):
        self.dataSliders.twothSlider.setMaximum(d)
        self.dataSliders.timeSlider.setMaximum(t)
        self.fourierSliders.twothSlider.setMaximum(fd)
        self.fourierSliders.timeSlider.setMaximum(ft)
        self.dataTree.takeTopLevelItem(0)
        mainItem = QtWidgets.QTreeWidgetItem(self.dataTree)
        self.dataTree.addTopLevelItem(mainItem)
        mainItem.setText(0, dire)
        self.items = []
        for f in files:
            item = QtWidgets.QTreeWidgetItem(mainItem)
            item.setText(0, f)
            self.items.append(item)
        for _ in FOURIER_COMPONENTS:
            self.fourierTree.takeTopLevelItem(0)
        self.fitems = {}
        for name in FOURIER_COMPONENTS:
            mainItem = QtWidgets.QTreeWidgetItem(self.fourierTree)
            mainItem.setText(0, name)
            self.fitems[name] = []
            for i in range(ft + 1):
                item = QtWidgets.QTreeWidgetItem(mainItem)
                item.setText(0, 'Harmonic {:d}'.format(i))
                self.fitems[name].append(item)
            self.fourierTree.addTopLevelItem(mainItem)

    @QtCore.pyqtSlot()
    def on_actionOpenDir_triggered(self):
        # noinspection PyCallByClass,PyTypeChecker,PyArgumentList
        dire = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select directory', directory=self.lastdir)
        if dire:
            self.lastdir = dire
            self.chosenDirSignal.emit(dire)

    def showCurrentDataTreeItem(self, value):
        self.dataTree.setCurrentItem(self.items[value])

    def showCurrentFourierTreeItem(self, value):
        for component in FOURIER_COMPONENTS:
            if self.__dict__['action{}'.format(component)].isChecked():
                self.fourierTree.setCurrentItem(self.fitems[component][value])

    @QtCore.pyqtSlot(QtWidgets.QTreeWidgetItem, int)
    def on_dataTree_itemClicked(self, item):
        # noinspection PyUnresolvedReferences
        self.dataSliders.timeSlider.valueChanged.emit(self.items.index(item))

    @QtCore.pyqtSlot(QtWidgets.QTreeWidgetItem, int)
    def on_fourierTree_itemClicked(self, item):
        text = item.text(0)
        if text not in FOURIER_COMPONENTS:
            text = item.parent().text(0)
            # noinspection PyUnresolvedReferences
            self.fourierSliders.timeSlider.valueChanged.emit(self.fitems[text].index(item))
        self.uncheckAllYActionsBut(self.__dict__['action{}'.format(text)])

    def on_actionReal_triggered(self):
        self.uncheckAllYActionsBut(self.actionReal)

    def on_actionImaginary_triggered(self):
        self.uncheckAllYActionsBut(self.actionImaginary)

    def on_actionPhase_triggered(self):
        self.uncheckAllYActionsBut(self.actionPhase)

    def on_actionAmplitude_triggered(self):
        self.uncheckAllYActionsBut(self.actionAmplitude)

    def on_action2Theta_triggered(self):
        self.uncheckAllXActionsBut(self.action2Theta)

    def on_actionD_triggered(self):
        self.uncheckAllXActionsBut(self.actionD)

    def on_actionD2_triggered(self):
        self.uncheckAllXActionsBut(self.actionD2)

    def on_actionAbout_triggered(self):
        self.wabout.show()

    def uncheckAllYActionsBut(self, action):
        actions = self.actionReal, self.actionPhase, self.actionAmplitude, self.actionImaginary
        self.uncheckAllActionsBut(action, actions)

    def uncheckAllXActionsBut(self, action):
        actions = self.action2Theta, self.actionD, self.actionD2
        self.uncheckAllActionsBut(action, actions)

    def uncheckAllActionsBut(self, action, actions):
        for act in actions:
            if action != act:
                act.setChecked(False)
        action.setChecked(True)
        self.updateFourierPlot.emit()
        self.updateDataPlot.emit()

    def showModelError(self, msg):
        # noinspection PyArgumentList,PyCallByClass,PyTypeChecker
        QtWidgets.QMessageBox.critical(self, 'Error', msg)
