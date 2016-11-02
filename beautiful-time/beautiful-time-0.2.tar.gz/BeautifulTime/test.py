# -*- coding: utf-8 -*-
# Created by restran on 2016/11/2
from __future__ import unicode_literals, absolute_import

import time
import unittest
from datetime import datetime

import BeautifulTime


class BeautifulTimeTest(unittest.TestCase):
    def setUp(self):
        self.date_str = '2016-10-30 12:30:30'
        self.dt = datetime(year=2016, month=10, day=30, hour=12, minute=30, second=30)
        self.t = self.dt.timetuple()
        self.ts = int(time.mktime(self.t))

    def test_str2datetime(self):
        dt = BeautifulTime.str2datetime(self.date_str)
        self.assertEqual(dt, self.dt)

    def test_str2time(self):
        t = BeautifulTime.str2time(self.date_str)
        self.assertEqual(t[0:6], self.t[0:6])

    def test_str2timestamp(self):
        ts = BeautifulTime.str2timestamp(self.date_str)
        self.assertEqual(ts, self.ts)

    def test_datetime2str(self):
        s = BeautifulTime.datetime2str(self.dt)
        self.assertEqual(s, self.date_str)

    def test_datetime2time(self):
        t = BeautifulTime.datetime2time(self.dt)
        self.assertEqual(t[0:6], self.t[0:6])

    def test_datetime2timestamp(self):
        ts = BeautifulTime.datetime2timestamp(self.dt)
        self.assertEqual(ts, self.ts)

    def test_time2str(self):
        s = BeautifulTime.time2str(self.t)
        self.assertEqual(s, self.date_str)

    def test_time2datetime(self):
        dt = BeautifulTime.time2datetime(self.t)
        self.assertEqual(dt, self.dt)

    def test_time2timestamp(self):
        ts = BeautifulTime.time2timestamp(self.t)
        self.assertEqual(ts, self.ts)

    def test_timestamp2datetime(self):
        dt = BeautifulTime.timestamp2datetime(self.ts)
        self.assertEqual(dt, self.dt)

    def test_timestamp2time(self):
        t = BeautifulTime.timestamp2time(self.ts)
        self.assertEqual(t[0:6], self.t[0:6])

    def test_timestamp2str(self):
        s = BeautifulTime.timestamp2str(self.ts)
        self.assertEqual(s, self.date_str)


if __name__ == '__main__':
    unittest.main()
