from __future__ import print_function

import os
import errno
import shutil
import unittest
import tempfile
import datetime

import pyconfreader

class TestCase(unittest.TestCase):
    def assertConf(self, result, d):
        # ignore any symbols that begin with _
        self.assertEqual({key:value for key, value in result.items() if not key.startswith('_')}, d)


class SimpleTestCase(TestCase):

    def test_simple(self):
        self.assertConf(pyconfreader.loads('i=3'),
                        {'i': 3})
        self.assertConf(pyconfreader.loads('i=3\n'),
                        {'i': 3})
        self.assertConf(pyconfreader.loads('\ni=3\n'),
                        {'i': 3})
        self.assertConf(pyconfreader.loads('i="3"\nj=i*2'),
                        {'i': '3', 'j': '33'})

    def test_vars(self):
        vars = {'i': 10}
        self.assertConf(pyconfreader.loads('i *= 3', vars=vars),
                        {'i': 30})

        # and make sure the locals were updated
        self.assertEqual(vars, {'i': 30})


class TestSimpleLoader(TestCase):
    def setUp(self):
        # create a temporary directory
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        # remove the directory after the test
        shutil.rmtree(self.test_dir)

    def write_file(self, filename, contents):
        filename = os.path.join(self.test_dir, filename)

        # create the directory, in case we're writing to a subdirectory
        dirname = os.path.dirname(filename)
        try:
            os.makedirs(dirname)
        except OSError as exc:
            if exc.errno == errno.EEXIST and os.path.isdir(dirname):
                pass
            else:
                raise

        with open(filename, 'w') as fl:
            fl.write(contents)

    def with_files(self, file_map, default_file, d, vars=None, fl_validator=None):
        for filename, contents in file_map.items():
            self.write_file(os.path.join(self.test_dir, filename), contents)

        loader = pyconfreader.SimpleFileLoader(self.test_dir, vars=vars, fl_validator=fl_validator)
        self.assertConf(loader(default_file), d)

    def test_input_vars(self):
        vars = {'x': 'hi', 'j': []}
        self.with_files({'foo.cfg': '''
x *= 3
j += 'a'
''',
                         },
                        'foo.cfg',
                        {'x': 'hihihi', 'j': ['a']},
                        vars=vars)

    def test_loader(self):
        self.with_files({'foo.cfg': '''
x = 3
''',
                         },
                        'foo.cfg',
                        {'x': 3})

    def test_loader_include(self):
        self.with_files({'foo.cfg': '''
x = 3
include('bar.cfg')
''',
                         'bar.cfg': '''
j=x*3
''',
                         },
                        'foo.cfg',
                        {'x': 3, 'j': 9})

    def test_loader_include_import(self):
        self.with_files({'foo.cfg': '''
_day = 19
x=3
# make sure we can use the imported module in the included file
import datetime as _datetime
include('bar.cfg')
''',
                         'bar.cfg': '''
j=_datetime.date(2016, 8, _day)
''',
                         },
                        'foo.cfg',
                        {'x': 3, 'j': datetime.date(2016, 8, 19)})

    def test_loader_include_import_1(self):
        self.with_files({'foo.cfg': '''
_day = 19
x=3
# make sure we can use the module that was imported in the include file
include('bar.cfg')
j=_datetime.date(2016, 8, _day)
''',
                         'bar.cfg': '''
import datetime as _datetime
''',
                         },
                        'foo.cfg',
                        {'x': 3, 'j': datetime.date(2016, 8, 19)})

    def test_function_access_to_module_globals(self):
        self.with_files({'foo.cfg': '''
v = 100
def _f(i):
    return v + i   # use a module global
x = _f(2)
''',
                         },
                        'foo.cfg',
                        {'x': 102, 'v': 100})

    def test_validator(self):
        def validator(fl, filename):
            if os.path.basename(filename) == 'bar.cfg':
                raise ValueError('cannot load {}: {}'.format(fl, filename))

        self.assertRaises(ValueError, self.with_files,
                          {'foo.cfg': '''
include('bar.cfg')
''',
                           'bar.cfg': '''
x=0
''',
                           },
                          'foo.cfg',
                          {'x': 3, 'j': datetime.date(2016, 8, 19)},
                          fl_validator=validator)


class TestToNamedtuple(unittest.TestCase):
    def test(self):
        result = pyconfreader.to_namedtuple({'x': 3, 'y': 'hi'})

        # make sure it's a namedtuple
        self.assertTrue(hasattr(result, '_fields'))

        self.assertEqual(result._asdict(), {'x': 3, 'y': 'hi'})

    def test_default_predicate(self):
        result = pyconfreader.to_namedtuple({'x': 3, '_y': 'hi', 'pyconfreader': pyconfreader})
        self.assertEqual(result._asdict(), {'x': 3})

    def test_empty_custom_predicate(self):
        def predicate(key, value):
            return True
        result = pyconfreader.to_namedtuple({'x': 3, '_y': 'hi', 'pyconfreader': pyconfreader}, predicate=predicate)
        self.assertEqual(result._asdict(), {'x': 3, 'pyconfreader': pyconfreader})

    def test_custom_predicate(self):
        def predicate(key, value):
            return not (key == 'x' or value == pyconfreader)
        result = pyconfreader.to_namedtuple({'x': 3, '_y': 'hi', 'pyconfreader': pyconfreader}, predicate=predicate)
        self.assertEqual(result._asdict(), {})


unittest.main()
