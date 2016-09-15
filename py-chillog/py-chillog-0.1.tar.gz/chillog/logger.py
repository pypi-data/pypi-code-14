import json
import os
import socket
import time


class Chillog:
    """
    Python library for building logging data structure based on GELF
    More info check http://docs.graylog.org/en/2.1/pages/gelf.html
    """
    LOG_MESSAGE_VERSION = 1

    LOG_ALERT = 1
    LOG_CRITICAL = 2
    LOG_ERROR = 3
    LOG_WARNING = 4
    LOG_NOTICE = 5
    LOG_INFO = 6
    LOG_DEBUG = 7

    def __init__(self, service_name=None, hostname=None):
        """
        Init logger
        Just do this one time and reuse object for best practice
        Ex: `logger = Chillog()` --> use `logger` object to logging

        :param service_name: From which service the log is coming. Default is get value of os environ 'SERVICE_NAME'
        :param hostname: From which host the log is coming. Default is get value of hostname natively with python
        """
        self.__service_name = service_name if service_name else os.environ.get('SERVICE_NAME')
        self.__hostname = hostname if hostname else socket.gethostname()

    @staticmethod
    def __get_current_millis():
        """
        Get current time in milliseconds.

        :return: Current time in milliseconds
        """
        return int(round(time.time() * 1000))

    @staticmethod
    def __add_optional_fields(dict_to_add, **kwargs):
        """
        Add optional field to dict
        Additional field(s) will be preceded with underscore in front of the field name

        :param dict_to_add: Dict to be added with optional field(s)
        :param kwargs: Optional field(s)
        :return: Dict with optional field(s)
        """
        for key, value in kwargs.items():
            key = '_' + str(key)
            dict_to_add[key] = value

        return dict_to_add

    @staticmethod
    def __print_log(formatted_log):  # pragma: no cover
        """
        Print formatted log prettify

        :param formatted_log: Formatted JSON log
        :return: Print to stdout
        """
        print json.dumps(formatted_log, indent=4, sort_keys=True)

    def build_log_message(self, log_level, short_message, **kwargs):
        """
        Build log message in Chillog format

        :param log_level: Level of log
        :param short_message: Short message about the event
        :param kwargs: Additional field(s)
        :return: Dict of formatted log
        """
        expected_level = [
            self.LOG_ALERT,
            self.LOG_CRITICAL,
            self.LOG_ERROR,
            self.LOG_WARNING,
            self.LOG_NOTICE,
            self.LOG_INFO,
            self.LOG_DEBUG
        ]

        if log_level not in expected_level:
            log_level = self.LOG_INFO

        formatted_log = {
            'version': self.LOG_MESSAGE_VERSION,
            'host': self.__hostname,
            'service': self.__service_name,
            'short_message': short_message,
            'full_message': kwargs.get('full_message'),
            'timestamp': self.__get_current_millis(),
            'level': log_level
        }

        if kwargs.get('full_message'):
            del kwargs['full_message']

        formatted_log = self.__add_optional_fields(formatted_log, **kwargs)

        return formatted_log

    def debug(self, short_message, **kwargs):  # pragma: no cover
        """
        Format log with debug level

        :param short_message: Short log message
        :param kwargs: Additional param(s)
        :return: Print formatted log to stdout
        """
        formatted_log = self.build_log_message(log_level=self.LOG_DEBUG,
                                               short_message=short_message,
                                               **kwargs)
        self.__print_log(formatted_log)

    def info(self, short_message, **kwargs):  # pragma: no cover
        """
        Format log with info level

        :param short_message: Short log message
        :param kwargs: Additional param(s)
        :return: Print formatted log to stdout
        """
        formatted_log = self.build_log_message(log_level=self.LOG_INFO,
                                               short_message=short_message,
                                               **kwargs)
        self.__print_log(formatted_log)

    def notice(self, short_message, **kwargs):  # pragma: no cover
        """
        Format log with notice level

        :param short_message: Short log message
        :param kwargs: Additional param(s)
        :return: Print formatted log to stdout
        """
        formatted_log = self.build_log_message(log_level=self.LOG_NOTICE,
                                               short_message=short_message,
                                               **kwargs)
        self.__print_log(formatted_log)

    def warning(self, short_message, **kwargs):  # pragma: no cover
        """
        Format log with warning level

        :param short_message: Short log message
        :param kwargs: Additional param(s)
        :return: Print formatted log to stdout
        """
        formatted_log = self.build_log_message(log_level=self.LOG_WARNING,
                                               short_message=short_message,
                                               **kwargs)
        self.__print_log(formatted_log)

    def error(self, short_message, **kwargs):  # pragma: no cover
        """
        Format log with error level

        :param short_message: Short log message
        :param kwargs: Additional param(s)
        :return: Print formatted log to stdout
        """
        formatted_log = self.build_log_message(log_level=self.LOG_ERROR,
                                               short_message=short_message,
                                               **kwargs)
        self.__print_log(formatted_log)

    def critical(self, short_message, **kwargs):  # pragma: no cover
        """
        Format log with critical level

        :param short_message: Short log message
        :param kwargs: Additional param(s)
        :return: Print formatted log to stdout
        """
        formatted_log = self.build_log_message(log_level=self.LOG_CRITICAL,
                                               short_message=short_message,
                                               **kwargs)
        self.__print_log(formatted_log)

    def alert(self, short_message, **kwargs):  # pragma: no cover
        """
        Format log with alert level

        :param short_message: Short log message
        :param kwargs: Additional param(s)
        :return: Print formatted log to stdout
        """
        formatted_log = self.build_log_message(log_level=self.LOG_ALERT,
                                               short_message=short_message,
                                               **kwargs)
        self.__print_log(formatted_log)
