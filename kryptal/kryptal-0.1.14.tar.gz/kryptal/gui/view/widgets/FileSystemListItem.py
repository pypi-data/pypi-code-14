from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget #type: ignore
from PyQt5 import uic #type: ignore
import pkg_resources
from kryptal.gui.view.icons import Icons
from kryptal.model.Filesystem import Filesystem


class FileSystemListItem(QWidget):
    def __init__(self, filesystem: Filesystem) -> None:
        super(FileSystemListItem, self).__init__()

        uipath = pkg_resources.resource_filename(__name__, "filesystemlistitem.ui")
        uic.loadUi(uipath, self)
        self.nameLabel.setText(filesystem.name)
        self.fstypeLabel.setText(filesystem.fstype)
        self.plaintextDirLabel.setDirectory(filesystem.plaintextDirectory)
        self.ciphertextDirLabel.setText(filesystem.ciphertextDirectory)

        self.detailsButton.setIcon(QIcon(Icons.get_path("gear.svg")))
        self.detailsButton.clicked.connect(self._onDetailsButtonClick)
        self.detailsFrame.setVisible(False)

    def _onDetailsButtonClick(self) -> None:
        self.detailsFrame.setVisible(self.detailsButton.isChecked())
