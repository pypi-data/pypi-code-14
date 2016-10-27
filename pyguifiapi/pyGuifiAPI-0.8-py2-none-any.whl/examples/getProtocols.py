#!/usr/bin/env python
import sys
sys.path.append('..')

from api import GuifiAPI

#No authentication needed
g = GuifiAPI()

if __name__ == "__main__":
    protocols = g.getProtocols()

    print('Total protocols: {}'.format(len(protocols)))
    print('Title\tDescription')
    for protocol in protocols:
        print('{}\t{}'.format(protocol['title'], protocol['description']))
