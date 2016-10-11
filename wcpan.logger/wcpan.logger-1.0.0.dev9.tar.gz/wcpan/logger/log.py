import datetime
import logging
from typing import Any, Generator, Iterable, List, Optional


class Logger(object):

    def __init__(self, name: str, level: str) -> None:
        super().__init__()
        self._logger = logging.getLogger(name)
        self._level = level
        self._parts = []

    def __lshift__(self, part: Any) -> 'Logger':
        self._parts.append(str(part))
        return self

    def __del__(self) -> None:
        msg = ' '.join(self._parts)
        log = getattr(self._logger, self._level)
        log(msg)


def DEBUG(name: str) -> Logger:
    return Logger(name, 'debug')


def INFO(name: str) -> Logger:
    return Logger(name, 'info')


def WARNING(name: str) -> Logger:
    return Logger(name, 'warning')


def ERROR(name: str) -> Logger:
    return Logger(name, 'error')


def CRITICAL(name: str) -> Logger:
    return Logger(name, 'critical')


def EXCEPTION(name: str) -> Logger:
    return Logger(name, 'exception')


def setup(log_name_list: Iterable[str], file_path: str = None) -> List[logging.Logger]:
    formatter = logging.Formatter('{asctime}|{levelname:_<8}|{message}',
                                  style='{')
    handler = create_handler(file_path, formatter)
    return list(bind_to_logger(handler, log_name_list))


def create_handler(path: Optional[str], formatter: logging.Formatter) -> logging.Handler:
    if path:
        # alias
        TRFHandler = logging.handlers.TimedRotatingFileHandler
        # rotate on Sunday
        handler = TRFHandler(path, when='w6', atTime=datetime.time())
    else:
        handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(formatter)
    return handler


def bind_to_logger(handler: logging.Handler, names: Iterable[str]) -> Generator[logging.Logger, None, None]:
    for name in names:
        logger = create_logger(name)
        logger.addHandler(handler)
        yield logger


def create_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.propagate = False
    logger.setLevel(logging.DEBUG)
    return logger
