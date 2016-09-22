import pytest
from .._cli import cli

f = g = h = i = j = lambda x: int(x) + 4
nest = {
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

def something(input_file, output_file, n_cores: int=3):
    pass

_argvalues = [
    (
        something,
        ['a', 'b'],
        ['a', 'b'],
        [],
    ),
    (
        nest,
        ['subcommand2', '-help'],
        [],
        [('help', None)],
    ),
    (
        nest,
        ['subcommand2', '-help', 'aa'],
        ['aa'],
        [('help', None)],
    ),
    (
        lambda x: 1,
        ['-help', 'aa'],
        ['aa'],
        [('help', None)],
    ),
    (
        lambda x: 2,
        ['bb', '--', '-help'],
        ['bb', '-help'],
        [],
    ),
    (
        lambda x: 3,
        ['cc', '-help'],
        ['cc'],
        [('help', None)],
    ),
    (
        lambda x: 4,
        ['dd'],
        ['dd'],
        [],
    ),
]
@pytest.mark.parametrize('function, argv, positionals, flags', _argvalues)
def test_cli(function, argv, positionals, flags):
    i = cli(function, argv)
    print('Positionals:', i.positionals)
    print('Flags:', i.flags)
    assert i.positionals == positionals
    assert i.flags == flags
