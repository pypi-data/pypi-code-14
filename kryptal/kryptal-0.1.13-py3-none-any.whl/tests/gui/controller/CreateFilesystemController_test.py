from typing import Callable
from unittest.mock import create_autospec, patch, Mock #type: ignore
import os
import tempfile
from kryptal.gui.controller.CreateFilesystemController import CreateFilesystemController
from kryptal.pluginmanager.IFilesystem import FilesystemCreateException
from kryptal.services.FilesystemCreatorService import FilesystemCreatorService
from nose.tools import assert_equals


class CreateFilesystemDialogMock(object):
    def setAcceptHandler(self, acceptHandler: Callable[..., bool]) -> None:
        self._acceptHandler = acceptHandler

    def whenShownAcceptWithValues(self, name: str, ciphertextDir: str, plaintextDir: str, password1: str,
                                  password2: str) -> None:
        self._accept = True
        self._name = name
        self._ciphertextDir = ciphertextDir
        self._plaintextDir = plaintextDir
        self._password1 = password1
        self._password2 = password2

    def clearPasswordFields(self) -> None:
        pass

    def whenShownDecline(self) -> None:
        self._accept = False

    def exec_(self) -> None:
        if self._accept:
            self._acceptHandler(name=self._name, ciphertextDir=self._ciphertextDir, plaintextDir=self._plaintextDir,
                                password1=self._password1, password2=self._password2)


tempdir1 = tempfile.TemporaryDirectory()
tempdir2 = tempfile.TemporaryDirectory()


