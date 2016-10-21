#!/usr/bin/python3
"""
MatrixParser tests
"""
__author__ = 'heliosantos99@gmail.com (Helio Santos)'

import unittest

from .context import matrix_parser
from matrix_parser import MatrixParser

class MatrixParserTest(unittest.TestCase):

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

        matrix = MatrixParser()
        matrix.parse(raw)

        for i, row in enumerate(matrix):
            for j, val in enumerate(row):
                self.assertEqual(matrix[i][j].val, '{}{}'.format(i, j))   


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

        matrix = MatrixParser()
        matrix.parse(raw)


        emptyCells = set([
            '05', '06', '07', '08', 
            '16', '17', '18',
            '25', '26', '27', '28',
            '36', '37', '38',
            '56', '57', '58',
            '62', '63', '64', '65', '66', '67', '68'])

        for i, colm in enumerate(matrix.cols):
            for j, cell in enumerate(colm):
                if '{}{}'.format(j, i) in emptyCells:
                    self.assertIsNone(cell.val)
                else:
                    self.assertEqual(cell.val, '{}{}'.format(j, i))   

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

        matrix = MatrixParser()
        matrix.parse(raw)

        matrix.transform(lambda x: x.replace('0', ''))

        for i, row in enumerate(matrix):
            for j, val in enumerate(row):
                self.assertEqual(matrix[i][j].val, '{}{}'.format(i, j).replace('0', '')) 


    def test_to_list(self):
        raw = '''
        00,01,02,03,04
        10,11,12,13,14,15
        20,21,22,23,24
        30,31,32,33,34,35
        40,41,42,43,44,45,46,47,48
        50,51,52,53,54,55
        60,61
        '''

        matrix = MatrixParser()
        matrix.parse(raw)

        emptyCells = set([
            '05', '06', '07', '08', 
            '16', '17', '18',
            '25', '26', '27', '28',
            '36', '37', '38',
            '56', '57', '58',
            '62', '63', '64', '65', '66', '67', '68'])

        for i, colm in enumerate(matrix.cols.to_list()):
            for j, cell in enumerate(colm):
                if '{}{}'.format(j, i) in emptyCells:
                    self.assertIsNone(cell)
                else:
                    self.assertEqual(cell, '{}{}'.format(j, i))  


    def test_to_set(self):
        raw = '''
        00,00,00,00,00
        00,00,00,11,11,11,11,11
        00,00,22,23,24
        '''

        matrix = MatrixParser()
        matrix.parse(raw)

        combinedSet = matrix.to_set()
        self.assertEqual(len(combinedSet), 5)
        self.assertTrue('00' in combinedSet)
        self.assertTrue('11' in combinedSet)
        self.assertTrue('22' in combinedSet)
        self.assertTrue('23' in combinedSet)
        self.assertTrue('24' in combinedSet)

