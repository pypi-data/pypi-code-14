#!/usr/bin/env python
import sys
sys.path.append('..')

from guifiConfig import USERNAME, PASSWORD, DEFAULT_ZONE
from api import GuifiAPI

g = GuifiAPI(USERNAME, PASSWORD, secure=True)
g.auth()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print('Create a new node')
        print('Usage: {} <title>'.format(sys.argv[0]))
        sys.exit(1)

    # Create node somewhere in Málaga
    g.addNode(sys.argv[1],
              DEFAULT_ZONE,
              36.69912736,
              -4.44647219)
