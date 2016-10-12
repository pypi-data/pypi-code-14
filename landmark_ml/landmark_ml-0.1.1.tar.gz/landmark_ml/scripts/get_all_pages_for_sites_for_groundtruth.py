import urllib3
import sys
from elasticsearch import Elasticsearch
import getopt
import codecs
import re
import json
urllib3.disable_warnings()

user_password = "user:password"
domain = "domain"
gt_regex = 'gt_regex'
limit = None

usage = "get_all_pages_for_sites_for_groundtruth -u " + user_password + " -d " + domain + " -g " + gt_regex

try:
    opts, args = getopt.getopt(sys.argv[1:], "hu:d:g:l:")
except getopt.GetoptError:
    print usage
    sys.exit(2)

for opt, arg in opts:
    if opt == '-h':
        print usage
        sys.exit()
    elif opt in "-u":
        user_password = arg
    elif opt in "-d":
        domain = arg
    elif opt in "-g":
        gt_regex = arg
    elif opt in "-l":
        limit = int(arg)

if user_password == "user:password" or domain == "domain" or gt_regex == 'gt_regex':
    print usage
    sys.exit(2)

ground_truth_regex = re.compile(gt_regex)

all_output_file = '_'+domain+'_all_urls.txt'
groundtruth_output_file = '_'+domain+'_gt.jl'
other_output_file = '_'+domain+'_not_gt.jl'

cdr = "https://" + user_password + "@els.istresearch.com:19200"
es = Elasticsearch(cdr, timeout=30)

# Query to get 1000 urls at a time
urls_query = {
   "query": {
      "match": {
          "url.domain": domain
      }
   },
   
   "_source": {
        "include": [
            "url",
            "raw_content"
        ]
    }
}

# Initialize the scroll
page = es.search(
  scroll = '2m',
  search_type = 'scan',
  size = 10,
  body = urls_query,
  request_timeout=30)
sid = page['_scroll_id']
scroll_size = page['hits']['total']

gt_links = {}
other_links = {}

# Start scrolling
done = False
with codecs.open(all_output_file, "w", encoding='utf-8') as all_site_file:
    while (scroll_size > 0 and not done):
        print "Scrolling..."
        page = es.scroll(scroll_id = sid, scroll = '2m')
        # Update the scroll ID
        sid = page['_scroll_id']
        # Get the number of results that we returned in the last scroll
        scroll_size = len(page['hits']['hits'])
        print "scroll size: " + str(scroll_size)
        # Do something with the obtained page
        for hit in page['hits']['hits']:
            json_vals = {}
            _id = hit['_id']
            url = hit['_source']['url']
            if 'raw_content' in hit['_source']:
                raw_content = hit['_source']['raw_content']
            all_site_file.write(url + "\n")
            
            if ground_truth_regex.search(url):
                gt_links[url] = hit
                if limit:
                    if len(gt_links.keys()) >= limit:
                        done = True
                        break
            else:
                other_links[url] = hit
                
with codecs.open(groundtruth_output_file, "w", encoding='utf-8') as gt_file:
    for url in gt_links:
        gt_file.write(json.dumps(gt_links[url]) + "\n")
    gt_file.close()
    
with codecs.open(other_output_file, "w", encoding='utf-8') as other_file:
    for url in other_links:
        other_file.write(json.dumps(other_links[url]) + "\n")
    other_file.close()
                        