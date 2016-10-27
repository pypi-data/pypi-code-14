#!/usr/bin/env python
import sys
sys.path.append('..')

from guifiConfig import USERNAME, PASSWORD
from api import GuifiAPI, GuifiApiError

g = GuifiAPI(USERNAME, PASSWORD, secure=True)
g.auth()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print('Remove an existing radio')
        print('Usage: {} <device_id> <radiodev_counter>'.format(sys.argv[0]))
        sys.exit(1)

    try:
        g.removeRadio(sys.argv[1], sys.argv[2])
    except GuifiApiError as e:
        print(e.reason)