class test_CreateFilesystemController(object):
    @patch('kryptal.gui.controller.CreateFilesystemController.CreateFilesystemDialog', CreateFilesystemDialogMock)
    def __init__(self) -> None:
        self.serviceMock = create_autospec(FilesystemCreatorService)
        self.obj = CreateFilesystemController(self.serviceMock)

    def test_create(self) -> None:
        self.obj._dlg.whenShownAcceptWithValues("My name", tempdir1.name, tempdir2.name, "mypw", "mypw")
        self.obj.create()
        self.serviceMock.create.assert_called_once_with(name="My name", fstype="CryFS", ciphertextDirectory=tempdir1.name,
                                                        plaintextDirectory=tempdir2.name,
                                                        password="mypw".encode(encoding="UTF-8"))

    @patch('kryptal.gui.controller.CreateFilesystemController.QMessageBox.warning')
    def test_passwords_dont_match_doesnt_create(self, warningBoxMock: Mock) -> None:
        self.obj._dlg.whenShownAcceptWithValues("My name", tempdir1.name, tempdir2.name, "mypw1", "mypw2")
        self.obj.create()
        assert self.serviceMock.create.call_count == 0

    @patch('kryptal.gui.controller.CreateFilesystemController.QMessageBox.warning')
    def test_passwords_dont_match_shows_warning(self, warningBoxMock: Mock) -> None:
        self.obj._dlg.whenShownAcceptWithValues("My name", tempdir1.name, tempdir2.name, "mypw1", "mypw2")
        self.obj.create()
        assert warningBoxMock.call_count == 1
        assert "Passwords don't match" in warningBoxMock.call_args[0][2]

    @patch('kryptal.gui.controller.CreateFilesystemController.CreateDirectoryYesNoController.askYesNoAndCreateDir')
    def test_plaintextdir_doesnt_exist_asks_whether_should_create(self, createDirectoryQuestionMock: Mock) -> None:
        createDirectoryQuestionMock.return_value = False
        self.obj._dlg.whenShownAcceptWithValues("My name", tempdir1.name, os.path.join(tempdir2.name, "notexistingsubdir"),
                                           "mypw", "mypw")
        self.obj.create()
        createDirectoryQuestionMock.assert_called_once_with("plaintext directory",
                                                            os.path.join(tempdir2.name, "notexistingsubdir"))

    @patch('kryptal.gui.controller.CreateFilesystemController.CreateDirectoryYesNoController.askYesNoAndCreateDir')
    def test_plaintextdir_doesnt_exist_create(self, createDirectoryQuestionMock: Mock) -> None:
        createDirectoryQuestionMock.return_value = True
        self.obj._dlg.whenShownAcceptWithValues("My name", tempdir1.name, os.path.join(tempdir2.name, "notexistingsubdir"),
                                           "mypw", "mypw")
        self.obj.create()
        self.serviceMock.create.assert_called_once_with(name="My name", fstype="CryFS", ciphertextDirectory=tempdir1.name,
                                                        plaintextDirectory=os.path.join(tempdir2.name, "notexistingsubdir"),
                                                        password="mypw".encode(encoding="UTF-8"))

    @patch('kryptal.gui.controller.CreateFilesystemController.CreateDirectoryYesNoController.askYesNoAndCreateDir')
    def test_plaintextdir_doesnt_exist_dont_create(self, createDirectoryQuestionMock: Mock) -> None:
        createDirectoryQuestionMock.return_value = False
        self.obj._dlg.whenShownAcceptWithValues("My name", tempdir1.name, os.path.join(tempdir2.name, "notexistingsubdir"),
                                           "mypw", "mypw")
        self.obj.create()
        assert self.serviceMock.create.call_count == 0

    @patch('kryptal.gui.controller.CreateFilesystemController.CreateDirectoryYesNoController.askYesNoAndCreateDir')
    def test_ciphertextdir_doesnt_exist_asks_whether_should_create(self, createDirectoryQuestionMock: Mock) -> None:
        createDirectoryQuestionMock.return_value = False
        self.obj._dlg.whenShownAcceptWithValues("My name", os.path.join(tempdir1.name, "notexistingsubdir"), tempdir2.name,
                                           "mypw", "mypw")
        self.obj.create()
        createDirectoryQuestionMock.assert_called_once_with("ciphertext directory",
                                                            os.path.join(tempdir1.name, "notexistingsubdir"))

    @patch('kryptal.gui.controller.CreateFilesystemController.CreateDirectoryYesNoController.askYesNoAndCreateDir')
    def test_ciphertextdir_doesnt_exist_create(self, createDirectoryQuestionMock: Mock) -> None:
        createDirectoryQuestionMock.return_value = True
        self.obj._dlg.whenShownAcceptWithValues("My name", os.path.join(tempdir1.name, "notexistingsubdir"), tempdir2.name,
                                           "mypw", "mypw")
        self.obj.create()
        self.serviceMock.create.assert_called_once_with(name="My name", fstype="CryFS",
                                                        ciphertextDirectory=os.path.join(tempdir1.name, "notexistingsubdir"),
                                                        plaintextDirectory=tempdir2.name,
                                                        password="mypw".encode(encoding="UTF-8"))

    @patch('kryptal.gui.controller.CreateFilesystemController.CreateDirectoryYesNoController.askYesNoAndCreateDir')
    def test_ciphertextdir_doesnt_exist_dont_create(self, createDirectoryQuestionMock: Mock) -> None:
        createDirectoryQuestionMock.return_value = False
        self.obj._dlg.whenShownAcceptWithValues("My name", os.path.join(tempdir1.name, "notexistingsubdir"), tempdir2.name,
                                           "mypw", "mypw")
        self.obj.create()
        assert self.serviceMock.create.call_count == 0

    @patch('kryptal.gui.controller.CreateFilesystemController.CreateDirectoryYesNoController.askYesNoAndCreateDir')
    def test_bothdirs_dont_exist_asks_whether_should_create(self, createDirectoryQuestionMock: Mock) -> None:
        createDirectoryQuestionMock.return_value = True
        self.obj._dlg.whenShownAcceptWithValues("My name", os.path.join(tempdir1.name, "notexistingsubdir"), os.path.join(tempdir2.name, "notexistingsubdir"),
                                           "mypw", "mypw")
        self.obj.create()
        assert createDirectoryQuestionMock.call_count == 2
        createDirectoryQuestionMock.assert_any_call("ciphertext directory", os.path.join(tempdir1.name, "notexistingsubdir"))
        createDirectoryQuestionMock.assert_any_call("plaintext directory",
                                                       os.path.join(tempdir2.name, "notexistingsubdir"))

    @patch('kryptal.gui.controller.CreateFilesystemController.CreateDirectoryYesNoController.askYesNoAndCreateDir')
    def test_bothdirs_dont_exist_ask_only_once_if_declined(self, createDirectoryQuestionMock: Mock) -> None:
        createDirectoryQuestionMock.return_value = False
        self.obj._dlg.whenShownAcceptWithValues("My name", os.path.join(tempdir1.name, "notexistingsubdir"), os.path.join(tempdir2.name, "notexistingsubdir"),
                                           "mypw", "mypw")
        self.obj.create()
        assert createDirectoryQuestionMock.call_count == 1

    @patch('kryptal.gui.controller.CreateFilesystemController.CreateDirectoryYesNoController.askYesNoAndCreateDir')
    def test_bothdirs_dont_exist_create_both(self, createDirectoryQuestionMock: Mock) -> None:
        createDirectoryQuestionMock.return_value = True
        self.obj._dlg.whenShownAcceptWithValues("My name", os.path.join(tempdir1.name, "notexistingsubdir"), os.path.join(tempdir2.name, "notexistingsubdir"),
                                           "mypw", "mypw")
        self.obj.create()
        self.serviceMock.create.assert_called_once_with(name="My name", fstype="CryFS",
                                                        ciphertextDirectory=os.path.join(tempdir1.name, "notexistingsubdir"),
                                                        plaintextDirectory=os.path.join(tempdir2.name, "notexistingsubdir"),
                                                        password="mypw".encode(encoding="UTF-8"))

    @patch('kryptal.gui.controller.CreateFilesystemController.CreateDirectoryYesNoController.askYesNoAndCreateDir')
    def test_bothdirs_dont_exist_create_one(self, createDirectoryQuestionMock: Mock) -> None:
        createDirectoryQuestionMock.side_effect = [True, False]
        self.obj._dlg.whenShownAcceptWithValues("My name", os.path.join(tempdir1.name, "notexistingsubdir"),
                                           os.path.join(tempdir2.name, "notexistingsubdir"),
                                           "mypw", "mypw")
        self.obj.create()
        assert self.serviceMock.create.call_count == 0

    @patch('kryptal.gui.controller.CreateFilesystemController.CreateDirectoryYesNoController.askYesNoAndCreateDir')
    def test_bothdirs_dont_exist_create_none(self, createDirectoryQuestionMock: Mock) -> None:
        createDirectoryQuestionMock.return_value = False
        self.obj._dlg.whenShownAcceptWithValues("My name", os.path.join(tempdir1.name, "notexistingsubdir"), os.path.join(tempdir2.name, "notexistingsubdir"),
                                           "mypw", "mypw")
        self.obj.create()
        assert self.serviceMock.create.call_count == 0

    @patch('kryptal.gui.controller.CreateFilesystemController.QMessageBox.critical')
    def test_create_error(self, criticalBoxMock: Mock) -> None:
        self.obj._dlg.whenShownAcceptWithValues("My name", tempdir1.name, tempdir2.name, "mypw", "mypw")
        self.serviceMock.create.side_effect = Exception()
        self.obj.create()
        assert criticalBoxMock.call_count == 1
        assert "Failed to create" in criticalBoxMock.call_args[0][2]


    @patch('kryptal.gui.controller.CreateFilesystemController.QMessageBox.critical')
    def test_create_custom_error(self, criticalBoxMock: Mock) -> None:
        self.obj._dlg.whenShownAcceptWithValues("My name", tempdir1.name, tempdir2.name, "mypw", "mypw")
        self.serviceMock.create.side_effect = FilesystemCreateException("My custom error message")
        self.obj.create()
        assert criticalBoxMock.call_count == 1
        assert_equals("My custom error message", criticalBoxMock.call_args[0][2])
