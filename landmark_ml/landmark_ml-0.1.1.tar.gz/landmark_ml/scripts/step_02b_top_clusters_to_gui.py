import sys
import json
import getopt
import os
import codecs
from landmark_extractor.extraction.Landmark import RuleSet
import shutil
import copy

rules_file_string = 'step02_rules.json'
directory = "directory"

usage = "step_02b_top_clusters_to_gui -d " + directory

working = os.getcwd()
while not working.endswith('/src'):
    (working,other) = os.path.split(working)
web_app_projects_dir = os.path.join(working, 'angular_flask/static/project_folders')

markup_slot = {
  "id": "j1_2",
  "text": "slot",
  "icon": "glyphicon glyphicon-stop",
  "li_attr": {
    "id": "j1_2"
  },
  "a_attr": {
    "href": "#",
    "id": "j1_2_anchor"
  },
  "state": {
    "loaded": True,
    "opened": False,
    "selected": False,
    "disabled": False
  },
  "data": {},
  "children": [],
  "type": "item"
};

def single_site_copy(sub_dir):
    clusters_dir = os.path.join(directory, sub_dir, 'clusters')
    cdr_dir = os.path.join(directory, sub_dir, 'cdr')
    cluster_dirs = [f for f in os.listdir(clusters_dir) if os.path.isdir(os.path.join(clusters_dir, f))]
    cluster_count = 0
    for cluster_name in cluster_dirs:
        #Top 10 clusters only for now
        if cluster_count == 10:
            break
        
        cluster_dir = os.path.join(clusters_dir, cluster_name)
        rule_file_name = os.path.join(directory, sub_dir, 'clusters', cluster_name, rules_file_string)        
        if not os.path.exists(rule_file_name):
            continue
        
        print '...reapplying rules and copying to GUI for ' + sub_dir + "/" + cluster_name + '...'
        
        rules = None
        with codecs.open(rule_file_name, "r", "utf-8") as myfile:
            rules = RuleSet(json.loads(myfile.read()))
        if rules:
            #create the project UI directory if the rules exist
            blank = os.path.join(web_app_projects_dir, '_blank')
            project_dir = os.path.join(web_app_projects_dir, sub_dir+"_"+cluster_name)
            if os.path.exists(project_dir):
                shutil.rmtree(project_dir)
            shutil.copytree(blank, project_dir)
            
            #copy the rules to the UI directory
            ui_rules_file_name = os.path.join(project_dir, 'learning', 'rules.json')
            shutil.copyfile(rule_file_name, ui_rules_file_name)
            
            #grab the markup so we have the __URLS__ and __SCHEMA__ already setup
            ui_markup_file_name = os.path.join(project_dir, 'learning', 'markup.json')
            with codecs.open(ui_markup_file_name, "r", "utf-8") as myfile:
                json_str = myfile.read().encode('utf-8')
            markup = json.loads(json_str)
            
            rule_count = 1
            for rule in rules.rules:
                rule_count += 1
                auto_markup_slot = copy.deepcopy(markup_slot)
                auto_markup_slot['text'] = rule.name
                auto_markup_slot['id'] = 'j1_'+str(rule_count)
                auto_markup_slot['li_attr']['id'] = 'j1_'+str(rule_count)
                auto_markup_slot['a_attr']['id'] = 'j1_'+str(rule_count)+'_anchor'
                markup['__SCHEMA__'][0]['children'].append(auto_markup_slot)
            
            file_count = 0
            files = [f for f in os.listdir(cluster_dir) if os.path.isfile(os.path.join(cluster_dir, f))]
            for the_file in files:
                #only get 6 pages for now
                if file_count == 6:
                    break
                
                if the_file.startswith('.') or the_file == rules_file_string or the_file.endswith('.json'):
                    continue
                
                clustered_file_string = os.path.join(cluster_dir, the_file)
                
                #copy the file to the UI directory
                shutil.copyfile(clustered_file_string, os.path.join(project_dir, the_file))
                
                #get the real url from the CDR folder
                url = "NON_EXISTENT"
                try:
                    with codecs.open(os.path.join(cdr_dir, the_file.replace('.html', '.json')), "r", "utf-8") as json_file:
                        cdr_str = json_file.read().encode('utf-8')
                        cdr_json = json.loads(cdr_str)
                        url = cdr_json['url']
                except:
                    pass
                
                #add the info about the file to the UI markup
                markup['__URLS__'][the_file] = url
                
                #get the extraction for the file
                with codecs.open(clustered_file_string, "r", "utf-8") as myfile:
                    page_str = myfile.read().encode('utf-8')
                    extraction_list = rules.extract(page_str)
                    markup[the_file] = extraction_list
                
                file_count += 1
        
            #write the markup to the UI markup file
            with codecs.open(ui_markup_file_name, "w", "utf-8") as myfile:
                myfile.write(json.dumps(markup, sort_keys=True, indent=2, separators=(',', ': ')))
            
        cluster_count += 1

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

if directory == 'directory':
    print usage
    sys.exit(2)

single_site = ''
if len(args) > 0:
    single_site = args[0]

if single_site:
    single_site_copy(single_site)
else:
    dirs = [f for f in os.listdir(directory) if os.path.isdir(os.path.join(directory, f))]
    for sub_dir in dirs:
        single_site_copy(sub_dir)