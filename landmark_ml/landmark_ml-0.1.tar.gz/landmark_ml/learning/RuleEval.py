# This Python file uses the following encoding: utf-8

import codecs
import sys
import getopt

import logging
from landmark_ml.extraction.ExtractionCheck import run_extraction_check

import json
from landmark_extractor.extraction.Landmark import RuleSet
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("landmark")
handler = logging.FileHandler('landmark.log')
handler.setLevel(logging.INFO)
formatter = logging.Formatter(u'%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg

def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        try:
            opts, args = getopt.getopt(argv[1:], "dh", ["debug", "help"])
            
            for opt in opts:
                if opt in [('-h', ''), ('--help', '')]:
                    raise Usage('python -m learning.RuleLearnerAllSlots [OPTIONAL_PARAMS] [TEST_FILES_FOLDER] \n\t[OPTIONAL_PARAMS]: -d to get debug stripe html files')
        except getopt.error, msg:
            raise Usage(msg)
        
        logger.info('Running RuleEval with files at %s and rules %s', args[0], args[1])
        
        #read the directory location from arg0
        page_file_dir = args[0]
        
        json_file_str = args[1]
        with codecs.open(json_file_str, "r", "utf-8") as myfile:
            json_str = myfile.read().encode('utf-8')
        json_object = json.loads(json_str)
        rules = RuleSet(json_object)
        
        run_extraction_check(page_file_dir, '../../output/watable/', rules)
        
        
    except Usage, err:
        print >>sys.stderr, err.msg
        print >>sys.stderr, "for help use --help"
        return 2
    
if __name__ == '__main__':
    sys.exit(main())