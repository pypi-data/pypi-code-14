from __future__ import division, absolute_import, print_function
import abc
from pydash import human_case, title_case


class _FrameSingleton(type):
    __metaclass__ = abc.ABCMeta

    def __init__(cls, name, bases, dict):
        super(_FrameSingleton, cls).__init__(name, bases, dict)
        cls.instance = None

    def __call__(cls, *args, **kw):
        if cls.instance is None:
            cls.instance = super(_FrameSingleton, cls).__call__(*args, **kw)

        return cls.instance


class Frame(object):
    """
    Base class for all frames

    Contains methods shared by all frames, and provides default configuration.
    """
    __metaclass__ = _FrameSingleton

    def __init__(self, df):
        self._df = df
        self._config = self._merge_config(self._base_config, self._config)

    def _merge_config(self, base, new):
        for key, value in base.items():
            if key not in new:
                if value['required']:
                    raise LookupError('{0} must be defined in frame config'.format(key))
                else:
                    new[key] = value['default']
        return new

    @property
    def _base_config(self):
        return {
            'name': {
                'default': None,
                'required': True
            },
            'display_name': {
                'default': title_case(human_case(self.__class__.__name__)),
                'required': False
            },
            'prepared': {
                'default': False,
                'required': False
            },
            'column_map': {
                'default': {},
                'required': False
            }
        }

    @property
    def df(self):
        """Original pandas dataframe

        :returns: The actual dataframe being wrapped by this class
        :rtype: `pandas.DataFrame <http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.html#pandas-dataframe>`_
        """
        return self._df

    @df.setter
    def df(self, value):
        self._df = value

    @property
    def config(self):
        """Configuration dict

        :returns: a dict that has merged the frame config with the base frame class config.
        :rtype: dict
        """
        return self._config

    @property
    def chain(self):
        """
        :returns: This frame wrapped in a chain
        """
        from ..utils.chaining import _Chain
        return _Chain()(self.df)
