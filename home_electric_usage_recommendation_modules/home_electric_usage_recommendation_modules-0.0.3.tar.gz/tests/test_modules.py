# coding: utf-8

import unittest
import csv
from datetime import datetime as dt

from home_electric_usage_recommendation_modules \
    import (SettingTemp, ReduceUsage, ChangeUsage)

CSVFILE_PATH = "tests/test.csv"


class RowData:
    '''
    想定しているデータカラム
    --------------------------------------------------------------------------------------------
    timestamp,on_off,operating,set_temperature,wind,temperature,pressure,humidity,IP_Address
    --------------------------------------------------------------------------------------------
    ...
    '''
    def __init__(self, timestamp, on_off=None, operating=None,
                 set_temperature=None, wind=None,
                 temperature=None, pressure=None, humidity=None,
                 IP_Address=None):
        self.timestamp = dt.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
        self.on_off = str(on_off) if on_off else on_off
        self.operating = str(operating) if operating else operating
        self.set_temperature = int(set_temperature)\
            if set_temperature else set_temperature
        self.wind = str(wind) if wind else wind
        self.temperature = float(temperature) if temperature else wind
        self.pressure = float(pressure) if pressure else pressure
        self.humidity = float(humidity) if humidity else humidity
        self.IP_Address = str(IP_Address) if IP_Address else IP_Address


class SettingTempModuleTestCase(unittest.TestCase):
    def setUp(self):
        '''
        # prepare TestCase
        input_rowsの中にRowData型を入れていく
        '''
        with open(CSVFILE_PATH) as csvfile:
            reader = csv.DictReader(csvfile)
            self.input_rows = []
            for row in reader:
                self.input_rows.append(
                    RowData(timestamp=row['timestamp'],
                            set_temperature=row['set_temperature']))

    def test_find_frequest_set_temperature(self):
        '''
        find_frequent_set_temperature()メソッドをテスト
        '''
        st = SettingTemp(self.input_rows)
        frequent_set_temp = st.find_frequent_set_temperature()
        self.assertEqual(frequent_set_temp, 25)

    def test_show_recommend_set_temperature(self):
        '''
        _show_recommend_set_temperature()メソッドをテスト
        '''
        st = SettingTemp(self.input_rows)
        recommend_set_temp = st.show_recommend_set_temperature()
        self.assertEqual(recommend_set_temp, 27)


class ReduceUsageModuleTestCase(unittest.TestCase):
    def setUp(self):
        # prepare TestCase
        with open(CSVFILE_PATH) as csvfile:
            reader = csv.DictReader(csvfile)
            self.input_rows = []
            for row in reader:
                self.input_rows.append(
                    RowData(timestamp=row['timestamp'],
                            on_off=row['on_off']))

    def test_make_horizontal_axis_weekly_values(self):
        '''
        _make_horizontal_axis_weekly_values()メソッドをテスト
        '''
        ru = ReduceUsage(self.input_rows)
        ret_list = ru._make_horizontal_axis_weekly_values()
        self.assertEqual(ret_list, ['2016-08-28', '2016-08-29', '2016-08-30',
                                    '2016-08-31', '2016-09-01', '2016-09-02',
                                    '2016-09-03'])

    def test_make_virtical_axis_weekly_values(self):
        '''
        _make_virtical_axis_weekly_values()メソッドをテスト
        '''
        ru = ReduceUsage(self.input_rows)
        ret_list = ru._make_virtical_axis_weekly_values()
        self.assertEqual(ret_list, [7.0, 16.5, 11.5, 8.0, 17.4, 17.7, 25.4])

    def test_find_the_rank_weekday(self):
        '''
        find_the_rank_weekday()メソッドをテスト
        '''
        ru = ReduceUsage(self.input_rows)
        # 1st Test
        weekday = ru.find_the_rank_weekday()
        self.assertEqual(weekday, '土')
        # 2nd Test
        weekday = ru.find_the_rank_weekday(rank=4, lang='en')
        self.assertEqual(weekday, 'Mon')


class ChangeUsageModuleTestCase(unittest.TestCase):
    def setUp(self):
        # prepare TestCase
        with open(CSVFILE_PATH) as csvfile:
            reader = csv.DictReader(csvfile)
            self.input_rows = []
            for row in reader:
                self.input_rows.append(
                    RowData(timestamp=row['timestamp'],
                            on_off=row['on_off']))

    def test_make_hourly_usage_frequent_list(self):
        '''
        find_the_rank_weekday()メソッドをテスト
        '''
        cu = ChangeUsage(self.input_rows)
        ret_list = cu._make_hourly_usage_frequent_list()
        self.assertEqual(
            ret_list, [142, 28, 0, 0, 0, 0, 14, 114, 114,
                       42, 28, 28, 57, 42, 42, 57, 71, 157,
                       142, 142, 142, 142, 142, 142])

    def test_find_a_certain_hour_value(self):
        '''
        find_the_rank_weekday()メソッドをテスト
        '''
        cu = ChangeUsage(self.input_rows)
        # 1st Test
        val = cu.find_a_certain_hour_value()
        self.assertEqual(val, 42)
        # 2nd Test
        val = cu.find_a_certain_hour_value(index=1)
        self.assertEqual(val, 28)
