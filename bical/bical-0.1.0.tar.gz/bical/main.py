#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime


class Calendar:
    def __init__(self):
        self.data = []
        self.today = datetime.datetime.today()

    @staticmethod
    def quarter(date):
        return ((date.month-1) // 3) + 1

    @staticmethod
    def add(year, unit, limit, quarter):
        """ Compose a string of the next time period

        :param int year: date year
        :param int unit: number of the week/month/quarter
        :param int limit: maximum unit possible
        :param bool quarter: True if quarter format is required
        """
        string = '{}-Q{}' if quarter else '{}-{:02}'
        if unit == limit:
            return string.format(year+1, 1)
        else:
            return string.format(year, unit+1)

    def convert(self, date, period):
        """ Converts a datetime object into a formatted string

        :param datetime date: date to be converted
        :param str period: string format
        """
        if period == 'week':
            return "{}-{:02}".format(*date.isocalendar())
        elif period == 'month':
            return "{0.year}-{0.month:02}".format(date)
        elif period == 'quarter':
            return "{}-Q{}".format(date.year, self.quarter(date))
        elif period == 'year':
            return "{}".format(date.year)

    def increment(self, date, period):
        """ Increment the time period by one unit

        :param str date: date formatted string
        :param str period: 'week', 'month', 'quarter' or 'year'
        """
        if period == 'week':
            year, week = [int(i) for i in date.split('-')]
            total_weeks = datetime.datetime(year, 12, 31).isocalendar()[1]
            return self.add(year, week, total_weeks, False)
        elif period == 'month':
            year, month = [int(i) for i in date.split('-')]
            return self.add(year, month, 12, False)
        elif period == 'quarter':
            year, quarter = [int(i) for i in date.split('-Q')]
            return self.add(year, quarter, 4, True)
        elif period == 'year':
            return str(int(date) + 1)

    def timeline(self, since, until, period):
        """ Create a list of date formatted strings for a given timeframe
        :param since: datetime or date formatted string
        :param until: datetime or date formatted string
        :param str period: 'week', 'month', 'quarter' or 'year'
        """
        since = self.convert(since, period) if isinstance(since, datetime.datetime) else since
        until = self.convert(until, period) if isinstance(until, datetime.datetime) else until
        assert since <= until, "Inconsistent dates"
        timeline = [since]
        while since < until:
            since = self.increment(since, period)
            timeline.append(since)
        return timeline

    def filter(self, date, **kwargs):
        """ Filter results according to the matching kwargs keys

        :param str date: name of the key with the datetime value
        :param kwargs: filters
        """
        matches = []
        for item in self.data:
            if item[date]:
                include = True
                for attribute, value in kwargs.items():
                    if item[attribute] != value:  # TODO: add operator modes
                        include = False
                        break
                if include:
                    matches.append(item)
        return matches

    def query(self, date, until=None, period='week', **kwargs):
        """ Arrange the data into a dictionary

        :param str date: name of the key with the datetime value
        :param datetime until: ...
        :param str period: 'week', 'month', 'quarter' or 'year'
        :param kwargs: filters (e.g. priority='Critical')
        """
        first = min([item[date] for item in self.data])
        timeline = self.timeline(first, self.today, period)
        results = dict(zip(timeline, [[] for _ in range(len(timeline))]))

        for item in self.filter(date, **kwargs):
            if until:
                date1 = self.convert(item[date], period)
                if item[until]:
                    date2 = self.convert(item[until], period)
                else:
                    date2 = self.increment(self.convert(self.today, period), period)
                while date1 < date2:
                    results[date1].append(item)
                    date1 = self.increment(date1, period)
            else:
                key = self.convert(item[date], period)
                results[key].append(item)

        return results

