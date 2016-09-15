from PyQt5.QtWidgets import QLineEdit, QWidget #type: ignore
from kryptal.gui import Application
from kryptal.gui.view.utils.PasswordsMatchPolicy import display


app = Application.get_instance_for_test()

class test_PasswordsMatchPolicy(object):
    def __init__(self) -> None:
        self.indicator = QWidget()
        self.password1Field = QLineEdit()
        self.password2Field = QLineEdit()

    def test_is_initially_not_shown_when_fields_equal(self) -> None:
        self.password1Field.setText("")
        self.password2Field.setText("")
        display(self.indicator).whenPasswordsDontMatch([self.password1Field, self.password2Field])
        assert not self.indicator.isVisible()

    def test_is_initially_shown_when_fields_not_equal(self) -> None:
        self.password1Field.setText("pw1")
        self.password2Field.setText("pw2")
        display(self.indicator).whenPasswordsDontMatch([self.password1Field, self.password2Field])
        assert self.indicator.isVisible()

    def test_changes_to_shown_when_fields_unequal_change1st(self) -> None:
        self.password1Field.setText("")
        self.password2Field.setText("")
        display(self.indicator).whenPasswordsDontMatch([self.password1Field, self.password2Field])
        assert not self.indicator.isVisible()
        self.password1Field.setText("different")
        assert self.indicator.isVisible()

    def test_changes_to_shown_when_fields_unequal_change2nd(self) -> None:
        self.password1Field.setText("")
        self.password2Field.setText("")
        display(self.indicator).whenPasswordsDontMatch([self.password1Field, self.password2Field])
        assert not self.indicator.isVisible()
        self.password2Field.setText("different")
        assert self.indicator.isVisible()

    def test_changes_to_not_shown_when_fields_equal_change1nd(self) -> None:
        self.password1Field.setText("pw1")
        self.password2Field.setText("pw2")
        display(self.indicator).whenPasswordsDontMatch([self.password1Field, self.password2Field])
        assert self.indicator.isVisible()
        self.password2Field.setText("pw1")
        assert not self.indicator.isVisible()

    def test_changes_to_not_shown_when_fields_equal_change2nd(self) -> None:
        self.password1Field.setText("pw1")
        self.password2Field.setText("pw2")
        display(self.indicator).whenPasswordsDontMatch([self.password1Field, self.password2Field])
        assert self.indicator.isVisible()
        self.password1Field.setText("pw2")
        assert not self.indicator.isVisible()


def test_zero_password_fields() -> None:
    indicator = QWidget()
    display(indicator).whenPasswordsDontMatch([])
    assert not indicator.isVisible()

def test_one_password_fields() -> None:
    indicator = QWidget()
    passwordField = QLineEdit()
    passwordField.setText("sometext")
    display(indicator).whenPasswordsDontMatch([passwordField])
    assert not indicator.isVisible()
