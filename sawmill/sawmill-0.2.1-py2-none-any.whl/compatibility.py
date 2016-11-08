# :coding: utf-8
# :copyright: Copyright (c) 2013 Martin Pengelly-Phillips
# :license: See LICENSE.txt.

import logging
import os
import traceback

import sawmill
import sawmill.log


def redirect_standard_library_logging():
    '''Redirect standard library logging to Sawmill.

    Replace any existing handlers on the standard library root logger with a
    single :class:`RedirectToSawmillHandler`. Other handlers should be left
    untouched.

    In addition, unset any level filter on the standard library root logger to
    ensure logs are passed through.

    '''
    sawmill_handler = RedirectToSawmillHandler()
    sawmill_handler.setFormatter(SawmillFormatter())

    del logging.root.handlers[:]
    logging.root.addHandler(sawmill_handler)

    logging.root.setLevel(logging.NOTSET)

    return sawmill_handler


class RedirectToSawmillHandler(logging.Handler):
    '''Redirect to Sawmill.'''

    def __init__(self, target=sawmill.root, *args, **kwargs):
        '''Initialise handler.

        *target* should be the Sawmill handler to redirect to.

        '''
        self.target = target
        super(RedirectToSawmillHandler, self).__init__(*args, **kwargs)

    def emit(self, record):
        '''Emit *record* to Sawmill.

        .. note::

            It is the responsibility of the attached formatter to convert the
            *record* to a Sawmill :class:`~sawmill.log.Log` instance.

        '''
        log = self.format(record)
        self.target.handle(log)


class SawmillFormatter(logging.Formatter):
    '''Format records for use by Sawmill.'''

    def __init__(self):
        '''Initialise formatter.'''
        super(SawmillFormatter, self).__init__()

    def format(self, record):
        '''Return Sawmill :class:`~sawmill.log.Log` instance from *record*.'''
        log = sawmill.log.Log()

        log['name'] = record.name
        log['message'] = record.getMessage()

        level = self._format_level(record.levelno)
        if level is not None:
            log['level'] = level

        if record.exc_info:
            log['traceback'] = os.linesep.join(
                traceback.format_exception(*record.exc_info)
            ).strip(os.linesep)

        log['timestamp'] = record.created

        additional_data = self._extract_additional_data(record)
        log.update(**additional_data)

        return log

    @staticmethod
    def _format_level(level):
        '''Return *level* converted to Sawmill level.'''
        if level >= logging.ERROR:
            return 'error'
        if level >= logging.WARNING:
            return 'warning'
        if level >= logging.INFO:
            return 'info'

        return 'debug'

    @staticmethod
    def _extract_additional_data(record):
        '''Return additional data from *record* as mapping.'''
        data = vars(record).copy()
        for key in (
            'name', 'msg', 'args', 'levelname', 'levelno', 'pathname',
            'filename', 'module', 'exc_info', 'exc_text', 'lineno', 'funcName',
            'created', 'msecs', 'relativeCreated', 'thread', 'threadName',
            'greenlet', 'processName', 'process'
        ):
            data.pop(key, None)

        return data
