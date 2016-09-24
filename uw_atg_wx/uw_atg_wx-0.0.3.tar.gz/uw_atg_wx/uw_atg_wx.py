""" provides latest_uw_data(), a generator which yields dictionary records of current
weather obs from UW ATG """

from datetime import datetime, timedelta
import json
import os
from urllib import request


def get_obs_from_uw_atg():

    url = "http://www.atmos.washington.edu/cgi-bin/latest_uw.cgi?data"

    with request.urlopen(url, timeout=2) as f:

        # lop off header
        for header in f :
            if 'knot' in str(header):
                break
        f.readline()

        now = datetime.utcnow()

        for record in f:
            fields = record.decode().strip().split()

            if len(fields) != 9:
                continue

            # parse time and convert to a datetime
            t = datetime.strptime(fields[0], '%H:%M:%S')
            if t.hour > now.hour:
                # this record is from yesterday
                delta = timedelta(days=1)
            else:
                delta = timedelta()

            dt = now.replace(hour=t.hour, minute=t.minute, second=t.second, microsecond=0)
            observation_time = dt - delta

            data = {
                'time': observation_time.isoformat(),
                'rh': int(fields[1]),
                'temperature': int(fields[2]),
                'direction': int(fields[3]),
                'speed': int(fields[4]),
                'gust': int(fields[5]),
                'rain': float(fields[6]),
                'radiation': float(fields[7]),
                'pressure': float(fields[8])
            }
            yield data


if __name__ == "__main__":
    for obs in get_obs_from_uw_atg():
        print(obs)
