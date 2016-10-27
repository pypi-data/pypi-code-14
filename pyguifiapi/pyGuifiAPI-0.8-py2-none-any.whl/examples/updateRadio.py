#!/usr/bin/env python
import sys
sys.path.append('..')

from guifiConfig import USERNAME, PASSWORD
from api import GuifiAPI, GuifiApiError

g = GuifiAPI(USERNAME, PASSWORD, secure=True)
g.auth()

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print('Update an existing radio changing its gain')
        print('Usage: {} <device_id> <radiodev> <gain>'.format(sys.argv[0]))
        sys.exit(1)

    try:
        g.updateRadio(sys.argv[1], sys.argv[2], gain=sys.argv[3])
    except GuifiApiError as e:
        print(e.reason)
