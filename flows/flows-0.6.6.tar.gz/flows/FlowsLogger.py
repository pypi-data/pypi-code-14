#!/usr/bin/env python

'''
FlowsLogger.py
Logging facility module for flows
----------------------------------

Copyright 2016 Davide Mastromatteo
License: Apache-2.0
'''

import logging
import threading

from flows import Global


class FlowsLogger:
    """
    FlowsLogger class
    Logger Factory
    """

    _instance = None
    _instance_lock = threading.Lock()
    _logger_instance = None

    @classmethod
    def default_instance(cls):
        """For use like a singleton, return the existing instance of the object or a new instance"""
        if cls._instance is None:
            with cls._instance_lock:
                if cls._instance is None:
                    cls._instance = FlowsLogger()

        return cls._instance

    def get_logger(self):
        """Returns the standard logger"""
        if self._logger_instance is None:
            self._logger_instance = logging.getLogger("flowsLogger")
            self._logger_instance.setLevel(logging.DEBUG)

            log_format = '%(asctime)s - %(message)s'
            log_date_format = '%Y-%m-%d %H:%M:%S'
            formatter = logging.Formatter(log_format, log_date_format)

            new_log_stream_handler = logging.StreamHandler()
            new_log_stream_handler.setFormatter(formatter)
            new_log_stream_handler.setLevel(Global.CONFIG_MANAGER.log_level)

            self._logger_instance.addHandler(new_log_stream_handler)

        return self._logger_instance
