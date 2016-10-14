import pkg_resources
from PyQt5 import uic #type: ignore
from PyQt5.Qt import QStyle #type: ignore
from PyQt5.QtCore import Qt #type: ignore
from PyQt5.QtGui import QCursor #type: ignore
from PyQt5.QtWidgets import QMainWindow, QWidget, QFileDialog, QMessageBox #type: ignore
from wortfilter import NormalizingFilter


class MainWindow(QMainWindow):
    def __init__(self, parent: QWidget = None) -> None:
        super(MainWindow, self).__init__(parent)

        uipath = pkg_resources.resource_filename(__name__, "ui/MainWindow.ui")
        uic.loadUi(uipath, self)

        self.addWordsButton.clicked.connect(self.onAddWordsButtonClick)
        self.saveWordsButton.clicked.connect(self.onSaveWordsButtonClick)
        self.filterButton.clicked.connect(self.onFilterButtonClick)

    def onAddWordsButtonClick(self) -> None:
        (filename, filter) = QFileDialog.getOpenFileName(self, "Wörter hinzufügen")
        if filename != "":
            self.setCursor(QCursor(Qt.WaitCursor))
            content = self._loadFromFile(filename)
            oldWordList = self.wordListEdit.toPlainText()
            newWordList = oldWordList + "\n" + content
            newWordList = self._maybeNormalize(newWordList)
            self.wordListEdit.document().setPlainText(newWordList)
            self.unsetCursor()

    def _loadFromFile(self, filename: str) -> str:
        try:
            with open(filename, 'r') as file:
                return file.read()
        except:
            with open(filename, 'r', encoding = 'ISO-8859-1') as file:
                return file.read()

    def _maybeNormalize(self, wordList: str) -> str:
        normalized = "\n".join(NormalizingFilter.normalizeWordList(wordList))
        if normalized == wordList:
            return wordList

        removeDuplicates = QMessageBox.Yes == QMessageBox.question(self, "Wortliste speichern", "Sollen doppelte Wörter in der Datei gelöscht werden?")
        if removeDuplicates:
            wordList = normalized
        return wordList

    def onSaveWordsButtonClick(self) -> None:
        (filename, filter) = QFileDialog.getSaveFileName(self, "Wortliste speichern")
        if filename!= "":
            self._storeWordList(filename)

    def _storeWordList(self, filename: str) -> None:
        wordList = self.wordListEdit.toPlainText()
        with open(filename, 'w') as file:
            file.write(wordList)

    def onFilterButtonClick(self) -> None:
        self.setCursor(QCursor(Qt.WaitCursor))
        allowedLetters = self.allowedLettersEdit.text()
        wordList = self.wordListEdit.toPlainText()
        filteredWords = NormalizingFilter.filter(wordList, allowedLetters)
        self.filteredWordsEdit.document().setPlainText(filteredWords)
        self.unsetCursor()
