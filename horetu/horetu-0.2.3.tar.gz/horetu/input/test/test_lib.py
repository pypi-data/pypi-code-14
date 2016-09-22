import pytest
from ..lib import getsection

f = g = h = i = j = lambda x: int(x) + 4
commands = {
    'subcommand1': {
        'subsubcommand1.1': f,
        'subsubcommand1.2': g,
    },
    'subcommand2': h,
    'subcommand3': {
        'subsubcommand3.1': i,
        'subsubcommand3.2': {
            'subsubsubcommand3.2.1': j,
        }
    },
}

def k(*args):
    return 'blah'

def f1(a:int, b:int, c:int):
    return a + b - c
def f2(a:int, b:int):
    return a * b
def f3():
    return 2
fs = {'f1': f1, 'f2': f2, 'f3': f3}

_testcases = [
    (commands, ['subcommand2', '-help'], ('subcommand2',)),
    (commands, ['subcommand2', 'hoeu', 'ou', 'sth'], ('subcommand2',)),
    (k, [], tuple()),
    (k, ['a', 'b', 'c'], tuple()),
    ({'a': k}, ['a', 'b', 'c'], ('a',)),
    (fs, ['f1', '8', '2', '9'], ('f1',)),
    (fs, ['f2', '8', '2'], ('f2',)),
]
@pytest.mark.parametrize('functions, argv, exp', _testcases)
def test_getsection(functions, argv, exp):
    obs = getsection(True, functions, argv)
    assert obs.section == exp
