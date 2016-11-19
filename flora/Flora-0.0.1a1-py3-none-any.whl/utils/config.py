from sys import argv

import yaml

from .values import CONFIG_FILE


class _Config(type):
    raw_config = yaml.load(open(CONFIG_FILE))
    get = raw_config.get
    update = raw_config.update
    __name__ = 'Config'
    if '--selfbot' in argv and 'SelfBot' in raw_config.keys():
        main = 'SelfBot'
    else:
        main = 'Flora'
    update_main = raw_config[main]

    @property
    def Token(self):
        return self[_Config.main]['Token']

    token = Token

    @property
    def OwnerID(self):
        return self[_Config.main]['OwnerID']


    @property
    def Prefix(self):
        return self[_Config.main]['Prefix']

    prefix = Prefix

    @property
    def SelfBot(self):
        return self[_Config.main]['SelfBot']

    @property
    def Password(self):
        return self[_Config.main]['Password']

    @property
    def Plugins(self):
        return self[_Config.main]['Plugins']

    plugins = Plugins

    def __getitem__(self, item):
        return _Config.raw_config[item]

    def __setitem__(self, key, value):
        _Config.raw_config[key] = value

    def __delitem__(self, key):
        del _Config.raw_config[key]

    @staticmethod
    def reload():
        _Config.__data = yaml.load(open(CONFIG_FILE))

    @staticmethod
    def save():
        with open(CONFIG_FILE, 'w', errors='backslashreplace') as f:
            yaml.safe_dump(_Config.__data, f)





class Config(metaclass=_Config):
    pass
