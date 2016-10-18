# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import unicode_literals

import arrow
import argparse

__doc__ = """
Prints a monthly journal template.

$ journal_dates 2015 9
Deník 2015/08

1.8.2015 (So)
2.8.2015 (Ne)
[...]
30.8.2015 (Ne)
31.8.2015 (Po)

$ journal_dates 2015 9 --locale en_US --format 'YYYY-MM-DD'
Journal 2015/09

2015-09-01
2015-09-02
[...]
2015-09-29
2015-09-30
"""


def date_range(since, till):
    return [s for (s,e) in arrow.Arrow.span_range('day', since, till)]

def date_range_for_month(year, month):
    since = arrow.get('%s-%s' % (year, month))
    till = since.replace(months=1, days=-1)
    return date_range(since, till)

def print_journal_template(year, month, format, locale):
    title = 'Deník' if locale == 'cs_CZ' else 'Journal'
    if year is None or month is None:
        year, month = arrow.utcnow().format('YYYY-MM').split('-')
    year = year
    month = '%02d' % int(month)
    print('%s %s/%s\n' % (title, year, month))
    for date in date_range_for_month(year, month):
        print(date.format(format, locale=locale))

def parse_args():
    parser = argparse.ArgumentParser(
        description='Prints a monthly journal template.')
    parser.add_argument('year', metavar='YEAR', nargs='?')
    parser.add_argument('month', metavar='MONTH', nargs='?')
    parser.add_argument('--locale', default='cs_CZ')
    parser.add_argument('--format', default='D.M.YYYY (ddd)')
    args = parser.parse_args()
    return args

def main():
    args = parse_args()
    print_journal_template(args.year, args.month, args.format, args.locale)

if __name__ == '__main__':
    main()
