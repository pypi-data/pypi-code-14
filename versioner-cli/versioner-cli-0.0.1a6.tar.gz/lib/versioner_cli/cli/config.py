import yaml
from os.path import expanduser, join, isfile
from os import environ
from .versioner import Versioner
import logging

logger = logging.getLogger(__name__)

lookup_order = [join(expanduser('~'), '.versioner'), environ.get('VERSIONER_CONFIG'), Versioner.DEFAULT_CONFIG_PATH]


def find_config(*args, **kwargs):
    """

    :param args:
    :param kwargs:
    :return:
    """
    for i, path in enumerate(lookup_order):
        try:
            if isfile(path):
                return lookup_order[i]
        except AttributeError as msg:
            logger.info(msg)

