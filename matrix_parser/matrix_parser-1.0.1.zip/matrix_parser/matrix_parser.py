#!/usr/bin/python3
"""
parse text into a matrix
"""
__author__ = 'heliosantos99@gmail.com (Helio Santos)'

#from matrix_parser import MatrixParserBase

from . import MatrixParserBase

class MatrixParser(object):
    """docstring for MatrixParser"""
    def __init__(self):
        super(MatrixParser, self).__init__()
        self.rowNames = {}
        self.colNames = {}
    
    def parse(self, raw, columnSeparator=',', lineSeparator='\n', numLinesToIgnore=0):
        matrix = MatrixParserBase()
        matrix.parse(raw, columnSeparator, lineSeparator, numLinesToIgnore)
        self._prepare(matrix)

    def parse_from_clipboard(self, columnSeparator=',', lineSeparator='\n', numLinesToIgnore=0):
        matrix = MatrixParserBase()
        matrix.parse_from_clipboard(columnSeparator, lineSeparator, numLinesToIgnore)
        self._prepare(matrix)

    def _prepare(self, matrix):
        rows = MatrixSegment(self.rowNames)
        for i in range(matrix.maxHeight):
            rows.append(MatrixSegment(self.colNames))

        cols = MatrixSegment(self.colNames)
        for i in range(matrix.maxWidth):
            cols.append(MatrixSegment(self.rowNames))

        for i in range(matrix.maxHeight):
            for j in range(matrix.maxWidth):
                cell = MatrixCell(matrix[i][j] if j < len(matrix[i]) else None)
                if cell.val:
                    rows[i].append(cell)
                cols[j].append(cell)

        self.rows = rows
        self.cols = cols

    def __getitem__(self, idx):
        return self.rows[idx]

    def set_row_name(self, idx, name):
        self.rowNames[name] = idx

    def set_col_name(self, idx, name):
        self.colNames[name] = idx

    def transform(self, transformationLambda):
        for segment in self:
            segment.transform(transformationLambda)

    def to_list(self):
        return self.rows.to_list()

    def to_set(self):
        return self.rows.to_set()


class MatrixCell(object):
    """docstring for MatrixCell"""
    def __init__(self, val):
        super(MatrixCell, self).__init__()
        self.original = val
        self.val = val
    
    def transform(self, transformationLambda):
        self.val = transformationLambda(self.val)

    def to_list(self):
        return self.val

    def to_set(self):
        if self.val is None:
            return set()
        return set([self.val])

class MatrixSegment(list):
    """docstring for MatrixSegment"""
    def __init__(self, names=None):
        self.base = super(MatrixSegment, self)
        self.base.__init__()
        self.names = {} if names is None else names

    def __getitem__(self, idx):
        return self.base.__getitem__(self.names.get(idx, idx))

    def transform(self, transformationLambda):
        for segment in self:
            segment.transform(transformationLambda)

    def to_list(self):
        return [elem.to_list() for elem in self]

    def to_set(self):
        combinedSet = set()
        for elem in self:
            combinedSet.update(elem.to_set())
        return combinedSet
