import logging
import sys
import os


LOG_FORMATTER = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')


# A stdout Handler for writing dev debugging or platform debugging
STDOUT_HANDLER = logging.StreamHandler(sys.stdout)
STDOUT_HANDLER.setLevel(logging.DEBUG)
STDOUT_HANDLER.setFormatter(LOG_FORMATTER)


def get_logger(name, level=10):
    logger = logging.getLogger(name)

    logging_flag = os.environ.get('REMOTE_WORK_PATH', None)

    if logging_flag is None:
        logger.addHandler(logging.NullHandler())
        return logger

    logger.setLevel(logging.DEBUG)
    logger.addHandler(STDOUT_HANDLER)

    return logger
