from unittest.mock import MagicMock #type: ignore
from PyQt5.QtCore import Qt #type: ignore
from PyQt5.QtTest import QTest #type: ignore
from PyQt5.QtWidgets import QDialogButtonBox #type: ignore
from kryptal.gui import Application
from kryptal.gui.view.dialogs.CreateFilesystemDialog import CreateFilesystemDialog
from nose.tools import assert_equals

app = Application.get_instance_for_test()

def test_init_without_error() -> None:
    CreateFilesystemDialog()

def test_passwords_match_indicator() -> None:
    dlg = CreateFilesystemDialog()
    dlg.show() # Dialog has to be visible, otherwise isVisible() of passwordsMatchIndicator will always be false.
    assert not dlg.passwordsMatchIndicator.isVisible()
    dlg.password1Edit.setText("pw1")
    assert dlg.passwordsMatchIndicator.isVisible()
    dlg.password2Edit.setText("pw2")
    assert dlg.passwordsMatchIndicator.isVisible()
    dlg.password1Edit.setText("pw2")
    assert not dlg.passwordsMatchIndicator.isVisible()
    dlg.password2Edit.setText("pw1")
    assert dlg.passwordsMatchIndicator.isVisible()
    dlg.password1Edit.setText("pw2")
    assert dlg.passwordsMatchIndicator.isVisible()
    dlg.password1Edit.setText("pw1")
    assert not dlg.passwordsMatchIndicator.isVisible()

def test_clear_password_fields() -> None:
    dlg = CreateFilesystemDialog()
    dlg.password1Edit.setText("pw1")
    dlg.password2Edit.setText("pw2")
    dlg.clearPasswordFields()
    assert_equals("", dlg.password1Edit.text())
    assert_equals("", dlg.password2Edit.text())

def test_default_acceptor_just_accepts() -> None:
    dlg = CreateFilesystemDialog()
    dlg.show()
    QTest.keyClick(dlg, Qt.Key_Enter)
    assert not dlg.isVisible()

class test_WithCustomAcceptHandler(object):
    def __init__(self) -> None:
        self.acceptHandlerMock = MagicMock()
        self.acceptHandlerMock.return_value = True
        self.dlg = CreateFilesystemDialog()
        self.dlg.setAcceptHandler(self.acceptHandlerMock)

    def show_and_accept_dialog(self) -> None:
        self.dlg.show()
        self.accept_dialog()

    def show_and_decline_dialog(self) -> None:
        self.dlg.show()
        self.decline_dialog()

    def accept_dialog(self) -> None:
        QTest.mouseClick(self.dlg.dialogButtons.button(QDialogButtonBox.Ok), Qt.LeftButton)

    def decline_dialog(self) -> None:
        QTest.mouseClick(self.dlg.dialogButtons.button(QDialogButtonBox.Cancel), Qt.LeftButton)

    def test_accept_dialog(self) -> None:
        self.show_and_accept_dialog()
        assert self.acceptHandlerMock.call_count == 1

    def test_decline_dialog(self) -> None:
        self.show_and_decline_dialog()
        assert self.acceptHandlerMock.call_count == 0

    def test_custom_true_acceptor(self) -> None:
        self.acceptHandlerMock.return_value = True
        self.show_and_accept_dialog()
        assert not self.dlg.isVisible()

    def test_custom_false_acceptor(self) -> None:
        self.acceptHandlerMock.return_value = False
        self.show_and_accept_dialog()
        assert self.dlg.isVisible()

    def test_custom_acceptor_parameters(self) -> None:
        self.dlg.show()
        self.dlg.nameEdit.setText("MyName")
        self.dlg.ciphertextDirSelector.setDirectory("/my/ciphertext/dir")
        self.dlg.plaintextDirSelector.setDirectory("/my/plaintext/dir")
        self.dlg.password1Edit.setText("MyPassword1")
        self.dlg.password2Edit.setText("MyPassword2")
        self.accept_dialog()
        self.acceptHandlerMock.assert_called_once_with(
            name="MyName", ciphertextDir="/my/ciphertext/dir", plaintextDir="/my/plaintext/dir",
            password1="MyPassword1", password2="MyPassword2")

    def test_enter_accepts(self) -> None:
        self.dlg.show()
        QTest.keyClick(self.dlg, Qt.Key_Enter)
        assert not self.dlg.isVisible()
        assert self.acceptHandlerMock.call_count == 1

    def test_esc_declines(self) -> None:
        self.dlg.show()
        QTest.keyClick(self.dlg, Qt.Key_Escape)
        assert not self.dlg.isVisible()
        assert self.acceptHandlerMock.call_count == 0

    def test_close_declines(self) -> None:
        self.dlg.show()
        self.dlg.close()
        assert not self.dlg.isVisible()
        assert self.acceptHandlerMock.call_count == 0
