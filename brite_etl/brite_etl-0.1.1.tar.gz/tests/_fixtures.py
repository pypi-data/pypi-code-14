import brite_etl
import pkgutil
import pytest
import os
from collections import namedtuple


@pytest.fixture(scope="session")
def df_cache_dirs(request):
    # print(request.config.__dict__)
    Result = namedtuple('df_cache_exists', 'root prepared')
    return Result(
        request.config.getini('df_cache_root_dir'),
        request.config.getini('df_prep_cache_root_dir')
    )


@pytest.fixture(scope="session")
def df_cache_exists(request, df_cache_dirs):
    """Check that df_root/df_prep cache exists and contains files

    :returns: A named tuple (root, prepared) with True/False indicating if the cache exists
    """
    Result = namedtuple('df_cache_exists', 'root prepared')

    def _check_df(df_dir):
        if os.path.isdir(df_dir):
            files = os.listdir(df_dir)
            if len(files) > 0:
                return True
            else:
                return False
        else:
            return False

    return Result(
        _check_df(df_cache_dirs.root),
        _check_df(df_cache_dirs.prepared)
    )


@pytest.fixture(autouse=True)
def df_cache_ready(request, df_cache_exists):
    """Skip test if the df_cache isn't ready to use.

    Use this decorator: @pytest.mark.df_cache_ready
    Can also skip only for certain df_cache: @pytest.mark.df_cache_ready('prepared')
    """
    marker = request.node.get_marker('df_cache_ready')
    if marker:
        if (len(marker.args) > 0) and (marker.args[0] == 'root' or marker.args[0] == 'prepared'):
            if (not getattr(df_cache_exists, marker.args[0])):
                pytest.skip(marker.args[0] + ' df_cache not downloaded in directory defined in pytest.ini')
        elif (not df_cache_exists.root) or (not df_cache_exists.prepared):
            pytest.skip('df_cache not downloaded in directories defined in pytest.ini')


@pytest.fixture(scope="module")
def csv_sources(request, df_cache_dirs):
    from brite_etl.core.io.frame_sources import CsvSource

    Result = namedtuple('csv_sources', 'root prepared')
    return Result(
        CsvSource(df_cache_dirs.root),
        CsvSource(df_cache_dirs.prepared)
    )


@pytest.fixture(scope="session")
def frame_list():
    _frames = []
    for importer, frame_name, ispkg in pkgutil.iter_modules(brite_etl.frames.__path__):
            if not frame_name.startswith('prepared'):
                _frames.append(frame_name)

    for importer, frame_name, ispkg in pkgutil.iter_modules(brite_etl.frames.prepared.__path__):
        _frames.append('prepared.' + frame_name)

    return _frames


@pytest.fixture(scope="module")
def frame_set():
    _set = brite_etl.lib.FrameSet('test')
    return _set


@pytest.fixture(scope="module")
def frame_set_blanks(request, frame_list):
    def make_frame_set_blanks(include_prepared=False):
        _set = brite_etl.lib.FrameSet('test')

        for frame_name in frame_list:
            if not frame_name.startswith('prepared.'):
                _set.frames.get(frame_name, empty_frame=True)
            elif frame_name.startswith('prepared.') and include_prepared:
                _set.frames.get(frame_name, empty_frame=True)

        return _set

    return make_frame_set_blanks
