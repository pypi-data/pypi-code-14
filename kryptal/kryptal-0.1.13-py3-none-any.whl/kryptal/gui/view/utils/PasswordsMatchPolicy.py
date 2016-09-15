from typing import List

from PyQt5.QtCore import QObject #type: ignore
from PyQt5.QtWidgets import QLineEdit, QWidget #type: ignore

""" Use this class to automatically show/hide an indicator widget when two password QLineEdit have different contents.
Usage Example:

display(myIndicatorWidget).whenPasswordsDontMatch([passwordField1, passwordField2])
"""
class display(QObject):
    def __init__(self, indicator: QWidget) -> None:
        # Use indicator as parent object, so we don't get deleted
        # (i.e. users of this class don't have to store a reference)
        super(QObject, self).__init__(indicator)
        self._indicator = indicator
        self._passwordFields = [] # type: List[QLineEdit]

    def whenPasswordsDontMatch(self, passwordFields: List[QLineEdit]) -> None:
        for passwordField in passwordFields:
            self._passwordFields.append(passwordField)
            passwordField.textChanged.connect(self._onPasswordFieldChanged)
        self._onPasswordFieldChanged()

    def _onPasswordFieldChanged(self) -> None:
        self._indicator.setVisible(not self._passwordsMatch())

    def _passwordsMatch(self) -> bool:
        passwords = [field.text() for field in self._passwordFields]
        return len(set(passwords)) <= 1
