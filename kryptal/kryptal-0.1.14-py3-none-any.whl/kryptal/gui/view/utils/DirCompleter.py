from PyQt5.QtCore import QDir, QObject #type: ignore
from PyQt5.QtWidgets import QCompleter, QFileSystemModel #type: ignore


def get(parent: QObject) -> QCompleter:
    completer = QCompleter(parent)
    fsmodel = _fileSystemModel(parent=completer)
    completer.setModel(fsmodel)
    return completer

def _fileSystemModel(parent: QObject) -> QFileSystemModel:
    fsmodel = QFileSystemModel(parent)
    fsmodel.setReadOnly(True)
    fsmodel.setFilter(QDir.Dirs | QDir.AllDirs | QDir.Drives | QDir.NoDot | QDir.NoDotDot | QDir.Hidden)
    fsmodel.setRootPath('')
    return fsmodel
