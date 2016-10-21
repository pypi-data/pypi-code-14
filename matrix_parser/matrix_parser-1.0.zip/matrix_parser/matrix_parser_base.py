#!/usr/bin/python3
"""
parse text into a matrix
"""
__author__ = 'heliosantos99@gmail.com (Helio Santos)'

import tkinter

class MatrixParserBase(object):
    """docstring for MatrixParserBase"""
    def __init__(self):
        super(MatrixParserBase, self).__init__()

    def parse(self, raw, columnSeparator=',', lineSeparator='\n', numLinesToIgnore=0):
        rawRows = (x.strip() for x in raw.split(lineSeparator))
        matrix = []
        ignoredRows = []
        maxWidth = 0
        for n, rawRow in enumerate(rawRows):
            if not rawRow or n < numLinesToIgnore:
                ignoredRows.append((n, rawRow))
                continue
            row = [x.strip() for x in rawRow.split(columnSeparator)]
            rowLength = len(row)
            if rowLength > maxWidth:
                maxWidth = rowLength
            matrix.append(row) 

        self.maxHeight = len(matrix)
        self.maxWidth = maxWidth
        self._matrix = matrix
        self._ignoredRows = ignoredRows

    def parse_from_clipboard(self, columnSeparator=',', lineSeparator='\n', numLinesToIgnore=0):
        r = tkinter.Tk()
        text = r.clipboard_get()
        r.withdraw()
        r.update()
        r.destroy()
        self.parse(text, columnSeparator, lineSeparator, numLinesToIgnore)

    def __getitem__(self, idx):
        return self._matrix[idx]

    def get_row(self, rowIdx):
        return self._matrix[rowIdx]

    def get_column(self, columnIdx):
        if columnIdx >= self.maxWidth:
            raise Exception("Out of range")
        return [x[columnIdx] if columnIdx < len(x) else None for x in self._matrix]

    def get_cell(self, rowIdx, columnIdx):
        return self._matrix[rowIdx][columnIdx]

    def transform_cell(self, rowIdx, columnIdx, transformationLambda):
        self._matrix[rowIdx][columnIdx] = transformationLambda(self._matrix[rowIdx][columnIdx])

    def transform_row(self, rowIdx, transformationLambda):
        for columnIdx in range(len(self._matrix[rowIdx])):
            self.transform_cell(rowIdx, columnIdx, transformationLambda)

    def transform_column(self, columnIdx, transformationLambda):
        for rowIdx in range(len(self._matrix)):
            self.transform_cell(rowIdx, columnIdx, transformationLambda)

    def transform_matrix(self, transformationLambda):
        for rowIdx in range(len(self._matrix)):
            self.transform_row(rowIdx, transformationLambda)
