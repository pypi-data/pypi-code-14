import unittest
from unittest.mock import create_autospec, patch, Mock #type: ignore
import os
import tempfile
from PyQt5.QtCore import Qt #type: ignore
from PyQt5.QtTest import QTest #type: ignore
from PyQt5.QtWidgets import QDialogButtonBox, QMessageBox #type: ignore
from kryptal.gui.controller.CreateFilesystemController import CreateFilesystemController
from kryptal.pluginmanager.IFilesystem import FilesystemCreateException
from kryptal.services.FilesystemCreatorService import FilesystemCreatorService
from nose.tools import assert_equals


class test_CreateFilesystem_Integration(unittest.TestCase):
    def setUp(self) -> None:
        self.serviceMock = create_autospec(FilesystemCreatorService)
        self.createFilesystemController = CreateFilesystemController(self.serviceMock)
        self.tempdir1 = tempfile.TemporaryDirectory()
        self.tempdir2 = tempfile.TemporaryDirectory()

    def tearDown(self) -> None:
        self.tempdir1.cleanup()
        self.tempdir2.cleanup()

    @patch('kryptal.gui.controller.CreateFilesystemController.CreateFilesystemDialog.exec_')
    def showDialog(self, execDialogMock: Mock) -> None:
        # replace modal exec() call with non-modal show() call, so that our test case can continue and isn't blocked.
        execDialogMock.side_effect = self.createFilesystemController._dlg.show
        self.createFilesystemController.create()

    def setDialogValues(self, name: str, ciphertextDir: str, plaintextDir: str, password1: str, password2: str) -> None:
        self.createFilesystemController._dlg.nameEdit.setText(name)
        self.createFilesystemController._dlg.ciphertextDirSelector.directoryEdit.setText(ciphertextDir)
        self.createFilesystemController._dlg.plaintextDirSelector.directoryEdit.setText(plaintextDir)
        self.createFilesystemController._dlg.password1Edit.setText(password1)
        self.createFilesystemController._dlg.password2Edit.setText(password2)

    def acceptDialog(self) -> None:
        QTest.mouseClick(self.createFilesystemController._dlg.dialogButtons.button(QDialogButtonBox.Ok), Qt.LeftButton)

    def declineDialog(self) -> None:
        QTest.mouseClick(self.createFilesystemController._dlg.dialogButtons.button(QDialogButtonBox.Cancel), Qt.LeftButton)

    def showAndAcceptDialogWith(self, name: str, ciphertextDir: str, plaintextDir: str, password1: str, password2: str) -> None:
        self.showDialog()
        self.setDialogValues(name=name, ciphertextDir=ciphertextDir, plaintextDir=plaintextDir, password1=password1, password2=password2)
        self.acceptDialog()

    def test_accept_creates(self) -> None:
        self.showDialog()
        self.setDialogValues(name="My name", ciphertextDir=self.tempdir1.name, plaintextDir=self.tempdir2.name, password1="mypw", password2="mypw")
        self.acceptDialog()
        assert not self.createFilesystemController._dlg.isVisible()
        self.serviceMock.create.assert_called_once_with(name="My name", fstype="CryFS", ciphertextDirectory=self.tempdir1.name,
                                                        plaintextDirectory=self.tempdir2.name, password="mypw".encode(encoding="UTF-8"))

    def test_decline_doesnt_create(self) -> None:
        self.showDialog()
        self.setDialogValues(name="My name", ciphertextDir=self.tempdir1.name, plaintextDir=self.tempdir2.name,
                             password1="mypw", password2="mypw")
        self.declineDialog()
        assert not self.createFilesystemController._dlg.isVisible()
        assert self.serviceMock.create.call_count == 0

    @patch('kryptal.gui.controller.CreateFilesystemController.QMessageBox.warning')
    def test_passwords_mismatch(self, warningBoxMock: Mock) -> None:
        self.showAndAcceptDialogWith(name="My name", ciphertextDir=self.tempdir1.name, plaintextDir=self.tempdir2.name,
                             password1="mypw1", password2="mypw2")
        assert self.serviceMock.create.call_count == 0
        assert warningBoxMock.call_count == 1
        assert "Passwords don't match" in warningBoxMock.call_args[0][2]
        assert self.createFilesystemController._dlg.isVisible()

    @patch('kryptal.gui.controller.CreateDirectoryYesNoController.QMessageBox.question')
    def test_plaintextdir_doesnt_exist_create(self, questionBoxMock: Mock) -> None:
        questionBoxMock.return_value = QMessageBox.Yes
        self.showAndAcceptDialogWith(name="My name", ciphertextDir=self.tempdir1.name,
                                     plaintextDir=os.path.join(self.tempdir2.name, "notexistingsubdir"),
                                     password1="mypw", password2="mypw")
        assert questionBoxMock.call_count == 1  # Assert "Do you want to create the directory?" was asked
        assert "plaintext directory" in questionBoxMock.call_args[0][2]
        assert not self.createFilesystemController._dlg.isVisible()  # Assert dialog closed
        assert os.path.isdir(os.path.join(self.tempdir2.name, "notexistingsubdir"))  # Assert dir was created
        self.serviceMock.create.assert_called_once_with(name="My name", fstype="CryFS",  # Assert filesystem was created
                                                        ciphertextDirectory=self.tempdir1.name,
                                                        plaintextDirectory=os.path.join(self.tempdir2.name, "notexistingsubdir"),
                                                        password="mypw".encode(encoding="UTF-8"))

    @patch('kryptal.gui.controller.CreateDirectoryYesNoController.QMessageBox.question')
    def test_plaintextdir_doesnt_exist_dont_create(self, questionBoxMock: Mock) -> None:
        questionBoxMock.return_value = QMessageBox.No
        self.showAndAcceptDialogWith(name="My name", ciphertextDir=self.tempdir1.name,
                                     plaintextDir=os.path.join(self.tempdir2.name, "notexistingsubdir"),
                                     password1="mypw", password2="mypw")
        assert questionBoxMock.call_count == 1  # Assert "Do you want to create the directory?" was asked
        assert "plaintext directory" in questionBoxMock.call_args[0][2]
        assert self.createFilesystemController._dlg.isVisible()  # Assert dialog still open
        assert not os.path.isdir(os.path.join(self.tempdir2.name, "notexistingsubdir"))  # Assert dir was not created
        assert self.serviceMock.create.call_count == 0 # Assert filesystem was not created

    @patch('kryptal.gui.controller.CreateDirectoryYesNoController.QMessageBox.question')
    def test_ciphertextdir_doesnt_exist_create(self, questionBoxMock: Mock) -> None:
        questionBoxMock.return_value = QMessageBox.Yes
        self.showAndAcceptDialogWith(name="My name",
                                     ciphertextDir=os.path.join(self.tempdir1.name, "notexistingsubdir"),
                                     plaintextDir=self.tempdir2.name, password1="mypw", password2="mypw")
        assert questionBoxMock.call_count == 1  # Assert "Do you want to create the directory?" was asked
        assert "ciphertext directory" in questionBoxMock.call_args[0][2]
        assert not self.createFilesystemController._dlg.isVisible()  # Assert dialog closed
        assert os.path.isdir(os.path.join(self.tempdir1.name, "notexistingsubdir"))  # Assert dir was created
        self.serviceMock.create.assert_called_once_with(name="My name", fstype="CryFS",  # Assert filesystem was created
                                                        ciphertextDirectory=os.path.join(self.tempdir1.name, "notexistingsubdir"),
                                                        plaintextDirectory=self.tempdir2.name,
                                                        password="mypw".encode(encoding="UTF-8"))

    @patch('kryptal.gui.controller.CreateDirectoryYesNoController.QMessageBox.question')
    def test_ciphertextdir_doesnt_exist_dont_create(self, questionBoxMock: Mock) -> None:
        questionBoxMock.return_value = QMessageBox.No
        self.showAndAcceptDialogWith(name="My name",
                                     ciphertextDir=os.path.join(self.tempdir1.name, "notexistingsubdir"),
                                     plaintextDir=self.tempdir2.name, password1="mypw", password2="mypw")
        assert questionBoxMock.call_count == 1  # Assert "Do you want to create the directory?" was asked
        assert "ciphertext directory" in questionBoxMock.call_args[0][2]
        assert self.createFilesystemController._dlg.isVisible()  # Assert dialog still open
        assert not os.path.isdir(os.path.join(self.tempdir1.name, "notexistingsubdir"))  # Assert dir was not created
        assert self.serviceMock.create.call_count == 0  # Assert filesystem was not created

    @patch('kryptal.gui.controller.CreateDirectoryYesNoController.QMessageBox.question')
    def test_bothdirs_dont_exist_create_both(self, questionBoxMock: Mock) -> None:
        questionBoxMock.return_value = QMessageBox.Yes
        self.showAndAcceptDialogWith(name="My name",
                                     ciphertextDir=os.path.join(self.tempdir1.name, "notexistingsubdir"),
                                     plaintextDir=os.path.join(self.tempdir2.name, "notexistingsubdir"),
                                     password1="mypw", password2="mypw")
        assert questionBoxMock.call_count == 2  # Assert "Do you want to create the directory?" was asked twice
        assert not self.createFilesystemController._dlg.isVisible()  # Assert dialog closed
        assert os.path.isdir(os.path.join(self.tempdir1.name, "notexistingsubdir"))  # Assert ciphertext dir was created
        assert os.path.isdir(os.path.join(self.tempdir2.name, "notexistingsubdir"))  # Assert plaintext dir was created
        self.serviceMock.create.assert_called_once_with(name="My name", fstype="CryFS",  # Assert filesystem was created
                                                        ciphertextDirectory=os.path.join(self.tempdir1.name, "notexistingsubdir"),
                                                        plaintextDirectory=os.path.join(self.tempdir2.name, "notexistingsubdir"),
                                                        password="mypw".encode(encoding="UTF-8"))

    @patch('kryptal.gui.controller.CreateDirectoryYesNoController.QMessageBox.question')
    def test_bothdirs_dont_exist_create_one(self, questionBoxMock: Mock) -> None:
        questionBoxMock.side_effect = [QMessageBox.Yes, QMessageBox.No]
        self.showAndAcceptDialogWith(name="My name",
                                     ciphertextDir=os.path.join(self.tempdir1.name, "notexistingsubdir"),
                                     plaintextDir=os.path.join(self.tempdir2.name, "notexistingsubdir"),
                                     password1="mypw", password2="mypw")
        assert questionBoxMock.call_count == 2  # Assert "Do you want to create the directory?" was asked twice
        assert self.createFilesystemController._dlg.isVisible()  # Assert dialog still open
        assert self.serviceMock.create.call_count == 0  # Assert filesystem was not created

    @patch('kryptal.gui.controller.CreateDirectoryYesNoController.QMessageBox.question')
    def test_bothdirs_dont_exist_create_none(self, questionBoxMock: Mock) -> None:
        questionBoxMock.return_value = QMessageBox.No
        self.showAndAcceptDialogWith(name="My name",
                                     ciphertextDir=os.path.join(self.tempdir1.name, "notexistingsubdir"),
                                     plaintextDir=os.path.join(self.tempdir2.name, "notexistingsubdir"),
                                     password1="mypw", password2="mypw")
        assert questionBoxMock.call_count == 1  # Assert "Do you want to create the directory?" was asked only once
        assert self.createFilesystemController._dlg.isVisible()  # Assert dialog still open
        assert not os.path.isdir(os.path.join(self.tempdir1.name, "notexistingsubdir"))  # Assert ciphertext dir was not created
        assert not os.path.isdir(os.path.join(self.tempdir2.name, "notexistingsubdir"))  # Assert plaintextdir was not created
        assert self.serviceMock.create.call_count == 0  # Assert filesystem was not created

    @patch('kryptal.gui.controller.CreateFilesystemController.QMessageBox.critical')
    def test_create_error(self, criticalBoxMock: Mock) -> None:
        self.serviceMock.create.side_effect = Exception()
        self.showAndAcceptDialogWith("My name", self.tempdir1.name, self.tempdir2.name, "mypw", "mypw")
        assert criticalBoxMock.call_count == 1
        assert self.createFilesystemController._dlg.isVisible()
        assert "Failed to create" in criticalBoxMock.call_args[0][2]


    @patch('kryptal.gui.controller.CreateFilesystemController.QMessageBox.critical')
    def test_create_custom_error(self, criticalBoxMock: Mock) -> None:
        self.serviceMock.create.side_effect = FilesystemCreateException("My custom error message")
        self.showAndAcceptDialogWith("My name", self.tempdir1.name, self.tempdir2.name, "mypw", "mypw")
        assert criticalBoxMock.call_count == 1
        assert self.createFilesystemController._dlg.isVisible()
        assert_equals("My custom error message", criticalBoxMock.call_args[0][2])
