'''
'''
import json
from urllib import request, parse

class Scraper:
    # +-------------------------------------------------------------------------
    def __init__(self):
        self.name = ''
    # +-------------------------------------------------------------------------
    def get(self, url):
        pass
    # +-------------------------------------------------------------------------
    def post(self, url, params, fmt=None):
        '''
        '''
        if fmt == 'json':
            params = json.dumps(params)
        else:
            params = parse.urlencode(params)
            print(params)
        response = request.urlopen(url,params.encode('utf-8'))
        data = response.read().decode('utf-8')
        if fmt == 'json':
            return json.loads(data)
        return data
