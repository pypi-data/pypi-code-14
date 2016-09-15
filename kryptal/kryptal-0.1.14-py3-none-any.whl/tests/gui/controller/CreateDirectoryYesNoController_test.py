import stat
from unittest.mock import patch, Mock #type: ignore
import os
import tempfile
from PyQt5.QtCore import QObject #type: ignore
from PyQt5.QtWidgets import QMessageBox #type: ignore
from kryptal.gui import Application
from kryptal.gui.controller.CreateDirectoryYesNoController import CreateDirectoryYesNoController

app = Application.get_instance_for_test()


class test_CreateDirectoryYesNoController(object):
    def __init__(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.dir_to_create = os.path.join(self.tempdir.name, "mydirname")

    @patch('kryptal.gui.controller.CreateDirectoryYesNoController.QMessageBox.question')
    def test_create(self, questionBoxMock: Mock) -> None:
        questionBoxMock.return_value = QMessageBox.Yes
        obj = CreateDirectoryYesNoController()
        obj.askYesNoAndCreateDir("Mydir", self.dir_to_create)
        assert os.path.isdir(self.dir_to_create)

    @patch('kryptal.gui.controller.CreateDirectoryYesNoController.QMessageBox.question')
    def test_create_returnval(self, questionBoxMock: Mock) -> None:
        questionBoxMock.return_value = QMessageBox.Yes
        obj = CreateDirectoryYesNoController()
        assert obj.askYesNoAndCreateDir("Mydir", self.dir_to_create)

    @patch('kryptal.gui.controller.CreateDirectoryYesNoController.QMessageBox.question')
    def test_create_with_subdir(self, questionBoxMock: Mock) -> None:
        questionBoxMock.return_value = QMessageBox.Yes
        obj = CreateDirectoryYesNoController()
        assert obj.askYesNoAndCreateDir("Mydir", os.path.join(self.dir_to_create, "subdir"))
        assert os.path.isdir(os.path.join(self.dir_to_create, "subdir"))

    @patch('kryptal.gui.controller.CreateDirectoryYesNoController.QMessageBox.question')
    def test_dont_create(self, questionBoxMock: Mock) -> None:
        questionBoxMock.return_value = QMessageBox.No
        obj = CreateDirectoryYesNoController()
        not obj.askYesNoAndCreateDir("Mydir", self.dir_to_create)
        assert not os.path.isdir(self.dir_to_create)

    @patch('kryptal.gui.controller.CreateDirectoryYesNoController.QMessageBox.question')
    def test_dont_create_returnval(self, questionBoxMock: Mock) -> None:
        questionBoxMock.return_value = QMessageBox.No
        obj = CreateDirectoryYesNoController()
        assert not obj.askYesNoAndCreateDir("Mydir", self.dir_to_create)

    @patch('kryptal.gui.controller.CreateDirectoryYesNoController.QMessageBox.question')
    def test_msgbox_parent(self, questionBoxMock: Mock) -> None:
        questionBoxMock.return_value = QMessageBox.No
        parent = QObject()
        obj = CreateDirectoryYesNoController(parent)
        obj.askYesNoAndCreateDir("Mydir", self.dir_to_create)
        assert questionBoxMock.call_count == 1
        assert parent == questionBoxMock.call_args[0][0]

    @patch('kryptal.gui.controller.CreateDirectoryYesNoController.QMessageBox.question')
    def test_msgbox_text(self, questionBoxMock: Mock) -> None:
        questionBoxMock.return_value = QMessageBox.No
        obj = CreateDirectoryYesNoController()
        obj.askYesNoAndCreateDir("Mydir", self.dir_to_create)
        assert questionBoxMock.call_count == 1
        assert "Mydir" in questionBoxMock.call_args[0][2]

    @patch('kryptal.gui.controller.CreateDirectoryYesNoController.QMessageBox.warning')
    @patch('kryptal.gui.controller.CreateDirectoryYesNoController.QMessageBox.question')
    def test_missing_permissions_showswarning(self, questionBoxMock: Mock, warningBoxMock: Mock) -> None:
        questionBoxMock.return_value = QMessageBox.Yes
        os.chmod(self.tempdir.name, 0)
        obj = CreateDirectoryYesNoController()
        obj.askYesNoAndCreateDir("Mydir", self.dir_to_create)
        assert warningBoxMock.call_count == 1
        assert "missing permissions" in warningBoxMock.call_args[0][2]
        os.chmod(self.tempdir.name, stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR) # reset permissions (otherwise tempdir can't be cleaned up)

    @patch('kryptal.gui.controller.CreateDirectoryYesNoController.QMessageBox.warning')
    @patch('kryptal.gui.controller.CreateDirectoryYesNoController.QMessageBox.question')
    def test_missing_permissions_returnval(self, questionBoxMock: Mock, warningBoxMock: Mock) -> None:
        questionBoxMock.return_value = QMessageBox.Yes
        os.chmod(self.tempdir.name, 0)
        obj = CreateDirectoryYesNoController()
        assert not obj.askYesNoAndCreateDir("Mydir", self.dir_to_create)
        os.chmod(self.tempdir.name, stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR) # reset permissions (otherwise tempdir can't be cleaned up)

    @patch('kryptal.gui.controller.CreateDirectoryYesNoController.QMessageBox.warning')
    @patch('kryptal.gui.controller.CreateDirectoryYesNoController.QMessageBox.question')
    def test_invalid_dir_showswarning(self, questionBoxMock: Mock, warningBoxMock: Mock) -> None:
        questionBoxMock.return_value = QMessageBox.Yes
        obj = CreateDirectoryYesNoController()
        obj.askYesNoAndCreateDir("Mydir", "")
        assert warningBoxMock.call_count == 1
        assert "Couldn't create" in warningBoxMock.call_args[0][2]

    @patch('kryptal.gui.controller.CreateDirectoryYesNoController.QMessageBox.warning')
    @patch('kryptal.gui.controller.CreateDirectoryYesNoController.QMessageBox.question')
    def test_invalid_dir_returnval(self, questionBoxMock: Mock, warningBoxMock: Mock) -> None:
        questionBoxMock.return_value = QMessageBox.Yes
        obj = CreateDirectoryYesNoController()
        assert not obj.askYesNoAndCreateDir("Mydir", "")
