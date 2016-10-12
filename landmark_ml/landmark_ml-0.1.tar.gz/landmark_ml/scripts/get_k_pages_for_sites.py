import urllib3
import sys
from elasticsearch import Elasticsearch
import json
import getopt
import os
import codecs
urllib3.disable_warnings()

user_password = "user:password"
output_dir = '../../dig-data/sample-datasets/escorts/'
num_pages = 200

usage = "get_random_pages_for_sites -u " + user_password

try:
    opts, args = getopt.getopt(sys.argv[1:], "hu:")
except getopt.GetoptError:
    print usage
    sys.exit(2)

for opt, arg in opts:
    if opt == '-h':
        print usage
        sys.exit()
    elif opt in "-u":
        user_password = arg

cdr = "https://" + user_password + "@els.istresearch.com:19200/memex-domains"
es = Elasticsearch(cdr)

# Query to get the list of sites that have descriptions
#
sites_query = {
    "aggs": {
        "with-descriptions": {
            "filter": {
                "bool": {
                    "must": [
                        {
                            "term": {
                                "version": "2.0"
                            }
                        },
                        {
                            "exists": {
                                "field": "extractions.text.results"
                            }
                        }
                    ]
                }
            },
            "aggs": {
                "description": {
                    "terms": {
                        "field": "extractions.text.attribs.target",
                        "size": 1000
                    }
                }
            }
        }
    },
    "size": 0
}

pages_query = {
    "size": 200,
    "_source": {
        "include": [
            "extractions",
            "raw_content",
            "url"
        ]
    },
    "query": {
        "function_score": {
            "query": {
                "bool": {
                    "must": [{
                        "term": {
                            "version": "2.0"
                        }
                    }, {
                        "term": {
                            "extractions.text.attribs.target": "{{site}}"
                        }
                    }]
                }
            },
            "functions": [{
                "random_score": {}
            }]
        }
    },
    "sort": [{
        "_score": {
            "order": "desc"
        }
    }]
}

# Get the list of sites
#
buckets = es.search(index='escorts', body=sites_query)['aggregations']['with-descriptions']['description']['buckets']
sites = map(lambda x: x['key'], buckets)
print ", ".join(sites)

# Substitute the site into the {{site}} in the query and run the query
#

pages_query = {
    "size": 200,
    "_source": {
        "include": [
            "extractions",
            "raw_content",
            "url"
        ]
    },
    "query": {
        "function_score": {
            "query": {
                "bool": {
                    "must": [{
                        "term": {
                            "_type": "escorts"
                        }
                    }, {
                        "term": {
                            "domain": "theeroticreview.com"
                        }
                    }]
                }
            },
            "functions": [{
                "random_score": {}
            }]
        }
    },
    "sort": [{
        "_score": {
            "order": "desc"
        }
    }]
}
sites = ['theeroticreview']

pages_query_string = json.dumps(pages_query)

for s in sites:
    site_directory = os.path.join(output_dir, s)
    json_directory = os.path.join(site_directory, "cdr")
    html_directory = os.path.join(site_directory, "html")
    if not os.path.exists(site_directory):
        os.makedirs(site_directory)
    if not os.path.exists(json_directory):
        os.makedirs(json_directory)
    if not os.path.exists(html_directory):
        os.makedirs(html_directory)
        
    q = json.loads(pages_query_string.replace("{{site}}", s))
    for hit in es.search(index='escorts', body=q, request_timeout=30)['hits']['hits']:
        json_vals = {}
        _id = hit['_id']
        raw_content =  hit['_source']['raw_content']
        
        json_vals['_id'] = _id
        
        json_vals['extractions'] = hit['_source']['extractions']
        json_vals['raw_content'] = raw_content
        json_vals['url'] = hit['_source']['url']
        
        
        #write the json file first into /cdr/
        filename = os.path.join(json_directory, _id + '.json')
        with codecs.open(filename, "w", encoding='utf-8') as site_file:
            site_file.write(json.dumps(json_vals, indent=4, separators=(',', ': ')))
            site_file.close()
        
        #then write the html file into /html/
        filename = os.path.join(html_directory, _id + '.html')
        with codecs.open(filename, "w", encoding='utf-8') as site_file:
            site_file.write(raw_content)
            site_file.close()
        
        print "wrote json and html for %s" % _id
        
