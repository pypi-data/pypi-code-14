from unittest.mock import patch, Mock #type: ignore
from PyQt5.QtCore import Qt #type: ignore
from PyQt5.QtTest import QTest #type: ignore
from kryptal.gui import Application
from kryptal.gui.view.widgets.DirSelector import DirSelector
from nose.tools import assert_equals
from os.path import expanduser

app = Application.get_instance_for_test()

def test_init_without_error() -> None:
    DirSelector()

def test_defaults() -> None:
    obj = DirSelector()
    assert_equals("", obj.directory())

def test_set_and_get() -> None:
    obj = DirSelector()
    obj.setDirectory("/home/myuser")
    assert_equals("/home/myuser", obj.directory())

def test_set_value_is_shown() -> None:
    obj = DirSelector()
    obj.setDirectory("/tmp")
    assert_equals("/tmp", obj.directoryEdit.text())

def test_written_value_is_taken() -> None:
    obj = DirSelector()
    obj.directoryEdit.setText("/mydir/bla")
    assert_equals("/mydir/bla", obj.directoryEdit.text())

@patch('kryptal.gui.view.widgets.DirSelector.QFileDialog.selectedFiles')
@patch('kryptal.gui.view.widgets.DirSelector.QFileDialog.exec_')
def test_browse_button_opens_dialog(execMock: Mock, selectedFilesMock: Mock) -> None:
    selectedFilesMock.return_value = ["/home/mydir"] # Have to mock this, because code-under-test calls this to get the result
    obj = DirSelector()
    QTest.mouseClick(obj.browseButton, Qt.LeftButton)
    execMock.assert_called_once_with()

@patch('kryptal.gui.view.widgets.DirSelector.QFileDialog.selectedFiles')
@patch('kryptal.gui.view.widgets.DirSelector.QFileDialog.exec_')
def test_succeed_dialog_changes_value(execMock: Mock, selectedFilesMock: Mock) -> None:
    selectedFilesMock.return_value = ["/home/mydir"]
    execMock.return_value = True
    obj = DirSelector()
    obj.setDirectory("/home/otherdir")
    QTest.mouseClick(obj.browseButton, Qt.LeftButton)
    assert_equals("/home/mydir", obj.directory())

@patch('kryptal.gui.view.widgets.DirSelector.QFileDialog.selectedFiles')
@patch('kryptal.gui.view.widgets.DirSelector.QFileDialog.exec_')
def test_cancel_dialog_doesnt_change_value(execMock: Mock, selectedFilesMock: Mock) -> None:
    selectedFilesMock.return_value = ["/home/mydir"] # Have to mock this, because code-under-test calls this to get the result
    execMock.return_value = False
    obj = DirSelector()
    obj.setDirectory("/home/otherdir")
    QTest.mouseClick(obj.browseButton, Qt.LeftButton)
    assert_equals("/home/otherdir", obj.directory())

@patch('kryptal.gui.view.widgets.DirSelector.QFileDialog.selectedFiles')
@patch('kryptal.gui.view.widgets.DirSelector.QFileDialog.exec_')
@patch('kryptal.gui.view.widgets.DirSelector.QFileDialog.setDirectory')
def test_dialog_is_initialized_with_old_value(setDirectoryMock: Mock, execMock: Mock, selectedFilesMock: Mock) -> None:
    selectedFilesMock.return_value = ["/home/mydir"] # Have to mock this, because code-under-test calls this to get the result
    obj = DirSelector()
    obj.setDirectory("/home/otherdir")
    QTest.mouseClick(obj.browseButton, Qt.LeftButton)
    setDirectoryMock.assert_called_once_with("/home/otherdir")

@patch('kryptal.gui.view.widgets.DirSelector.QFileDialog.selectedFiles')
@patch('kryptal.gui.view.widgets.DirSelector.QFileDialog.exec_')
@patch('kryptal.gui.view.widgets.DirSelector.QFileDialog.setDirectory')
def test_dialog_shows_homedir_if_no_old_dir(setDirectoryMock: Mock, execMock: Mock, selectedFilesMock: Mock) -> None:
    selectedFilesMock.return_value = ["/home/mydir"] # Have to mock this, because code-under-test calls this to get the result
    obj = DirSelector()
    QTest.mouseClick(obj.browseButton, Qt.LeftButton)
    setDirectoryMock.assert_called_once_with(expanduser("~"))
