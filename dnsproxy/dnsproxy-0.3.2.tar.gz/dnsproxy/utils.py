import logging


def setup_logging(loglevel_name):
    logging.basicConfig(
        level=getattr(logging, loglevel_name),
        format='[%(asctime)s][%(levelname)s]%(message)s',
    )
