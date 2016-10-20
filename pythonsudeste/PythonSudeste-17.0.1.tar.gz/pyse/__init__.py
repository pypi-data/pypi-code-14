from datetime import datetime, timedelta, timezone


__version__ = '17.0.1'


_timezone = timezone(timedelta(hours=-3))


dates = (datetime(2017, 5, 5, tzinfo=_timezone),
         datetime(2017, 5, 6, tzinfo=_timezone))
website = 'http://pythonsudeste.org/'
contact = 'pythonsudeste@gmail.com'
