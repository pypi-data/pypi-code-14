import sys
import getopt
from landmark_ml.learning.TruffleShuffle import TruffleShuffle
from landmark_ml.learning.PageManager import PageManager
from landmark_extractor.extraction.Landmark import RuleSet
import requests
import json

DEBUG = False
SEMANTICTYPER_URL = 'http://52.38.65.60:80/search?namespaces=http%3A%2F%2Fdig.isi.edu'

class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg

def semanticType(extracts):
    the_type = ''
    good = False
    payload = '\n'.join(extracts)
    r = requests.post(SEMANTICTYPER_URL, data=payload)
    if r.status_code == 200:
        json_array = json.loads(r.text)
        the_type = json_array[0]['property']
        score = json_array[0]['score']
        if score > 0.06 and not the_type.startswith('notRelevant'):
            good = True
    return (the_type, good)

def semanticallyTypeRules(rule_set):
    semantic_rules = RuleSet()
    pages = rule_set['test_pages']
    rules = rule_set['rules']
    count = 1
    num_good = 0
    for rule in rules.rules:
        extracts = []
        for page in pages:
            extractaction = rule.apply(page)
            if extractaction['extract']:
                extracts.append(extractaction['extract'])
                
        if len(extracts) > 0:
            (semantic_type, good) = semanticType(extracts)
            if len(semantic_type) > 0:
                if good:
                    num_good += 1
                rule.name = semantic_type + format(count, '03')
                rule.removehtml = True
                semantic_rules.add_rule(rule)
                count += 1
    return (semantic_rules, num_good)

def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        try:
            opts, args = getopt.getopt(argv[1:], "h", ["help"])
            
            if '--help' in opts:
                raise Usage("ERROR!!!")
            
            json_lines_file = args[0]
            site_name = json_lines_file.split('/')[-1].split('.jl')[0]
            
            tf = TruffleShuffle(json_lines_file=json_lines_file)
            clusters = tf.do_truffle_shuffle(algorithm='rule_size')
            tf_page_manager = tf.get_page_manager()
            cluster_number = 0
            
            rule_sets = []
            if len(clusters) > 0:
                for rule in clusters:
                    cluster_number += 1
                    cluster_str = 'cluster' + format(cluster_number, '03')
                    
                    #learn the rules for this cluster if there are more than 5 pages in it
#                     print cluster_str + " -- " + str(len(clusters[rule]['MEMBERS']))
                    if len(clusters[rule]['MEMBERS']) > 5:
                        rule_set = []
                        pm = PageManager()
                        test_pages = []
                        
                        for page_id in clusters[rule]['MEMBERS']:
                            page_str = tf_page_manager.getPage(page_id).getString()
                            if len(pm.getPageIds()) < 7:
                                pm.addPage(page_id, page_str, False)
                            test_pages.append(page_str)
                            
                        pm.learnStripes()
                        rule_set = pm.learnAllRules()
                        
                        if DEBUG:
                            print cluster_str
                        #Clean the clusters rules
                        rule_set.removeBadRules(test_pages)
                        #print rule_set.toJson()
                        rule_sets.append(
                                        {'cluster_name': cluster_str,
                                         'rules': rule_set,
                                         'test_pages': test_pages}
                                         )
                        
            else:
                #This case means all the pages are the same cluster
                cluster_number += 1
                cluster_str = 'cluster' + format(cluster_number, '03')
                
                pm = PageManager()
                test_pages = []
                for page_id in tf_page_manager.getPageIds():
                    page_str = tf_page_manager.getPage(page_id).getString()
                    if len(pm.getPageIds()) < 7:
                        pm.addPage(page_id, page_str, False)
                    test_pages.append(page_str)
                pm.learnStripes()
                rule_set = pm.learnAllRules()
                #print 'Cluster ' + str(cluster_number)
                
                #Clean the clusters rules
                rule_set.removeBadRules(test_pages)
                rule_sets.append(
                                {'cluster_name': cluster_str,
                                 'rules': rule_set,
                                 'test_pages': test_pages}
                                 )
                #print rule_set.toJson()
            
            best_rule_set = RuleSet()
            best_rule_set_good_types = 0
            for rule_set in rule_sets:
                (new_rule_set, num_good) = semanticallyTypeRules(rule_set)
                if num_good > best_rule_set_good_types:
                    best_rule_set = new_rule_set
                    best_rule_set_good_types = num_good
#                     print 'picking ' + rule_set['cluster_name']
                
            print best_rule_set.toJson()
        
        except getopt.error, msg:
            raise Usage(msg)
 
    except Usage, err:
        print >>sys.stderr, err.msg
        print >>sys.stderr, "for help use --help"
        return 2
    
if __name__ == '__main__':
    sys.exit(main())