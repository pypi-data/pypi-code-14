from __future__ import division, absolute_import, print_function
import abc


class FrameDataSource:
    """Base class for fetching frame data.

    Every data source used by :class:`brite_etl.lib.FrameSet` must use this class
    as a metaclass!

    These are swappable classes that let us get a pandas dataframe of data when the user requests `whatever` frame.
    If you're using the :class:`BriteDataSource <brite_etl.core.io.frame_sources.BriteDataSource>`,
    it will call `BriteDataSource().get('framename')`. If you're using :class:`CsvSource <brite_etl.core.io.frame_sources.CsvSource>`,
    it will read the csv according to the paths you give it.

    :param source: The source for this data.
    """
    __metaclass__ = abc.ABCMeta

    def __init__(self, source):
        self._source = source

    @property
    def source(self):
        return self._source

    @source.setter
    def source(self, source):
        self._source = source

    @abc.abstractmethod
    def get(self, name, prepared=None):
        raise NotImplementedError()
