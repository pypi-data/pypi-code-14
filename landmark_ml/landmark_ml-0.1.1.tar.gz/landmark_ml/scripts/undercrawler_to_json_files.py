
# ls -1 | python -c "import sys; import random; print(''.join(random.sample(sys.stdin.readlines(), int(sys.argv[1]))).rstrip())" 200 | xargs -I {} mv {} ../cdr/

import sys
import json
import getopt
import os
import codecs
import random
import shutil

crawl_file = "crawl_file"

usage = "undercrawler_to_json_files -f " + crawl_file

try:
    opts, args = getopt.getopt(sys.argv[1:], "hf:")
except getopt.GetoptError:
    print usage
    sys.exit(2)
for opt, arg in opts:
    if opt == '-h':
        print usage
        sys.exit()
    elif opt in "-f":
        crawl_file = arg

if crawl_file == 'crawl_file':
    print usage
    sys.exit(2)
    
crawl_dir = os.path.join(os.path.dirname(crawl_file), "all")
if not os.path.exists(crawl_dir):
    os.makedirs(crawl_dir)

crawl_json = []
file_names = []
with codecs.open(crawl_file, "r", "utf-8") as myfile:
    for line in myfile:
        crawl_page = json.loads(line)
        if not crawl_page['content_type'].startswith('image'):
            json_out = {}
            try:
                if 'raw_content' in crawl_page:
                    json_out['_id'] = crawl_page['_id']
                    json_out['url'] = crawl_page['url']
                    json_out['raw_content'] = crawl_page['raw_content']
                    with codecs.open(os.path.join(crawl_dir, json_out['_id']+".json"), "w", "utf-8") as json_file:
                        json_file.write(json.dumps(json_out, indent=4, separators=(',', ': ')))
                    file_names.append(json_out['_id']+".json")
            except:
                print json.dumps(crawl_page)
                sys.exit()

cdr_dir = os.path.join(os.path.dirname(crawl_file), "cdr")    
if not os.path.exists(cdr_dir):
    os.makedirs(cdr_dir)

for random_file in random.sample(file_names, 200):
    shutil.copyfile(os.path.join(crawl_dir, random_file), os.path.join(cdr_dir, random_file))
