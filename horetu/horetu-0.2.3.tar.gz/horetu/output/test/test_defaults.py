import configparser
import os
import pytest

from .. import defaults

cases = [
    (None, ' ', {}),
    ('a.ini', ' ', {'simple': {'a': '4', 'a-b': '3'}}),
    ('b.ini', ' ', {'bb': {'a': '1'}}),
    ('c.ini', ' ', {'blub': {'blub': {'blub': {'beep': 'boop'}}}}),
    ('d.ini', None, {'calque': 'loanword'}),
]

@pytest.mark.parametrize('filename, config_sep, expected', cases)
def test_defaults(filename, config_sep, expected):
    if filename:
        config_file = os.path.abspath(os.path.join(__file__, '..',
                                                   'configuration-files', filename))
    else:
        config_file = None
    observed = defaults.Defaults(config_file, config_sep)
    assert observed == expected
