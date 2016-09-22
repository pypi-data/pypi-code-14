import pytest
from urllib.parse import parse_qs
from .._wsgi import _wsgi

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
        '/a/b',
        ['a', 'b'],
        [],
    ),
    (
        nest,
        '/subcommand2?help=',
        [],
        [('help', None)],
    ),
    (
        nest,
        '/subcommand2/aa?help=',
        ['aa'],
        [('help', None)],
    ),
    (
        lambda x: 1,
        '/aa?help=',
        ['aa'],
        [('help', None)],
    ),
    (
        lambda x: 2,
        '/bb/help',
        ['bb', 'help'],
        [],
    ),
    (
        lambda x: 3,
        '/cc?help=',
        ['cc'],
        [('help', None)],
    ),
    (
        lambda x: 4,
        '/dd',
        ['dd'],
        [],
    ),
]
@pytest.mark.parametrize('function, path, positionals, flags', _argvalues)
def test_wsgi(function, path, positionals, flags):
    i = _wsgi(function, FakeRequest(path))
   #print('Positionals:', i.positionals)
   #print('Flags:', i.flags)
    assert i['positionals'] == positionals
    assert i['flags'] == flags

class FakeRequest(object):
    def __init__(self, path):
        self.path = path
    @property
    def path_info(self):
        return self.path.split('?')[0]
    @property
    def GET(self):
        if '?' in self.path:
            x = parse_qs(self.path.partition('?')[2], keep_blank_values=True)
            return FakeMultiDict(x)
        else:
            return {}

class FakeMultiDict(dict):
    def __init__(self, x):
        y = {k:[None if v == '' else v for v in vs] for k,vs in x.items()}
        super(FakeMultiDict, self).__init__(y)
           
    def __getitem__(self, key):
        return super(FakeMultiDict, self).__getitem__(key)
    def getall(self, key):
        return self[key]
