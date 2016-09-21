import unittest
import random

from read import *
from write import *

class TestWriteXLS(unittest.TestCase):
    def setUp(self):
        N = 200

    def test_matrix_01(self):
        N = 200
        matrix = [
            [ x for x in range(u*N,(u+1)*N) ] for u in range(N)
        ]
        matrix.insert(0,['COL%3d' % n for n in range(N)])
        write_xls_from_matrix('TEST.xls','SHEET',matrix, styles = None)

    def test_matrix_02(self):
        N = 200
        matrix = [
            [ x if random.random()>.5 else "STR%d" % x for x in range(u*N,(u+1)*N) ]
            for u in range(N)
        ]
        matrix.insert(0,['COL%03d' % n for n in range(N)])
        write_xls_from_matrix('TEST.xls','SHEET',matrix, styles = None)
        

class TestReadXLS(unittest.TestCase):

    def setUp(self):
        N = 200
        matrix = [
            [ x if random.random()>.5 else "STR%d" % x for x in range(u*N,(u+1)*N) ]
            for u in range(N)
        ]
        matrix.insert(0,['COL%03d' % n for n in range(N)])        
        write_xls_from_matrix('TEST.xls','SHEET',matrix, styles = None)
        import xlwt
        styles =   map(xlwt.easyxf, (
            'font: bold 0, color black; ',
            'font: bold 0, color red; ',
            ))
        matrix = [
            [ (0, x if random.random()>.5 else "STR%d" % x, 0 if random.random()>.5 else 1) for x in range(u*N,(u+1)*N) ]
            for u in range(N)
        ]
        matrix.insert(0,[ ( 0, 'COL%03d' % n,0) for n in range(N)])
        write_xls_from_matrix('TEST-S.xls','SHEET',matrix, styles = styles)

    def tearDown(self):
        import os
        os.unlink('TEST-S.xls')
        os.unlink('TEST.xls')

    def test_matrix_noxf(self):
        matrix = read_xls_into_matrix('TEST.xls',0,False)
        self.assertEqual( matrix[0][0], u'COL000')

    def test_matrix_xf(self):
        matrix = read_xls_into_matrix('TEST-S.xls',0,True)
        self.assertEqual(matrix[0][0][1].value, u'COL000')
        self.assertEqual(matrix[0][0][1].xf_index, 17)

    def test_00(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_00(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

if __name__ == '__main__':
    unittest.main()
