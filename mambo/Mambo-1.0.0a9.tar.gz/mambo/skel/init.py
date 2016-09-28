# Mambo

import os

# ------------------------------------------------------------------------------
# A convenient utility to access data path from your application and config files

# The application directory
# /application
APP_DIR = os.path.dirname(__file__)

# Data directory
# application/_data
DATA_DIR = os.path.join(APP_DIR, "_data")


def get_app_data_path(path):
    """
    get the path stored in the 'application/_data' directory
    :param path: string
    :return: string
    """
    return os.path.join(DATA_DIR, path)
# ------------------------------------------------------------------------------
