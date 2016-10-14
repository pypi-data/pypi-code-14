import traceback
from typing import List, Type
from types import TracebackType
from PyQt5.QtWidgets import QMessageBox, QApplication #type: ignore
import sys
from wortfilter.MainWindow import MainWindow


class Application(QApplication):
    def __init__(self, argv: List[str]) -> None:
        super(Application, self).__init__(argv)

    def setupUncaughtExceptionHandler(self) -> None:
        sys.excepthook = self._onUncaughtException

    def run(self) -> int:
        mainWindow = MainWindow()
        mainWindow.show()
        return self.exec_()

    def _onUncaughtException(self, type_: Type[BaseException], value: BaseException, trace: TracebackType) -> None:
        exception_msg = ''.join(traceback.format_exception_only(type_, value))
        full_traceback_msg = ''.join(traceback.format_exception(type_, value, trace, chain=True))
        print(exception_msg +"\n" + full_traceback_msg, file=sys.stderr)
        QMessageBox.critical(None, "Error", exception_msg + "\n" + full_traceback_msg)


def get_instance() -> Application:
    return _get_instance(sys.argv)

def get_instance_for_test() -> Application:
    return _get_instance(sys.argv + ["-platform", "offscreen"])

def _get_instance(argv: List[str]) -> Application:
    instance = Application.instance()
    if instance is None:
        instance = Application(argv)
    return instance
