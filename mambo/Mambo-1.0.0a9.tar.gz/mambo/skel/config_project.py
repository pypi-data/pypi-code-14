"""
Mambo: Project based configuration

Project based config will override global config

"""


class Development(object):
    """
    Config for development environment
    """
    DEBUG = True
    SECRET_KEY = "PLEASE CHANGE ME"


class Production(object):
    """
    Config for Production environment
    """
    DEBUG = False
    SECRET_KEY = None