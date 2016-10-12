import sys
import codecs
import json
import getopt
import os
from landmark_ml.learning.PageManager import PageManager

def main(argv=None):
    if argv is None:
        argv = sys.argv
        
    opts, args = getopt.getopt(argv[1:], "h", ["help"])
    project_name = args[0]
    
    working = os.getcwd()
    while not working.endswith('/src'):
        (working,other) = os.path.split(working)
    web_app_projects_dir = os.path.join(working, 'angular_flask/static/project_folders')
    
    directory = os.path.join(web_app_projects_dir, project_name)
    markup_file = os.path.join(directory, 'learning', 'markup.json')
    with codecs.open(markup_file, "r", "utf-8") as myfile:
        json_str = myfile.read().encode('utf-8')
        
    markup = json.loads(json_str)
    
    pageManager = PageManager()
    for key in markup['__URLS__']:
        page_file = os.path.join(directory, key)
        with codecs.open(page_file, "r", "utf-8") as myfile:
            page_str = myfile.read().encode('utf-8')
        pageManager.addPage(key, page_str)

    markup.pop("__SCHEMA__", None)
    markup.pop("__URLS__", None)

    pageManager.learnStripes(markup)
    rule_set = pageManager.learnRulesFromMarkup(markup)
    
    print rule_set.toJson()

if __name__ == '__main__':
    sys.exit(main())