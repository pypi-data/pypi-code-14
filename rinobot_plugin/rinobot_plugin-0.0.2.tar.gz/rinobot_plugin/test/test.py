
import rinobot_plugin as bot
import numpy.testing as npt
import unittest
import shutil
import os
import sys
from mock import patch

_dir = os.path.join(os.path.dirname(__file__), 'text-fixtures')


class Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        os.mkdir(_dir)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(_dir)

    def getFixturePath(self, subDir=''):
        return os.path.join(_dir, self.id(), subDir)

    def setUp(self):
        os.mkdir(self.getFixturePath())

    def test_loadfile(self):
        with open(self.getFixturePath('test.txt'), 'w') as outfile:
            outfile.write('# comment\n# comment\n1\n2\n3\n')
        data = bot.loadfile(self.getFixturePath('test.txt'))
        npt.assert_array_equal(data, [1,2,3])

    def test_parser_default(self):
        filepath = self.getFixturePath('test.txt')
        prefix='.abcd'

        with patch.object(sys, 'argv', ['script.py', filepath, '--prefix='+prefix]):
            args = bot.get_args()
            assert args.filepath == filepath
            assert args.prefix == prefix

    def test_parser_with_args(self):
        filepath = self.getFixturePath('test.txt')
        prefix='.abcd'
        xmin=3
        bot.add_argument('--xmin', type=int, required=True)

        with patch.object(sys, 'argv', ['script.py', filepath, '--prefix='+prefix, '--xmin='+str(xmin)]):
            args = bot.get_args()
            assert args.filepath == filepath
            assert args.prefix == prefix
            assert args.xmin == xmin

    def test_output_filepath(self):
        filepath = self.getFixturePath('test.txt')
        prefix='.abcd'

        with patch.object(sys, 'argv', ['script.py', filepath, '--prefix='+prefix]):
            args = bot.get_args()
            assert args.filepath == filepath
            assert args.prefix == prefix
            bot.output_filepath('output.txt')

    def test_plugin(self):
        bot.reset_parser()

        filepath = self.getFixturePath('test.txt')
        _shift=3
        prefix = '.123'
        with patch.object(sys, 'argv', ['script.py', filepath, '--prefix='+prefix, '--shift='+str(_shift)]):
            infile = bot.filepath()
            shift = bot.get_arg('shift', type=float, required=True)
            outname = bot.no_extension() + 'shifted-%s.txt' % shift
            outfile = bot.output_filepath(outname)

            assert infile == filepath
            assert shift == _shift
            assert bot.no_extension() == 'test'
            assert outfile == os.path.join(
                self.getFixturePath(),
                prefix + 'testshifted-%s.txt' % float(_shift)
            )
