from unittest.mock import patch, Mock #type: ignore
from PyQt5.QtCore import Qt #type: ignore
from PyQt5.QtTest import QTest #type: ignore
from kryptal.gui import Application
from kryptal.gui.MainWindow import MainWindow

app = Application.get_instance_for_test()

def test_init_without_error() -> None:
    MainWindow()

@patch('kryptal.gui.view.dialogs.CreateFilesystemDialog.CreateFilesystemDialog.exec_')
def test_show_create_filesystem_dialog(execDialogMock: Mock) -> None:
    window = MainWindow()
    QTest.mouseClick(window.createFilesystemButton, Qt.LeftButton)
    execDialogMock.assert_called_once_with()
