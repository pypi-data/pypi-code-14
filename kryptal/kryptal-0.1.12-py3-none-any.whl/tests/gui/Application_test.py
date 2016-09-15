from unittest.mock import patch, Mock #type: ignore
from kryptal.gui import Application

app = Application.get_instance_for_test()

@patch('kryptal.gui.Application.QApplication.exec_')
@patch('kryptal.gui.MainWindow.MainWindow.show')
def test_starts_mainloop(mainWindowShowMock: Mock, execMock: Mock) -> None:
    app.run()
    execMock.assert_called_once_with()

@patch('kryptal.gui.Application.QApplication.exec_')
@patch('kryptal.gui.MainWindow.MainWindow.show')
def test_shows_mainwindow(mainWindowShowMock: Mock, execMock: Mock) -> None:
    app.run()
    mainWindowShowMock.assert_called_once_with()
