import pkg_resources
from PyQt5 import uic #type: ignore
from PyQt5.Qt import QStyle #type: ignore
from PyQt5.QtWidgets import QMainWindow, QWidget #type: ignore


class MainWindow(QMainWindow):
    def __init__(self, parent: QWidget = None) -> None:
        super(MainWindow, self).__init__(parent)

        uipath = pkg_resources.resource_filename(__name__, "ui/MainWindow.ui")
        uic.loadUi(uipath, self)
