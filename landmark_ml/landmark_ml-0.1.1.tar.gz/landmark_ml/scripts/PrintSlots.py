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
        
#         pageManager = PageManager()
#         page_file_dir = args[0]
#         
#         for subdir, dirs, files in os.walk(page_file_dir):
#             for file_pointer in files:
#                 if file_pointer.startswith('.'):
#                     continue
#                 
#                 with codecs.open(os.path.join(subdir, file_pointer), "r", "utf-8") as myfile:
#                     page_str = myfile.read().encode('utf-8')
#                     
#                 pageManager.addPage(page_str)
#         
#         pageManager.learnStripes()
#         page_markups = []
#         pageManager.cleanStripes(page_markups)
#         
#         for page_id in pageManager.getPageIds():
#             print '====PAGE ' + str(page_id) + "===="
#             count = 0
#             for slot in pageManager.getSlots(page_id):
#                 print "SLOT " + str(count) + ":" + slot['extract']
#                 count = count + 1
#             print ''

#TEST of REGEX
        test_string = "testing brad pitt is nice and so is will smith. here is the list now <li>brad pitt</li><li>will smith</li><li>kane see</li><li>steve minton</li>"
        first = 'brad pitt'
        second = 'will smith'
        last = 'steve minton'
        markup = first+'.*?'+second+'.*?'+last
        indexes = [m.start() for m in re.finditer(first, test_string)]
        for index in indexes:
            index_sets = [[m.start()+index, m.end()+index] for m in re.finditer(markup, test_string[index:])]
            for index_set in index_sets:
                print test_string[index_set[0]:index_set[1]]
        
    except Usage, err:
        print >>sys.stderr, err.msg
        print >>sys.stderr, "for help use --help"
        return 2

if __name__ == '__main__':
    sys.exit(main())