# encoding: utf-8

import datetime

__author__ = u'Hywel Thomas'
__copyright__ = u'Copyright (C) 2016 Hywel Thomas'


# get the daylight savings/summer/GMT/UTC offset
def calculate_time_offset():
    TEN_MINUTES = datetime.timedelta(minutes = 10)
    utc_time = datetime.datetime.utcnow()
    local_time = datetime.datetime.now()
    if local_time.minute == 0: # could be on boundary so that utc is hh:59:59.xx and local is hh+1:00.00.xx
        utc_time -= TEN_MINUTES
        local_time -= TEN_MINUTES
    utc_time = datetime.datetime.utcnow().replace(minute = 0, second = 0, microsecond = 0)
    local_time = datetime.datetime.now().replace(minute = 0, second = 0, microsecond = 0)
    return local_time - utc_time


try:
    TIME_OFFSET
except NameError:
    TIME_OFFSET = calculate_time_offset()
