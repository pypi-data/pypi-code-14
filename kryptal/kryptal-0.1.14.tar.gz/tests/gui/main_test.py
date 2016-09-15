from unittest.mock import patch, Mock #type: ignore
from kryptal.gui import Application
from kryptal.gui import __main__

app = Application.get_instance_for_test()

@patch('kryptal.gui.Application.Application.run')
@patch('sys.exit')
def test_runs_application(exitMock: Mock, runMock: Mock) -> None:
    runMock.return_value = 0
    __main__.main()
    runMock.assert_called_once_with()

@patch('kryptal.gui.Application.QApplication.exec_')
@patch('kryptal.gui.MainWindow.MainWindow.show')
@patch('sys.exit')
def test_shows_mainwindow(exitMock: Mock, mainWindowShowMock: Mock, execMock: Mock) -> None:
    __main__.main()
    mainWindowShowMock.assert_called_once_with()
