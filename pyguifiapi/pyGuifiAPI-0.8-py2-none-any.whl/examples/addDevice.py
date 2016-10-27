#!/usr/bin/env python
import sys
sys.path.append('..')

from guifiConfig import USERNAME, PASSWORD, NOTIFICATION
from api import GuifiAPI

g = GuifiAPI(USERNAME, PASSWORD, secure=True)
g.auth()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print('Create a new device')
        print('Usage: {} <nick>'.format(sys.argv[0]))
        sys.exit(1)

    # NanoStation2 and AirOSv30
    g.addDevice(33968,
                'radio',
                '12:12:12:12:12:12',
                nick=sys.argv[1],
                notification=NOTIFICATION,
                comment='comment1',
                status='Planned',
                graph_server=None,
                model_id=25,
                firmware='AirOSv30')
