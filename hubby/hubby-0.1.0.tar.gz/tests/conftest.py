import pytest

import tempfile as _tempfile
from collections import namedtuple
import textwrap
import os
import shutil

GitOrigin = namedtuple('GitOrigin', 'user url show_output')

@pytest.yield_fixture
def tempfile():
    temp = _tempfile.NamedTemporaryFile(delete=False, mode='w')
    try:
        yield temp
    finally:
        try:
            os.remove(temp.name)
        except FileNotFoundError:
            pass


@pytest.yield_fixture
def tempdir():
    temp = _tempfile.mkdtemp()
    try:
        yield temp
    finally:
        shutil.rmtree(temp)


GIT_SHOW_REMOTE_ORIGIN_OUTPUTS = [
    GitOrigin('thusoy', 'git-pull-request', textwrap.dedent('''\
        * remote origin
          Fetch URL: github:thusoy/git-pull-request
          Push  URL: github:thusoy/git-pull-request
          HEAD branch: (not queried)
          Remote branch: (status not queried)
            master
          Local branch configured for 'git pull':
            master merges with remote master
          Local ref configured for 'git push' (status not queried):
            (matching) pushes to (matching)
    ''')),
    GitOrigin('saltstack', 'salt', textwrap.dedent('''\
        * remote origin
          Fetch URL: https://github.com/saltstack/salt
          Push  URL: https://github.com/saltstack/salt
          HEAD branch: (not queried)
          Remote branch: (status not queried)
            develop
          Local branch configured for 'git pull':
            develop merges with remote develop
          Local ref configured for 'git push' (status not queried):
            (matching) pushes to (matching)
        ''')),
    GitOrigin('thusoy', 'git-pull-request', textwrap.dedent('''\
        * remote origin
  Fetch URL: git@github.com:thusoy/git-pull-request
  Push  URL: git@github.com:thusoy/git-pull-request
  HEAD branch: (not queried)
  Remote branch: (status not queried)
    master
  Local branch configured for 'git pull':
    master merges with remote master
  Local ref configured for 'git push' (status not queried):
    (matching) pushes to (matching)
        ''')),
]


@pytest.fixture(params=GIT_SHOW_REMOTE_ORIGIN_OUTPUTS)
def git_origin(request):
    return request.param
