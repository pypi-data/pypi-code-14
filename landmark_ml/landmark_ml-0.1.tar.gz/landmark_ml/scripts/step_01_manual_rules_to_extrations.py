import json
import os
import codecs
from landmark_extractor.extraction.Landmark import flattenResult, RuleSet

rules_file_string = 'step01_rules.json'
output_file_string = 'step01_extractions.jl'
pages = [
         {'_cdr': 'page_1.html', '_url': 'url1'},
         {'_cdr': 'page_3.html', '_url': 'url2'},
         {'_cdr': 'page_4.html', '_url': 'url3'},
         {'_cdr': 'page_5.html', '_url': 'url4'}
         ]

json_line = {}
directory = '/cluster_dir/'

with codecs.open(os.path.join(directory, rules_file_string), "r", "utf-8") as myfile:
    json_str = myfile.read().encode('utf-8')
json_object = json.loads(json_str)
rules = RuleSet(json_object)

jl_file = os.path.join(directory, output_file_string)
with codecs.open(jl_file, "w", encoding='utf-8') as extractions_jl:
    for page in pages:
        json_line = {}
        json_line["_cdr"] = page["_cdr"]
        json_line["_url"] = page['_url']
        
        with codecs.open(os.path.join(directory, json_line["_cdr"]), "r", "utf-8") as myfile:
            page_str = myfile.read().encode('utf-8')
            
            extraction_list = rules.extract(page_str)
            json_line.update(flattenResult(extraction_list))
            extractions_jl.write(json.dumps(json_line))
            extractions_jl.write('\n')
