import sys
import getopt
from landmark_ml.learning.PageManager import PageManager
import codecs
import os

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
        page_file_dir = args[0]
        
        for subdir, dirs, files in os.walk(page_file_dir):
            for file_pointer in files:
                if file_pointer.startswith('.'):
                    continue
                
                with codecs.open(os.path.join(subdir, file_pointer), "r", "utf-8") as myfile:
                    page_str = myfile.read().encode('utf-8')
                    
                pageManager.addPage(file_pointer, page_str)
        
        pageManager.learnStripes()
        
        count = 0
        for stripe in pageManager.getStripes():
            print str(count) + ": " + str(stripe)
            count = count + 1
        
    except Usage, err:
        print >>sys.stderr, err.msg
        print >>sys.stderr, "for help use --help"
        return 2

if __name__ == '__main__':
    sys.exit(main())