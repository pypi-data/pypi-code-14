#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from PyQt5 import QtCore, QtGui, QtWidgets
from cryio import cbfimage
from .ui.ui_wheader import Ui_WHeader


class WHeader(QtWidgets.QDialog, Ui_WHeader):
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self._parent = parent
        self.setupUi(self)
        self.valuesList.addItems(sorted(list(cbfimage.CbfImage.ALL_KEYWORDS.keys()) + ['!File name', 'Date', 'Time']))
        self.loadSettings()
        self.stopButton.setVisible(False)
        self.stopped = True
        self.createContextMenu()
        self.resultTable.keyPressEvent = self.resultTableKeyPressEvent
        self.resultTable.contextMenuEvent = self.resultTableContextMenuEvent

    def createContextMenu(self):
        copyMenuAction = QtWidgets.QAction('&Copy', self.resultTable)
        copyMenuAction.setShortcut(QtGui.QKeySequence.Copy)
        # noinspection PyUnresolvedReferences
        copyMenuAction.triggered.connect(self.copyToClipboard)
        saveTextAction = QtWidgets.QAction('&Save as text', self.resultTable)
        saveTextAction.setShortcut(QtGui.QKeySequence.Save)
        # noinspection PyUnresolvedReferences
        saveTextAction.triggered.connect(self.on_saveButton_clicked)
        self.contextMenu = QtWidgets.QMenu()
        self.contextMenu.addAction(copyMenuAction)
        self.contextMenu.addAction(saveTextAction)

    def resultTableContextMenuEvent(self, event):
        self.contextMenu.exec_(event.globalPos())

    @QtCore.pyqtSlot()
    def copyToClipboard(self):
        selectedItems = self.resultTable.selectedItems()
        toClipboard = u''
        for i in range(self.resultTable.rowCount()):
            setNewLine = u''
            for j in range(self.resultTable.columnCount()):
                item = self.resultTable.item(i, j)
                if selectedItems:
                    if item in selectedItems:
                        toClipboard += item.text() + u'\t'
                        setNewLine = '\n'
                elif item:
                    toClipboard += item.text() + u'\t'
                    setNewLine = '\n'
            toClipboard += setNewLine
        # noinspection PyArgumentList
        QtWidgets.QApplication.clipboard().setText(toClipboard)

    def resultTableKeyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_C and event.modifiers() == QtCore.Qt.ControlModifier:
            self.copyToClipboard()

    def closeEvent(self, event):
        self.saveSettings()
        self.hide()

    def checkedHeaderValues(self):
        checked = []
        for i in range(self.valuesList.count()):
            item = self.valuesList.item(i)
            if item.checkState():
                checked.append(item.text())
        return checked

    def saveSettings(self):
        settings = QtCore.QSettings()
        settings.setValue('WHeader/Geometry', self.saveGeometry())
        settings.setValue('WHeader/checked', self.checkedHeaderValues())
        settings.setValue('WHeader/lastFolder', self.lastFolder)

    def loadSettings(self):
        settings = QtCore.QSettings()
        self.restoreGeometry(settings.value('WHeader/Geometry', QtCore.QByteArray()))
        self.lastFolder = settings.value('WHeader/lastFolder', u'')
        self.folderLineEdit.setText(self.lastFolder)
        checked = settings.value('WHeader/checked') or []
        for i in range(self.valuesList.count()):
            item = self.valuesList.item(i)
            item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
            item.setCheckState(QtCore.Qt.Checked if item.text() in checked else QtCore.Qt.Unchecked)
        self.on_valuesList_itemClicked()

    #noinspection PyUnusedLocal
    def on_valuesList_itemClicked(self, item=None):
        self.resultTable.clear()
        self.resultTable.setRowCount(0)
        checked = self.checkedHeaderValues()
        self.resultTable.setColumnCount(len(checked))
        self.resultTable.setHorizontalHeaderLabels(checked)

    @QtCore.pyqtSlot()
    def on_stopButton_clicked(self):
        self.stopped = True

    @QtCore.pyqtSlot()
    def on_runButton_clicked(self):
        self.stopped = False
        self.runButton.setVisible(False)
        self.stopButton.setVisible(True)
        self.walkThroughFolder()
        self.stopped = True
        self.runButton.setVisible(True)
        self.stopButton.setVisible(False)

    @QtCore.pyqtSlot()
    def on_saveButton_clicked(self):
        # noinspection PyCallByClass,PyTypeChecker
        datName = QtWidgets.QFileDialog.getSaveFileName(self, 'Save file as a text', self.lastFolder)
        if not datName:
            return
        res = u'%s\n' % u' '.join(self.checkedHeaderValues())
        for i in range(self.resultTable.rowCount()):
            for j in range(self.resultTable.columnCount()):
                res += u'%s ' % self.resultTable.item(i, j).text()
            res += '\n'
        open(datName, 'w').write(res)

    def walkThroughFolder(self):
        self.on_valuesList_itemClicked()
        folder = self.folderLineEdit.text()
        checked = self.checkedHeaderValues()
        if not folder or not checked or not os.path.exists(folder):
            return
        files = sorted([f for f in os.listdir(folder) if f.endswith('.cbf')])
        self.resultTable.setRowCount(len(files))
        for i, cbf in enumerate(files):
            # noinspection PyArgumentList
            QtCore.QCoreApplication.processEvents()
            if self.stopped:
                return

            hdr = cbfimage.CbfHeader(os.path.join(folder, cbf))
            for j, key in enumerate(checked):
                try:
                    value = hdr[key]
                except KeyError:
                    continue
                item = QtWidgets.QTableWidgetItem(str(value))
                self.resultTable.setItem(i, j, item)
            self.runProgressBar.setValue(100 * (i + 1) / len(files))

    @QtCore.pyqtSlot()
    def on_folderButton_clicked(self):
        # noinspection PyCallByClass,PyTypeChecker
        folder = QtWidgets.QFileDialog.getExistingDirectory(self, 'Choose folder with cbf files', self.lastFolder)
        if folder:
            self.folderLineEdit.setText(folder)
            self.lastFolder = folder

    @QtCore.pyqtSlot()
    def on_copyButton_clicked(self):
        self.resultTable.selectAll()
        self.copyToClipboard()
