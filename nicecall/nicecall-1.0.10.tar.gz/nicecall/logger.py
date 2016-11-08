import logging


class Logger():
    def __init__(self, logger, level="DEBUG"):
        if isinstance(logger, str):
            self._logger = logging.getLogger(logger)
            self._logger.addHandler(logging.NullHandler())
        else:
            self._logger = logger

        self._level = logging._nameToLevel[level]

    def log(self, line):
        self._logger.log(self._level, line)


class StdoutLogger(Logger):
    def __init__(self, logger, level="INFO"):
        super().__init__(logger, level)


class StderrLogger(Logger):
    def __init__(self, logger, level="ERROR"):
        super().__init__(logger, level)
