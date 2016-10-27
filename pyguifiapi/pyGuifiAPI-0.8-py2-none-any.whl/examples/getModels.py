#!/usr/bin/env python
import sys
sys.path.append('..')

from api import GuifiAPI

#No authentication needed
g = GuifiAPI()

if __name__ == "__main__":

    if len(sys.argv) != 2:
        print('Usage: {} [model]\n'.format(sys.argv[0]))
        model = None
    else:
        model = sys.argv[1]

    models = g.getModels(model)

    print('Total models: {}'.format(len(models)))
    print('ID\tModel\t\t\t\t\tSupported\tType\tModel ID\tFirmware ID')
    for m in models:
        print('{}\t{}\t\t\t\t\t{}\t{}\t{}\t{}'.format(m['mid'], m['model'], m['supported'], m['type'], m['mid'], m['fid']))
