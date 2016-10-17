import logging
import sys


def get_logger(name, level=0):
    logger = logging.getLogger(name)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)

    formatter = logging.Formatter(
            '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    logger.setLevel(level)

    return logger