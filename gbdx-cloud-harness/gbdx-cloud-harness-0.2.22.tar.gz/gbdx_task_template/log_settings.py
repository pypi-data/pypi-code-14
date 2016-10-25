import logging
import sys
import os


LOG_FORMATTER = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')


# A stdout Handler for writing dev debugging or platform debugging
STDOUT_HANDLER = logging.StreamHandler(sys.stdout)
STDOUT_HANDLER.setLevel(logging.DEBUG)
STDOUT_HANDLER.setFormatter(LOG_FORMATTER)


def get_logger(name, level=10):
    remote_work_path = os.environ.get('REMOTE_WORK_PATH', None)
    if remote_work_path is None:
        level = 0  # Don't log for local.
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(STDOUT_HANDLER)
    return logger
