import sys
import getopt
from landmark_ml.learning.PageManager import PageManager
import codecs
import os
import re

class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg

def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        try:
            opts, args = getopt.getopt(argv[1:], "h", ["help"])
        except getopt.error, msg:
            raise Usage(msg)
        
        pageManager = PageManager()
        page_file = args[0]

        with codecs.open(page_file, "r", "utf-8") as myfile:
            page_str = myfile.read().encode('utf-8')
                    
        pageManager.addPage(page_file, page_str)

        shortest_pair = pageManager.getPossibleLocations(page_file, args[1], False)
        print "shortest pair:", shortest_pair
                
    except Usage, err:
        print >>sys.stderr, err.msg
        print >>sys.stderr, "for help use --help"
        return 2

if __name__ == '__main__':
    sys.exit(main())