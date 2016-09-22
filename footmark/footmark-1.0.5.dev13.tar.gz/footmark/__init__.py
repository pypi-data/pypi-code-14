#
import datetime
import logging
import logging.config
import os
import ConfigParser
from footmark.pyami.config import FootmarkConfigLocations, LoggingDictConfig

__version__ = '1.0.5.dev.13'
Version = __version__  # for backware compatibility


def init_logging():
    try:
        for file in FootmarkConfigLocations:
            try:
                logging.config.fileConfig(os.path.expanduser(file))
            except:
                logging.config.dictConfig(LoggingDictConfig)
    except:
        pass

init_logging()
log = logging.getLogger('footmark')

def connect_ecs(acs_access_key_id=None, acs_secret_access_key=None, **kwargs):
    """
    :type acs_access_key_id: string
    :param acs_access_key_id: Your AWS Access Key ID

    :type acs_secret_access_key: string
    :param acs_secret_access_key: Your AWS Secret Access Key

    :rtype: :class:`footmark.ecs.connection.ECSConnection`
    :return: A connection to Amazon's ECS
    """
    from footmark.ecs.connection import ECSConnection
    return ECSConnection(acs_access_key_id, acs_secret_access_key, **kwargs)
