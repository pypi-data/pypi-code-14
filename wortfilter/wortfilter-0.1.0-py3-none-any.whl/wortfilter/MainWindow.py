import pkg_resources
from PyQt5 import uic #type: ignore
from PyQt5.Qt import QStyle #type: ignore
from PyQt5.QtWidgets import QMainWindow, QWidget, QFileDialog, QMessageBox #type: ignore
from wortfilter import NormalizingFilter


class MainWindow(QMainWindow):
    def __init__(self, parent: QWidget = None) -> None:
        super(MainWindow, self).__init__(parent)

        uipath = pkg_resources.resource_filename(__name__, "ui/MainWindow.ui")
        uic.loadUi(uipath, self)

        self.addWordsButton.clicked.connect(self.onAddWordsButtonClick)
        self.saveWordsButton.clicked.connect(self.onSaveWordsButtonClick)
        self.allowedLettersEdit.textChanged.connect(self.onInputChanged)
        self.wordListEdit.textChanged.connect(self.onInputChanged)

    def onAddWordsButtonClick(self) -> None:
        (filename, filter) = QFileDialog.getOpenFileName(self, "Wörter hinzufügen")
        with open(filename, 'r') as file:
            content = file.read()
        oldWordList = self.wordListEdit.toPlainText()
        newWordList = oldWordList + "\n" + content
        newWordList = self._maybeNormalize(newWordList)
        self.wordListEdit.document().setPlainText(newWordList)

    def _maybeNormalize(self, wordList: str) -> str:
        normalized = "\n".join(NormalizingFilter.normalizeWordList(wordList))
        if normalized == wordList:
            return wordList

        removeDuplicates = QMessageBox.Yes == QMessageBox.question(self, "Wortliste speichern", "Sollen doppelte Wörter in der Datei gelöscht werden?")
        if removeDuplicates:
            wordList = "\n".join(NormalizingFilter.normalizeWordList(wordList))
        return wordList

    def onSaveWordsButtonClick(self) -> None:
        (filename, filter) = QFileDialog.getSaveFileName(self, "Wortliste speichern")
        if filename!= "":
            self._storeWordList(filename)

    def _storeWordList(self, filename: str) -> None:
        wordList = self.wordListEdit.toPlainText()
        with open(filename, 'w') as file:
            file.write(wordList)

    def onInputChanged(self) -> None:
        allowedLetters = self.allowedLettersEdit.text()
        wordList = self.wordListEdit.toPlainText()
        filteredWords = NormalizingFilter.filter(wordList, allowedLetters)
        self.filteredWordsEdit.document().setPlainText(filteredWords)
