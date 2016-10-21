#!/usr/bin/python3
"""
MatrixParserBase tests
"""
__author__ = 'heliosantos99@gmail.com (Helio Santos)'

import unittest

from .context import matrix_parser
from matrix_parser import MatrixParserBase

class MatrixParserBaseTest(unittest.TestCase):

    def test_parse(self):
        raw = '''
        00,01,02,03,04
        10,11,12,13,14,15
        20,21,22,23,24
        30,31,32,33,34,35
        40,41,42,43,44,45,46,47,48
        50,51,52,53,54,55
        60,61
        '''

        matrix = MatrixParserBase()
        matrix.parse(raw)

        for i, row in enumerate(matrix):
            for j, val in enumerate(row):
                self.assertEqual(matrix[i][j], '{}{}'.format(i, j))   


    def test_columns(self):
        raw = '''
        00,01,02,03,04
        10,11,12,13,14,15
        20,21,22,23,24
        30,31,32,33,34,35
        40,41,42,43,44,45,46,47,48
        50,51,52,53,54,55
        60,61
        '''

        matrix = MatrixParserBase()
        matrix.parse(raw)


        emptyCells = set([
            '05', '06', '07', '08', 
            '16', '17', '18',
            '25', '26', '27', '28',
            '36', '37', '38',
            '56', '57', '58',
            '62', '63', '64', '65', '66', '67', '68'])

        for i in range(matrix.maxWidth):
            column = matrix.get_column(i)
            for j, cell in enumerate(column):
                if '{}{}'.format(j, i) in emptyCells:
                    self.assertIsNone(cell)
                else:
                    self.assertEqual(cell, '{}{}'.format(j, i))   

    def test_transforms(self):
        raw = '''
        00,01,02,03,04
        10,11,12,13,14,15
        20,21,22,23,24
        30,31,32,33,34,35
        40,41,42,43,44,45,46,47,48
        50,51,52,53,54,55
        60,61
        '''

        matrix = MatrixParserBase()
        matrix.parse(raw)

        matrix.transform_matrix(lambda x: x.replace('0', ''))

        for i, row in enumerate(matrix):
            for j, val in enumerate(row):
                self.assertEqual(matrix[i][j], '{}{}'.format(i, j).replace('0', '')) 









