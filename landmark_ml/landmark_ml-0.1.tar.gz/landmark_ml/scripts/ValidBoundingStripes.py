import sys
import getopt
from landmark_ml.learning.PageManager import PageManager
import codecs
import os
import json

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
        
        #read the directory location from arg0
        page_file_dir = args[0]
        
        pageManager = PageManager()
        
        for subdir, dirs, files in os.walk(page_file_dir):
            for the_file in files:
                if the_file.startswith('.'):
                    continue
                
                with codecs.open(os.path.join(subdir, the_file), "r", "utf-8") as myfile:
                    page_str = myfile.read().encode('utf-8')
                    
                pageManager.addPage(the_file, page_str)
                
        pageManager.learnStripes()
        
        #Read the markups from a file...
        markups_file = args[1]
        with codecs.open(os.path.join('', markups_file), "r", "utf-8") as myfile:
            markup_str = myfile.read().encode('utf-8')
        markups = json.loads(markup_str)

        print markups

        shortest_pairs = []
        all_bounding_stripes = []
        for markup in markups:
            print "mark:", markup
            page_id = markup
            title = markups[markup]['title']['extract']
            print "title:", title
            shortest_pair = pageManager.getPossibleLocations(page_id, title, False)
            print "shortest_pair:", shortest_pair

            bounding_stripes = pageManager.getAllBoundingStripes(page_id, shortest_pair)

            all_bounding_stripes.append(bounding_stripes)

        print "all bounding stripes:", all_bounding_stripes

        valid_bounding_stripes = pageManager.getValidBoundingStripes(all_bounding_stripes)

        print "valid stripes:", valid_bounding_stripes
        
        begin_stripes = pageManager.getNextLevelStripes(valid_bounding_stripes[0],'begin')

        print "begin stripes:", begin_stripes

        end_stripes = pageManager.getNextLevelStripes(valid_bounding_stripes[0], 'end')

        print "end stripes:", end_stripes

    except Usage, err:
        print >>sys.stderr, err.msg
        print >>sys.stderr, "for help use --help"
        return 2

if __name__ == '__main__':
    sys.exit(main())