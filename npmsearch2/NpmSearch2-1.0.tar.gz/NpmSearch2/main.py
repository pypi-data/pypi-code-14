# whole package list is HERE! - http://stackoverflow.com/a/34076754
# http://registry.npmjs.org/-/all

import urllib as urllib

import json

class NPMListener:
    def __init__(self):
        pass

    def downloaded_file(self,URL): # big joker this dragon. only works once, subsequent calls fail.
        response = urllib.urlopen(URL)
        file = response.read()
        response.close()
        return file

    def search_file(self,keywords_str):
        url = "http://npmsearch.com/query?q="+ keywords_str + "&dom&fields=name"
        # url = "http://registry.npmjs.org/" + keywords_str  # package details string
        results = json.loads(self.downloaded_file(url),encoding="utf-8")
        results_list = []
        for row in results["results"]:
            name = str(row["name"][0])
            results_list.append(name)
        return list(results_list)

    def lookup_project(self,project_name):
        url = "http://registry.npmjs.org/" + project_name  # package details string
        lookup_results = json.loads(self.downloaded_file(url))
        return dict(lookup_results)


if __name__ == '__main__':
    search_query = "express" # put your search term here .. hope you can read json!

    listener = NPMListener()
    results = listener.search_file(search_query)
    for row in results:
        print row

    print results

    print "print entire project details"
    for name in results:
        print name
        print listener.lookup_project(name)