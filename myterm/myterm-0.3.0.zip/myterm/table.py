#!/usr/bin/env python
# -*- coding: utf-8 -*-

import operator
import csv
from datetime import datetime

from tabulate import tabulate

class Table():

    def __init__(self, lst=[]):
        self._headers = []
        self._table = []
        for dct in lst:
            self.append(dct)
    
    @property
    def headers(self):
        return self._headers

    def add_columns(self, *cols):
        for col in cols:
            if len(self._table):
                tmp = list(zip(*self._table))
                tmp.append([''] * len(self._headers))
                self._table=list(zip(*tmp))
            self._headers.append(col)

    def remove_columns(self, *cols):
        cols = [col for col in cols if col in self._headers]
        if len(self._table):
            cols = [col for col in cols if col in self._headers]
            try:
                tmp = list(zip(*self._table))
                for colidx in reversed(sorted([ self._headers.index(col) for col in cols])):
                    tmp.pop(colidx)
                self._table = list(zip(*tmp))
            except:
                raise ValueError("column not found")
        else:
            for colidx in reversed(sorted([ self._headers.index(col) for col in cols])):
                self._headers.pop(colidx)

    def orderby(self, *cols):
        for col in reversed(cols):
            try:
                self._table = sorted(self._table, key=operator.itemgetter(self._headers.index(col)))
            except:
                pass

    def append(self, *rows):
        for row in rows:
            if type(row) == type(list()):
                if len(self._headers) < len(row):
                    raise ValueError("too many columns")
                row = {col:val for(col,val) in zip(self._headers,row)}
            if type(row) != type(dict()):
                raise ValueError("is not dict")
            for key in row.keys():
                if key not in self._headers:
                    self.add_columns(key)
            elt = []        
            for key in self._headers:
                elt.append(row.get(key,''))
            self._table.append(tuple(elt))   

    def remove(self, obj):
        self._table.remove(obj)

    def remove_line(self, idx):
        self._table.pop(idx)

    def rename_columns(self, old, new):
        try:
            col= self._headers.index(old)
        except:
            raise ValueError("column not found")
        self._headers[col] = new

    def set(self, row, col=None, value=None):
        if not col:
            self.append(value)
            self._table.pop(row)
            self._table.insert(row, self._table.pop())
        else:
            try:
                col= self._headers.index(old)
            except:
                raise ValueError("column not found")
            self._headers[col] = new
            rownew = self._table[row]
            rownew = rownew[:col] + (value,) + rownew[col+1:]
            self._table[row] = rownew

    def get(self, row, col=None):
        if not col:
            return {colname:val for(colname,val) in zip(self._headers, self._table[row])}
        return {colname:val for(colname,val) in zip(self._headers, self._table[row])}[col]

    def __getitem__(self, key):
        return self.get(key)

    def __setitem__(self, key, value):
        return self.set(key, value=value)

    def __len__(self):
        return len(self._table)

    def __iter__(self):
        return self._table.__iter__()

    def __delitem__(self, ii):
        del self._table[ii]

    def pprint(self, noheader=False, fmt='plain'):
        if noheader:
            headers = []
        else:
            headers = self._headers
        print(tabulate(self._table, headers, tablefmt=fmt))

    def csv(self, csvfile, noheader=False, **kw):
        writer = csv.DictWriter(csvfile, **kw)
        if not noheader:
            writer.writeheader()
        for line in self._table:
            writer.writerow({col:val for(col,val) in zip(self._headers,line)})

    def apply_formula(self, col, formula):
        try:
            col= self._headers.index(col)
        except:
            raise ValueError("column not found")
        for idxrow in list(range(0,len(self._table))):
            row = self._table[idxrow]
            value = row[col]
            current = { idx:val for(idx,val) in zip(self._headers, row)}
            if callable(formula):
                new_val = formula(*current)
            else:
                #try:
                new_val = eval(formula)
                #except:
                #    new_val = formula
            row = row[:col] + (new_val,) + row[col+1:]
            self._table[idxrow] = row

    def filter(self, formula):
         for idxrow in reversed(list(range(0,len(self._table)))):
            row = self._table[idxrow]
            current = { idx:val for(idx,val) in zip(self._headers, row)}
            if callable(formula):
                test = formula(*current)
            else:
                try:
                    test = eval(formula)
                except:
                    test = False
            if not test:
                self._table.pop(idxrow)
