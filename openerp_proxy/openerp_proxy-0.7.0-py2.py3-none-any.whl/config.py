# from .utils import AttrDict
__all__ = ('config',)


class Config(object):
    def __init__(self, data):
        assert isinstance(data, dict), "Data must be instace of dict"
        self._data = {} if data is None else dict(data)

    def parse(self):
        """Parse config values


        """

    def get(self, opt, default=None):
        return self._data.get(opt, default)

    def set(self, opt, val):
        self._date[opt] = val
        return val
