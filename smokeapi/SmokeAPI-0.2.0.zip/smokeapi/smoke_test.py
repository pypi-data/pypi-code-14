from smokeapi import SmokeAPI, SmokeAPIError
import datetime
import pprint
from HTMLParser import HTMLParser
from urlparse import urlparse
from collections import Counter
from findspam import FindSpam
import colorama
import urllib
import requests

SMOKE = SmokeAPI('aa6cb28600cfa209789a33284bca4b025beed39c5dfb171d5030c88189403d81')
SMOKE.max_pages = 100

TOP_RESULTS = 200
LAST_DAYS = 30

RESET_COLOR = colorama.Fore.RESET

# Download latest files from Github
files = [
    {'file': 'https://raw.githubusercontent.com/Charcoal-SE/SmokeDetector/master/blacklisted_websites.txt',
     'reload': False,
     'reload_string': None},
    {'file': 'https://raw.githubusercontent.com/Charcoal-SE/SmokeDetector/master/bad_keywords.txt',
     'reload': False,
     'reload_string': None},
    {'file': 'https://raw.githubusercontent.com/Charcoal-SE/SmokeDetector/master/findspam.py',
     'reload': True,
     'reload_string': 'FindSpam'},
]

for f in files:
    r = requests.get(f['file'])
    filename = f['file'].split('/')[-1]
    with open(filename, 'w') as outfile:
        outfile.write(r.content)

for f in files:
    if f['reload']:
        import importlib
        r = f['file'].split('/')[-1].split('.')[0]
        importlib.import_module(r)


class URLParser(HTMLParser):
    """ Extract URLs from a string """

    def __init__(self, output_list=None):
        HTMLParser.__init__(self)
        if output_list is None:
            self.output_list = []
        else:
            self.output_list = output_list

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            self.output_list.append(dict(attrs).get('href'))

yesterday = datetime.datetime.utcnow() - datetime.timedelta(days=1)
start_date_range = datetime.datetime.utcnow() - datetime.timedelta(days=LAST_DAYS)

try:
    posts = SMOKE.fetch('posts/search',
                        from_date=start_date_range,
                        to_date=yesterday,
                        )
except SmokeAPIError as e:
    print("   Error URL: {}".format(e.url))
    print("   Error Code: {}".format(e.error_code))
    print("   Error Name: {}".format(e.error_name))
    print("   Error Message: {}".format(e.error_message))

truepositives = [post for post in posts['items'] if post['is_tp']]

# Let's pull out some URLs:
urls = URLParser()
domains = []

for p in truepositives:
    urls.feed(p['body'])

for url in urls.output_list:
    try:
        parsed_uri = urlparse(url)
        domains.append('{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri))
    except ValueError as e:
        pass


unique_urls = list(set(urls.output_list))
unique_domains = list(set(domains))
count_urls = Counter(urls.output_list)
count_domains = Counter(domains)

top_domains = {url: {'count': count, 'caught': False} for url, count in count_domains.most_common(TOP_RESULTS)}
top_urls = {url: {'count': count, 'caught': False} for url, count in count_urls.most_common(TOP_RESULTS)}

for domain in top_domains:
    reasons, why = FindSpam.test_post(domain, domain, domain, "", False, False, 1, 0)
    if reasons:
        top_domains[domain]['caught'] = True

for domain in top_urls:
    reasons, why = FindSpam.test_post(domain, domain, domain, "", False, False, 1, 0)
    if reasons:
        top_urls[domain]['caught'] = True


print "Total Posts seen by MetaSmoke: {}".format(len(posts['items']))
print "Total True Positves: {}".format(truepositives)
print "Total URLs: {}".format(len(urls.output_list))
print "Total Domains: {}".format(len(domains))
print "Total Unique URLs: {}".format(len(unique_urls))
print "Total Unique domains: {}".format(len(unique_domains))
# print "{} Most Common (Domains):".format(TOP_RESULTS)
sorted_domains = sorted(top_domains.items(), key=lambda (k,v):v['count'], reverse=True)
# for url in sorted_domains:
#     print "      {count}  {displaycolor}{caught}{reset}   {url}".format(
#         count=url[1]['count'],
#         url=url[0],
#         displaycolor=colorama.Fore.GREEN if url[1]['caught'] else colorama.Fore.RED,
#         caught=url[1]['caught'],
#         reset=RESET_COLOR)
# print "{} Most Common (Full Path):".format(TOP_RESULTS)
sorted_urls = sorted(top_urls.items(), key=lambda (k,v):v['count'], reverse=True)
# for url in sorted_urls:
#     print "      {count}  {displaycolor}{caught}{reset}   {url}".format(
#         count=url[1]['count'],
#         url=url[0],
#         displaycolor=colorama.Fore.GREEN if url[1]['caught'] else colorama.Fore.RED,
#         caught=url[1]['caught'],
#         reset=RESET_COLOR)
print "URLs that would not be caught:"
ms_search_string = """https://metasmoke.erwaysoftware.com/search?utf8=%E2%9C%93&title=&body={pattern}&username=&why=&site=&feedback=&reason=&user_rep_direction=%3E%3D&user_reputation=0&commit=Search"""
for url in sorted_domains:
    if not url[1]['caught']:
        search_string = ms_search_string.format(pattern=urllib.quote(url[0][:-1]))
        print "      {count}  {displaycolor}{caught}{reset}   {url}  => {searchstring}".format(
            count=url[1]['count'],
            url=url[0],
            displaycolor=colorama.Fore.GREEN if url[1]['caught'] else colorama.Fore.RED,
            caught=url[1]['caught'],
            reset=RESET_COLOR,
            searchstring=search_string)


