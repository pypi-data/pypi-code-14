"""
.. py:module:: brite_etl.core.io.frame_sources


Options for sources to use when fetching data for dataframes.
"""
from brite_etl.abstracts.frame_data_source import FrameDataSource
import pandas as pd

__api__ = ['BriteDataSource', 'CsvSource']


class BriteDataSource(FrameDataSource):
    """Use BriteDataFrame or PreparedDataFrame to fetch dataframes

    This is a simple wrapper that will call `.get_dataframe()` on the passed class
    to retrieve the dataframes.
    """
    def get(self, name):
        _class = self.source
        return _class.get_dataframe(name)


class CsvSource(FrameDataSource):
    """Use pandas.read_csv() to fetch dataframes

    This will use the path and name of frame to read the dataframe's csv file and
    return it as a dataframe.
    """
    def get(self, name):
        _path = self.source
        return pd.read_csv('{0}/{1}.csv'.format(_path, name), escapechar='\\')
