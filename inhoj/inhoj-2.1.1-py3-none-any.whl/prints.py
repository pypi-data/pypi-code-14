"""
Print in terminal with colors

Based in http://stackoverflow.com/a/34443116 and http://stackoverflow.com/a/17064509
"""

import logging


logger_level = 100
logger_name = __name__
logger_filename = "logger.log"
logger_enabled = False


BLUE = '\033[94m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
CYAN = '\033[96m'
RED = '\033[91m'
ENDC = '\033[0m'


def trace(text):
    print(CYAN + "{}".format(text) + ENDC)
    __log_handler("trace: " + text)


def info(text):
    print(GREEN + "{}".format(text) + ENDC)
    __log_handler("info: " + text)


def warn(text):
    print(YELLOW + "{}".format(text) + ENDC)
    __log_handler("warn: " + text)


def err(text):
    print(RED + "{}".format(text) + ENDC)
    __log_handler("err: " + text)


def log_handler_config(name=logger_name, filename=logger_filename, enabled=logger_enabled):
    global logger_name
    global logger_filename
    global logger_enabled

    logger_name = name
    logger_filename = filename
    logger_enabled = enabled


def __log_handler(message):
    if logger_enabled:
        logger = logging.getLogger(logger_name)

        fh = logging.FileHandler(logger_filename)
        formatter = logging.Formatter('%(asctime)s (%(name)s) - %(message)s')

        fh.setFormatter(formatter)
        logger.addHandler(fh)

        logger.setLevel(logger_level)

        logger.log(logger_level, message)
