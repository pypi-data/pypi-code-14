import sys
import json
import getopt
import os
import codecs
from landmark_extractor.extraction.Landmark import flattenResult, RuleSet
from landmark_ml.learning import PageClusterer, RuleLearnerAllSlots

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
cluster_meta_data_string = 'cluster_meta_data.json'
directory = "directory"
cluster_dir = None
usage = "step_01_rules_to_extrations -d " + directory

def do_site_extraction(cluster_name, cdr_dir, cluster_dir):
    rules = RuleLearnerAllSlots.run(cluster_dir, ignore_files = ['step01_extractions.jl', 'step01_rules.json', 'cluster_meta_data.json'])
    
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
                if the_file.startswith('.') or the_file == rules_file_string or the_file == output_file_string or the_file == cluster_meta_data_string:
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

try:
    opts, args = getopt.getopt(sys.argv[1:], "hd:e:")
except getopt.GetoptError:
    print usage
    sys.exit(2)
for opt, arg in opts:
    if opt == '-h':
        print usage
        sys.exit()
    elif opt in "-d":
        directory = arg
    elif opt in "-e":
        cluster_dir = arg

if cluster_dir:
    if cluster_dir.endswith('/'):
        cluster_dir = cluster_dir[:-1]
    cluster_path, cluster_name = os.path.split(cluster_dir)
    path, ignore = os.path.split(cluster_path)
    cdr_dir = os.path.join(path, 'cdr')
    print 'extracting from ' + cluster_dir
    print cdr_dir
    print cluster_name
    do_site_extraction(cluster_name, cdr_dir, cluster_dir)
    sys.exit()

single_site = ''
if len(args) > 0:
    single_site = args[0]

if directory == 'directory':
    print usage
    sys.exit(2)

if single_site:
    single_site_cluster(single_site)
else:
    dirs = [f for f in os.listdir(directory) if os.path.isdir(os.path.join(directory, f))]
    for sub_dir in dirs:
        single_site_cluster(sub_dir)
    
#         #for now just get cluster001
#         top_clusters_rules = None
#         top_clusters_rules_file = os.path.join(directory, sub_dir, 'clusters', 'cluster001', rules_file_string)
#         with codecs.open(top_clusters_rules_file, "r", "utf-8") as myfile:
#             top_clusters_rules = RuleSet(json.loads(myfile.read()))
#         
#         bad_dir = os.path.join(directory, sub_dir, "bad")
#         if not os.path.exists(bad_dir):
#             os.makedirs(bad_dir)
#         
#         if top_clusters_rules:
#             print '====== TESTING RULES ====='
#             print top_clusters_rules_file
#             print len(top_clusters_rules.rules)
#             print '=========================='
#             files = [f for f in os.listdir(html_dir) if os.path.isfile(os.path.join(html_dir, f))]
#             for the_file in files:
#                 if the_file.startswith('.'):
#                     continue
#                 with codecs.open(os.path.join(html_dir, the_file), "r", "utf-8") as myfile:
#                     page_str = myfile.read().encode('utf-8')
#                     extracts = top_clusters_rules.extract(page_str)
#                     flat_extracts = flattenResult(extracts)
#                     good_count = 0
#                     for key in flat_extracts:
#                         if len(flat_extracts[key]) > 0:
#                             good_count += 1
#                     if good_count < len(top_clusters_rules.rules)/2:
#                         copyfile(os.path.join(html_dir, the_file), os.path.join(bad_dir, the_file))
#                         print the_file + " is BAD"