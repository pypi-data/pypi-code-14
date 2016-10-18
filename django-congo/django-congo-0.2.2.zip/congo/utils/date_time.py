# -*- coding: utf-8 -*-
from django.utils import timezone
import datetime

def years_ago(years, from_date = None):
    if from_date is None:
        from_date = timezone.now()
    try:
        return from_date.replace(year = from_date.year - years)
    except:
        return from_date.replace(month = 2, day = 28, year = from_date.year - years)

def get_default_start_date():
    return timezone.now()

def get_default_end_date(days_active):
    return timezone.now() + datetime.timedelta(days = days_active)

def str_to_hour(hour_str):
    return datetime.datetime.strptime(hour_str, '%H:%M').time()

def hour_to_str(hour):
    return datetime.time.strftime(hour, '%H:%M')

def date_to_str(date):
    return datetime.datetime.strftime(date, '%Y-%m-%d')

def datetime_to_str(date):
    return datetime.datetime.strftime(date, '%Y-%m-%d %H:%M')
