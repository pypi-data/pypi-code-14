#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    module myterm.log manage log
"""
import logging
import myterm
import sys

try:
    unicode
    _unicode = True
except NameError:
    _unicode = False


LEVEL = {
    "NOSET": {
        "id": 0,
        "colorfg": myterm.FOREGROUND_NOSET,
        "colorbg": myterm.BACKGROUND_NOSET,
    },
    "DEBUG": {
        "id": 10,
        "colorfg": myterm.FOREGROUND_DEBUG,
        "colorbg": myterm.BACKGROUND_DEBUG,
    },
    "INFO": {
        "id": 20,
        "colorfg": myterm.FOREGROUND_INFO,
        "colorbg": myterm.BACKGROUND_INFO,
    },
    "WARNING": {
        "id": 30,
        "colorfg": myterm.FOREGROUND_WARNING,
        "colorbg": myterm.BACKGROUND_WARNING,
    },
    "ERROR": {
        "id": 40,
        "colorfg": myterm.FOREGROUND_ERROR,
        "colorbg": myterm.BACKGROUND_ERROR,
    },
    "CRITICAL": {
        "id": 50,
        "colorfg": myterm.FOREGROUND_CRITICAL,
        "colorbg": myterm.BACKGROUND_CRITICAL,
    },
}

LEVELNO = {LEVEL[i]["id"]: i for i in LEVEL}

class StreamHandler(logging.Handler):
    """
        StreamHandler with color
    """
    def __init__(self, stream=None):
        logging.Handler.__init__(self)
        if stream is None:
            stream = sys.stderr
        self.stream = stream

    def flush(self):
        self.acquire()
        try:
            if self.stream and hasattr(self.stream, "flush"):
                self.stream.flush()
        finally:
            self.release()

    def emit(self, record):
        stream = sys.__stdout__
        if record.levelno > 30:
            stream = sys.__stderr__
        myterm.SCREEN.set_color(LEVEL[LEVELNO[record.levelno]]["colorfg"],
                                LEVEL[LEVELNO[record.levelno]]["colorbg"],
                                stream)
        try:
            msg = self.format(record)
            fs = "%s\n"
            if not _unicode: #if no unicode support...
                stream.write(fs % msg)
            else:
                try:
                    if (isinstance(msg, unicode) and
                        getattr(stream, 'encoding', None)):
                        ufs = u'%s\n'
                        try:
                            stream.write(ufs % msg)
                        except UnicodeEncodeError:
                            stream.write((ufs % msg).encode(stream.encoding))
                    else:
                        stream.write(fs % msg)
                except UnicodeError:
                    stream.write(fs % msg.encode("UTF-8"))
            self.flush()
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)
        myterm.SCREEN.set_color(myterm.FOREGROUND_DEFAULT,
                                myterm.BACKGROUND_DEFAULT,
                                stream)
logging.StreamHandler = StreamHandler
