# coding: utf-8
from __future__ import unicode_literals

import os
import platform
import sys
import unittest

from contextlib import contextmanager
from ctypes import *
from os import path
from textwrap import dedent
from unittest.mock import patch, Mock

import tecplot as tp
from tecplot import session
from tecplot.constant import *
from tecplot.exception import *

from ..sample_data import sample_data_file

class TestDataset(unittest.TestCase):

    def setUp(self):
        self.filenames = {
            '10x10x10' : sample_data_file('10x10x10'),
            '2x2x3_overlap' : sample_data_file('2x2x3_overlap')}

    def tearDown(self):
        for fname in self.filenames.values():
            os.remove(fname)

    def test___init__(self):
        page = tp.layout.Page(1)
        frame = tp.layout.Frame(2,page)
        dataset = tp.data.Dataset(3,frame)
        self.assertEqual(dataset.uid,3)
        self.assertEqual(dataset.frame.uid,2)
        self.assertEqual(dataset.frame.page.uid,1)

    def test___repr__(self):
        page = tp.layout.Page(1)
        frame = tp.layout.Frame(2,page)
        dataset = tp.data.Dataset(3,frame)
        self.assertEqual(repr(dataset), 'Dataset(uid=3, frame=Frame(uid=2, page=Page(uid=1)))')

    def test___str__(self):
        """brief string representation"""
        fmt = 'Dataset:\n  Zones: [{}]\n  Variables: [{}]'
        #return fmt.format(','.join("'{}'".format(z.name) for z in self.zones()),
        #                  ','.join("'{}'".format(v.name) for v in self.variables()))
        pass

    def test___eq__(self):
        page = tp.layout.Page(1)
        frame = tp.layout.Frame(2,page)
        dataset3 = tp.data.Dataset(3,frame)
        dataset4 = tp.data.Dataset(4,frame)
        dataset3_copy = tp.data.Dataset(3,frame)
        self.assertEqual(dataset3, dataset3_copy)
        self.assertNotEqual(dataset3, dataset4)

    def test_title(self):
        if not hasattr(tp.tecutil._tecutil,'DataSetGetInfoByUniqueID'):
            return
        else:
            raise Exception('DataSetGetInfoByUniqueID found. This line and the lines above can now be removed.')
        tp.new_layout()
        tp.data.load_tecplot(self.filenames['10x10x10'])
        ds = tp.active_frame().dataset
        self.assertEqual(ds.title, 'Internally created data set')
        ds.title = 'Test Τεστ'
        self.assertEqual(ds.title, 'Test Τεστ')
        ds.title = ''
        self.assertEqual(ds.title, '')

        ds.frame.uid += 1 # trick this dataset to point to a non-existant frame
        with self.assertRaises(TecplotSystemError):
            ds.title
        with self.assertRaises(TecplotSystemError):
            ds.title = 'Test'

        with self.assertRaises(TecplotLogicError):
            ds.title = None

    def test_num_zones(self):
        #return _tecutil.DataSetGetNumZonesForFrame(self.frame.uid)
        pass

    def test_zone(self):
        """returns zone by number or the first matching a pattern
        if isinstance(i, string_types):
            return next(self.zones(i))
        else:
            return Zone(_tecutil.ZoneGetUniqueIDForFrame(self.frame.uid, i+1), self)
        """
        pass

    def test_zones(self):
        """generator of all zones in this dataset
        for i in range(self.num_zones()):
            zone = self.zone(i)
            if pattern is None or fnmatch(zone.name, pattern):
                yield zone
        """
        pass

    def test_num_variables(self):
        """number of variables in this dataset
        return _tecutil.DataSetGetNumVarsForFrame(self.frame.uid)
        """
        pass

    def test_variable(self):
        """returns variable by number or the first matching a pattern
        if isinstance(i, string_types):
            return next(self.variables(i))
        else:
            return Variable(_tecutil.VarGetUniqueIDForFrame(self.frame.uid, i+1), self)
        """
        pass

    def test_variables(self):
        """generator of all variables in this dataset
        for i in range(self.num_variables()):
            variable = self.variable(i)
            if pattern is None or fnmatch(variable.name, pattern):
                yield variable
        """
        pass

    def test_copy_zones(self):
        tp.new_layout()
        tp.data.load_tecplot(self.filenames['10x10x10'])
        ds = tp.active_frame().dataset
        z = ds.copy_zones(ds.zones())[0]
        self.assertEqual(ds.num_zones, 2)
        self.assertEqual(ds.zone(0).shape, z.shape)
        self.assertNotEqual(ds.zone(0).uid, z.uid)
        self.assertEqual(ds.zone(1).uid, z.uid)

    def test_delete_zones_and_variables(self):
        tp.new_layout()
        ds = tp.data.load_tecplot(self.filenames['2x2x3_overlap'])
        self.assertIn('P', [v.name for v in ds.variables()])
        self.assertIn('Rectangular zone 2', [z.name for z in ds.zones()])
        ds.delete_variables(ds.variables('P'))
        ds.delete_zones(ds.zones('*2'))
        self.assertNotIn('P', [v.name for v in ds.variables()])
        self.assertNotIn('Rectangular zone 2', [z.name for z in ds.zones()])

        tp.new_layout()
        ds = tp.data.load_tecplot(self.filenames['2x2x3_overlap'])
        self.assertIn('P', [v.name for v in ds.variables()])
        self.assertIn('Rectangular zone 1', [z.name for z in ds.zones()])
        ds.delete_variables(ds.variable('P').index)
        ds.delete_zones(ds.zone('Rectangular zone 1').index)
        self.assertNotIn('P', [v.name for v in ds.variables()])
        self.assertNotIn('Rectangular zone 1', [z.name for z in ds.zones()])

    def test_delete_all_zones(self):
        ds = tp.data.load_tecplot(self.filenames['2x2x3_overlap'], append=False)
        self.assertEqual(ds.num_zones, 2)

        with self.assertRaises(TecplotLogicError):
            ds.delete_zones(ds.zones())

    def test_delete_all_variables(self):
        tp.new_layout()
        ds = tp.data.load_tecplot(self.filenames['2x2x3_overlap'])
        self.assertEqual(ds.num_variables, 4)
        with self.assertRaises(TecplotLogicError):
            ds.delete_variables(ds.variables())


class TestDatasetExamples(unittest.TestCase):
    def test_doc_VariablesNamedTuple(self):
        tp.new_layout()
        exdir = tp.session.tecplot_examples_directory()
        datafile = path.join(exdir,'3D_Volume','jetflow.plt')
        dataset = tp.data.load_tecplot(datafile)
        result = tp.data.probe_at_position(0,0.1,0.3)
        data = dataset.VariablesNamedTuple(*result.data)
        msg = '(RHO, E) = ({:.2f}, {:.2f})'.format(data.RHO, data.E)
        self.assertEqual(msg, '(RHO, E) = (1.17, 252930.37)')

if __name__ == '__main__':
    from .. import main
    main()
