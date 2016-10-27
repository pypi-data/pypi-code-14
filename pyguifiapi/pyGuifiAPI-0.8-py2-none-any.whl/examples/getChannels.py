#!/usr/bin/env python
import sys
sys.path.append('..')

from api import GuifiAPI

#No authentication needed
g = GuifiAPI()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print('Usage: {} <protocol>'.format(sys.argv[0]))
        print('To get the list of available protocols, use getProtocols.py')
        sys.exit(1)

    channels = g.getChannels(sys.argv[1])

    print('Total channels: {}'.format(len(channels)))
    print('Title\t\t\tDescription')
    for channel in channels:
        print('{}\t\t\t{}'.format(channel['title'], channel['description']))
