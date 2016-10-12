import sys
import json
import getopt
import os
import codecs
from landmark_extractor.extraction.Landmark import RuleSet, flattenResult
from landmark_ml.learning import PageClusterer, RuleLearnerAllSlots
import shutil
import copy

import logging.handlers
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger("landmark")
main_file = os.path.abspath(sys.modules['__main__'].__file__)
main_directory = os.path.dirname(main_file)
handler = logging.handlers.RotatingFileHandler(
              os.path.join(main_directory,'landmark.log'), maxBytes=10*1024*1024, backupCount=5)
handler.setLevel(logging.INFO)
formatter = logging.Formatter(u'%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

rules_file_string = 'step01_rules.json'
output_file_string = 'step01_extractions.jl'
directory = "directory"
cluster_dir = None
usage = "python runclustering.py -d " + directory + " [OPTIONAL_SINGLE_SITE]"

def do_site_extraction(cluster_name, cdr_dir, cluster_dir):
    rules = RuleLearnerAllSlots.run(cluster_dir, ignore_files = ['step01_extractions.jl', 'step01_rules.json'])
    
    for rule in rules.rules:
        rule.removehtml = True
    
    json_file_str = os.path.join(cluster_dir, rules_file_string)
    with codecs.open(json_file_str, "w", "utf-8") as myfile:
        myfile.write(json.dumps(json.loads(rules.toJson()), sort_keys=True, indent=2, separators=(',', ': ')))
        
        #now we apply the extractions for the files
        jl_file = os.path.join(cluster_dir, output_file_string)
         
        with codecs.open(jl_file, "w", encoding='utf-8') as extractions_jl:
            print '...applying rules for ' + cluster_name + '...'
            logger.info('...applying rules for ' + cluster_name + '...')
            files = [f for f in os.listdir(cluster_dir) if os.path.isfile(os.path.join(cluster_dir, f))]
            for the_file in files:
                if the_file.startswith('.') or the_file == rules_file_string or the_file == output_file_string:
                    continue
                
                json_line = {}
                json_line['_cdr_id'] = the_file.replace('.html', '')
                 
                #go get the url from the other file... HACK!!!
                url = ''
                with codecs.open(os.path.join(cdr_dir, json_line['_cdr_id']+'.json'), "r", "utf-8") as json_file:
                    cdr_str = json_file.read().encode('utf-8')
                    cdr_json = json.loads(cdr_str)
                    url = cdr_json['url']
                
                json_line["_url"] = url
                with codecs.open(os.path.join(cluster_dir, the_file), "r", "utf-8") as myfile:
                    page_str = myfile.read().encode('utf-8')
                    
                    try:
                        extraction_list = rules.extract(page_str)
                        json_line.update(flattenResult(extraction_list))
                        extractions_jl.write(json.dumps(json_line))
                        extractions_jl.write('\n')
                    except:
                        print 'ERROR extracting from ' + the_file + '...'
                        logger.info('ERROR extracting from ' + the_file + '...')

def single_site_cluster(sub_dir):
    print '...clustering ' + sub_dir + '...'
    logger.info('...clustering ' + sub_dir + '...')
    cdr_dir = os.path.join(directory, sub_dir, 'cdr')
    html_dir = os.path.join(directory, sub_dir, 'html')
    clusters_dir = os.path.join(directory, sub_dir, 'clusters')
    
    #count the files in the html directory if there are less than 6 skip it!
    num_files = len([f for f in os.listdir(html_dir) if os.path.isfile(os.path.join(html_dir, f)) and not f.startswith('.')])
    if num_files < 6:
        print 'SKIPPING because only has ' + str(num_files) + ' pages'
        logger.info('SKIPPING because only has ' + str(num_files) + ' pages')
        return
    #if the cluster dir already exists then skip it!
    if os.path.exists(clusters_dir):
        print 'SKIPPING because already clustered'
        logger.info('SKIPPING because already clustered')
        return
    PageClusterer.cluster(sub_dir, html_dir)
    
    #now there should be clusters for the whole thing we need to learn rules
    cluster_dirs = [f for f in os.listdir(clusters_dir) if os.path.isdir(os.path.join(clusters_dir, f))]
    for cluster_name in cluster_dirs:
        print '...learning rules for ' + cluster_name + '...'
        logger.info('...learning rules for ' + cluster_name + '...')
        cluster_dir = os.path.join(clusters_dir, cluster_name)
        do_site_extraction(cluster_name, cdr_dir, cluster_dir)

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

single_site = ''
if len(args) > 0:
    single_site = args[0]

if directory == 'directory':
    print usage
    sys.exit(2)

if single_site:
    single_site_cluster(single_site)
    single_site_copy(single_site)
else:
    dirs = [f for f in os.listdir(directory) if os.path.isdir(os.path.join(directory, f))]
    for sub_dir in dirs:
        single_site_cluster(sub_dir)
        single_site_copy(single_site)