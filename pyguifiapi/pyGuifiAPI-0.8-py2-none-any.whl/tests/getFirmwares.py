#!/usr/bin/env python
import sys
sys.path.append('..')

from api import *
from guifiConfig import *

if __name__ == "__main__":
    #No authentication needed
    g = GuifiAPI()
    firmwares = g.getFirmwares(model_id=sys.argv[1])

    print('Total firmwares: {}'.format(len(firmwares)))
    print('ID\tTitle\t\t\tDescription')
    for firmware in firmwares:
        print(u'{}\t{}\t\t\t{}'.format(firmware["id"], firmware['title'], firmware['description']))
