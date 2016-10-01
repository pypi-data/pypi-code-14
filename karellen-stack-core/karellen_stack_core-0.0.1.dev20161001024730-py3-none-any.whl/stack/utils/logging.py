#
#  -*- coding: utf-8 -*-
#
# (C) Copyright 2016 Karellen, Inc. (http://karellen.co/)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from logging import (Logger,
                     StreamHandler,
                     getLogger,
                     Formatter,
                     LogRecord,
                     addLevelName,
                     shutdown,
                     DEBUG,
                     INFO,
                     WARNING,
                     WARN,
                     FATAL,
                     ERROR,
                     CRITICAL)

from karellen.stack.utils.colors import (esc,
                                         COLOR_RESET,
                                         RED, BRIGHT, BLINK, YELLOW, GRAY, BLACK)

__all__ = ['ColorizedFormatter',
           'esc',
           'LEVEL_MINIMUM',
           'configure_logging',
           'shutdown_logging',
           'TRACE',
           'LOGGING_FORMAT'
           ]

LEVEL_MINIMUM = 1

CRITICAL = CRITICAL
FATAL = FATAL
ERROR = ERROR
WARNING = WARNING
WARN = WARN
INFO = INFO
DEBUG = DEBUG
TRACE = 5
addLevelName(5, 'TRACE')

LOGGING_FORMAT = "%(asctime)s: %(color)s%(levelname)s: %(name)s%(nocolor)s: %(message)s"

DEFAULT_COLOR_PALLETE = {
    'CRITICAL': esc(RED, BRIGHT, BLINK),
    'ERROR': esc(RED, BRIGHT),
    'WARNING': esc(YELLOW, BRIGHT),
    'INFO': esc(GRAY, BRIGHT),  # white
    'DEBUG': esc(GRAY),
    'TRACE': esc(BLACK, BRIGHT)  # dark gray
}


class ColorizedFormatter(Formatter):
    def __init__(self, fmt=None, datefmt=None, style='%', color_palette=DEFAULT_COLOR_PALLETE, colorize=True):
        super().__init__(fmt, datefmt, style)
        self._palette = color_palette
        self._colorize = colorize

    def format(self, record: LogRecord):
        levelname = record.levelname
        color = self._palette.get(levelname, None)
        if self._colorize and color:
            record.color = color
            record.nocolor = COLOR_RESET
        else:
            record.color = ''
            record.nocolor = ''

        return super().format(record)


def configure_logging(format, level, is_root, colorize):
    if is_root:
        logger = Logger.root
    else:
        logger = getLogger("karellen")
        logger.propagate = False

    for h in list(logger.handlers):
        logger.removeHandler(h)

    logger.addHandler(StreamHandler())
    logger.setLevel(level)

    formatter = ColorizedFormatter(format, colorize=colorize)

    for h in logger.handlers:
        h.setLevel(LEVEL_MINIMUM)
        h.setFormatter(formatter)


def shutdown_logging(is_root):
    if not is_root:
        logger = getLogger("karellen")
        for h in list(logger.handlers):
            logger.removeHandler(h)
            try:
                h.acquire()
                h.flush()
                h.close()
            except (OSError, ValueError):
                # Ignore errors which might be caused
                # because handlers have been closed but
                # references to them are still around at
                # application exit.
                pass
            finally:
                h.release()
    shutdown()
