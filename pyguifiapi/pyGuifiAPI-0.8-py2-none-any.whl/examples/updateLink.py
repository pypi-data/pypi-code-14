#!/usr/bin/env python
import sys
sys.path.append('..')

from api import GuifiAPI, GuifiApiError
from guifiConfig import USERNAME, PASSWORD

g = GuifiAPI(USERNAME, PASSWORD, secure=True)
g.auth()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print('Update an existing link changing its status')
        print('Usage: {} <link_id> <status>'.format(sys.argv[0]))
        sys.exit(1)

    try:
        g.updateLink(sys.argv[1], status=sys.argv[2])
    except GuifiApiError as e:
        print(e.reason)
