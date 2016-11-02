"""
Mambo: Project based configuration

Project based config will override global config

"""


class BaseConfig(object):
    pass


class Development(BaseConfig):
    """
    Config for development environment
    """
    pass


class Production(BaseConfig):
    """
    Config for Production environment
    """
    pass