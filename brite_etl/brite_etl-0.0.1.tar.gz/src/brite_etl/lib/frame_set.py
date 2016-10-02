from typedecorator import params, Union
from brite_etl.utils.types import DeepDict
from brite_etl.abstracts.frame_data_source import FrameDataSource
from brite_etl.exceptions import InvalidFrame
from brite_etl.lib import FrameBuilder
import pandas as pd
from brite_etl import logger


class _FrameDict(DeepDict):
    """
    A Dictionary used by :class:`.FrameSet` for storing/retrieveing frame classes. Shouldn't have to use this directly.

    :type: :class:`brite_etl.utils.types.DeepDict`
    """
    def __init__(self, data_sources):
        self._data_sources = data_sources
        super(self.__class__, self).__init__()

    def reset(self, name):
        self.get(name, fresh=True)

    def get(self, name, empty_frame=False, df=None, fresh=False):
        _og_name = name

        if fresh:
            _is_prepared = name.startswith('prepared')
            if _is_prepared:
                name = name[len('prepared.'):]

            _source = self._data_sources.get('prepared.source' if _is_prepared else 'source')
            _df = _source.get(name)
            return FrameBuilder(_og_name, df=_df)

        # Hasn't been retrieved yet. So we'll get it, then store in our frames object
        if not self.has(name):
            _is_prepared = name.startswith('prepared')
            if _is_prepared:
                name = name[len('prepared.'):]

            _source = self._data_sources.get('prepared.source' if _is_prepared else 'source')

            if (type(df).__name__ is 'DataFrame'):
                _df = df
            elif (_source is None) and (not empty_frame):
                raise InvalidFrame('The DataFrame Source has not been set, cannot get {0}. '.format(_og_name) +
                                   'Set the source, or use `empty_frame=True` param to fetch an empty frame.')
            elif empty_frame:
                logger.info('Getting {0} as an empty frame... '.format(_og_name))
                _df = pd.DataFrame()
            else:
                _df = _source.get(name)
            # _df = pd.DataFrame() if (_source is None) else _source.get(name)
            _frame = FrameBuilder(_og_name, df=_df)

            self.set(_og_name, _frame)

        return super(self.__class__, self).get(_og_name)


class FrameSet(object):
    """Store multiple frames in a single set

    A FrameSet makes it easy to manage multiple isolated instances of frames. You can set a source of frames
    for automatic fetching, and quickly get frames when needed. Frames are stored in a dictionary.
    """
    def __init__(self, name):
        """
        :param name: Name of the frameset. Can be anything.
        :type name: str
        """
        self._name = name
        self._data_sources = DeepDict({})
        self._frames = _FrameDict(self.data_sources)

    @property
    def data_sources(self):
        """
        A Dictionary containing the datasources to be used when fetching frames.

        Probably don't have to use directly, better off using :meth:`.set_data_sources`

        :type: :class:`brite_etl.utils.types.DeepDict`
        """
        return self._data_sources

    @params(self=object, source=Union(FrameDataSource, type(None)), prepared_source=Union(FrameDataSource, type(None)))
    def set_data_sources(self, source=None, prepared_source=None):
        """Set Data Sources to use fetching frames

        :param source: source to use when fetching non-prepared frames, defaults to None
        :type source: :class:`brite_etl.abstracts.FrameDataSource`, optional
        :param prepared_source: source to use when fetching prepared frames, defaults to None
        :type prepared_source: :class:`brite_etl.abstracts.FrameDataSource`, optional
        """
        if source is not None:
            self._data_sources.set('source', source)

        if prepared_source is not None:
            self._data_sources.set('prepared.source', prepared_source)

    @property
    def frames(self):
        """
        A Dictionary containing all frames that have been fetched thus far

        :type: :class:`._FrameDict`
        """
        return self._frames

    @property
    def chain(self):
        """
        :returns: This frameset wrapped in a chain
        """
        from ..utils.chaining import _Chain
        return _Chain()(self)
