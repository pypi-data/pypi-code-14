from typing import List

from PyQt5.QtCore import QLine
from PyQt5.QtGui import QPalette
from PyQt5.QtWidgets import QCompleter, QWidget, QFileDialog #type: ignore
from PyQt5 import uic #type: ignore
import pkg_resources
from PyQt5.QtWidgets import QFrame
from PyQt5.QtWidgets import QLayout
from PyQt5.QtWidgets import QListWidget
from PyQt5.QtWidgets import QListWidgetItem
from PyQt5.QtWidgets import QScrollArea
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtWidgets import QSpacerItem
from PyQt5.QtWidgets import QVBoxLayout
from kryptal.gui.view.widgets.FileSystemListItem import FileSystemListItem
from kryptal.model.Filesystem import Filesystem
from kryptal.model.Filesystems import Filesystems


class FileSystemList(QScrollArea):
    def __init__(self, parent: QWidget = None) -> None:
        super(FileSystemList, self).__init__(parent)
        self.setBackgroundRole(QPalette.Base)
        self.setWidgetResizable(True)
        self.setWidget(QFrame())
        self._layout = QVBoxLayout(self.widget())

    def setModel(self, model: Filesystems) -> None:
        self._model = model
        self._model.addChangeHandler(self._update)
        self._update()

    def _update(self) -> None:
        self._clear()
        if self._model == None:
            return
        entries = [self._model.get(i) for i in range(0, self._model.count())]
        self._addListItemsFor(entries)

    def _clear(self) -> None:
        while self._layout.count() > 0:
            widgetToRemove = self._layout.takeAt(0)
            if widgetToRemove.widget() is not None:
                widgetToRemove.widget().deleteLater()

    def _addListItemsFor(self, entries: List[Filesystem]) -> None:
        widgets = [FileSystemListItem(fs) for fs in entries]
#        i = 0
        for widget in widgets:
#            if i%2 == 0:
#                widget.setBackgroundRole(QPalette.AlternateBase)
#            else:
#                widget.setBackgroundRole(QPalette.Base)
#            i = i+1
            self._layout.addWidget(widget)
            self._layout.addWidget(self._horizontalLine())
        #self._layout.setSpacing(0)
        self._layout.addStretch()

    def _horizontalLine(self) -> QFrame:
        frame = QFrame()
        frame.setFrameShape(QFrame.HLine)
        frame.setStyleSheet("color: lightgray;")
        return frame
