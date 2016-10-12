import sys
import json
import getopt
import os
import codecs
import webbrowser
import shutil

from landmark_extractor.extraction.Landmark import RuleSet
from extraction.ExtractionCheck import run_extraction_check

rules_file_string = 'step03_rules.json'
output_file_location = '_output_TEMPLATE'
directory = "directory"
usage = "step_03b_tld_rules_to_extractions -d " + directory

def single_site_run(sub_dir):
    print '...applying rules to ' + sub_dir + '...'
    cdr_dir = os.path.join(directory, sub_dir, 'cdr')
    with codecs.open(os.path.join(directory, sub_dir, rules_file_string), "r", "utf-8") as myfile:
        json_str = myfile.read().encode('utf-8')
    json_object = json.loads(json_str)
    rules = RuleSet(json_object)
    
    output_template_dir = os.path.join(os.getcwd(), output_file_location)
    output_dir = os.path.join(directory, sub_dir, '_extraction_eval')
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    shutil.copytree(output_template_dir, output_dir)
    
    run_extraction_check(cdr_dir, os.path.join(output_dir, 'watable'), rules, is_cdr_format = True)
    webbrowser.open_new('file://'+ os.path.join(output_dir, 'watable', 'eval.html') )

try:
    opts, args = getopt.getopt(sys.argv[1:], "hd:")
except getopt.GetoptError:
    print usage
    sys.exit(2)
for opt, arg in opts:
    if opt == '-h':
        print usage
        sys.exit()
    elif opt in "-d":
        directory = arg

single_site = ''
if len(args) > 0:
    single_site = args[0]

if directory == 'directory':
    print usage
    sys.exit(2)

if single_site:
    single_site_run(single_site)
else:
    dirs = [f for f in os.listdir(directory) if os.path.isdir(os.path.join(directory, f))]
    for sub_dir in dirs:
        single_site_run(sub_dir)
