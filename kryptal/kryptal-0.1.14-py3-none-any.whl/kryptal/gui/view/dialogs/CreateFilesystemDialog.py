from typing import List, Callable

import pkg_resources
from PyQt5 import uic #type: ignore
from PyQt5.QtWidgets import QDialog, QWidget #type: ignore
from kryptal.gui.view.utils.PasswordsMatchPolicy import display


class CreateFilesystemDialog(QDialog):
    def __init__(self, parent: QWidget = None) -> None:
        super(CreateFilesystemDialog, self).__init__(parent)

        uipath = pkg_resources.resource_filename(__name__, "createfilesystemdialog.ui")
        uic.loadUi(uipath, self)

        display(self.passwordsMatchIndicator).whenPasswordsDontMatch([
            self.password1Edit, self.password2Edit
        ])
        self._acceptHandler = lambda **args: True

        # Setting tab order in QtDesigner doesn't work for nested widgets, do it manually.
        # See also: http://stackoverflow.com/questions/18641879/how-can-i-set-qt-tab-order-for-a-form-with-a-composite-widget
        #           https://bugreports.qt.io/browse/QTBUG-10907
        self._setTabOrder([
            self.nameLabel,
            self.ciphertextDirSelector.directoryEdit,
            self.ciphertextDirSelector.browseButton,
            self.plaintextDirSelector.directoryEdit,
            self.plaintextDirSelector.browseButton,
            self.password1Edit,
            self.password2Edit,
            self.dialogButtons
        ])

    def _setTabOrder(self, order: List[QWidget]) -> None:
        for i in range(1, len(order)):
            self.setTabOrder(order[i-1], order[i])

    def setAcceptHandler(self, acceptHandler: Callable[..., bool]) -> None:
        self._acceptHandler = acceptHandler

    def clearPasswordFields(self) -> None:
        self.password1Edit.setText("")
        self.password2Edit.setText("")
        self.password1Edit.setFocus()

    def accept(self) -> None:
        if self._acceptHandler(
            name=self.nameEdit.text(),
            ciphertextDir=self.ciphertextDirSelector.directory(),
            plaintextDir=self.plaintextDirSelector.directory(),
            password1=self.password1Edit.text(),
            password2=self.password2Edit.text()
        ):
            super(CreateFilesystemDialog, self).accept()
