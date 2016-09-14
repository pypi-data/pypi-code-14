import os
from PyQt5.QtWidgets import QMessageBox, QWidget #type: ignore


class CreateDirectoryYesNoController(object):
    def __init__(self, parent: QWidget = None) -> None:
        self._parent = parent

    def askYesNoAndCreateDir(self, name: str, path: str) -> bool:
        if self._askYesNo("Create %s?" % name, "The %s doesn't exist. Do you want to create it?" % name):
            return self._createDirectory(name, path)
        return False

    def _createDirectory(self, name: str, path: str) -> bool:
        try:
            os.makedirs(path)
            return True
        except PermissionError:
            QMessageBox.warning(self._parent, "Error creating %s" % name,
                                "Couldn't create %s because of missing permissions." % name)
            return False
        except:
            QMessageBox.warning(self._parent, "Error creating %s" % name, "Couldn't create %s." % name)
            return False

    def _askYesNo(self, title: str, question: str) -> bool:
        return QMessageBox.Yes == QMessageBox.question(self._parent, title, question, QMessageBox.Yes | QMessageBox.No,
                                                       QMessageBox.Yes)
