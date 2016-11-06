import pytz
from tzlocal import get_localzone

def same_date(utc_dt1, utc_dt2):
    #print(utc_dt1, utc_dt2)
    dt1 = pytz.utc.localize(utc_dt1)
    dt2 = pytz.utc.localize(utc_dt2)

    local_tz = get_localzone()
    local_dt1 = dt1.astimezone(local_tz)
    local_dt2 = dt2.astimezone(local_tz)

    #print(local_dt1.date(), local_dt2.date())
    return local_dt1.date() == local_dt2.date()

