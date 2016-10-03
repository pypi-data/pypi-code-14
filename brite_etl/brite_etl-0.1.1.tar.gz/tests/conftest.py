# flake8: noqa
from __future__ import absolute_import

import pytest

def pytest_addoption(parser):
    parser.addini('df_cache_root_dir', 'directory of the df_cache_root files')
    parser.addini('df_prep_cache_root_dir', 'directory of the df_prep_cache_root files')

from ._fixtures import *





