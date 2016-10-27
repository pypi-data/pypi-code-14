#!/usr/bin/env python
import sys
sys.path.append('..')

from guifiConfig import USERNAME, PASSWORD
from api import GuifiAPI, GuifiApiError

g = GuifiAPI(USERNAME, PASSWORD, secure=True)
g.auth()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print('Remove an existing link')
        print('Usage: {} <link_id>'.format(sys.argv[0]))
        sys.exit(1)

    try:
        g.removeLink(sys.argv[1])
    except GuifiApiError as e:
        print(e.reason)
