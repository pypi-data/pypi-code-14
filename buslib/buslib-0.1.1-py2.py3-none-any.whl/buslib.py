import requests
import json as _json

def remove_system_keys(item, ignore_id=True):
    for key in item.keys():
        if key[0]=="_" and not (key == "_id" and ignore_id):
            item.pop(key)

def parse_response(response, ignore_id=True):
    json = response.json()
    if json.has_key('_items'):
        items = response.json()['_items']
        map(lambda x: remove_system_keys(x, ignore_id), items)
        return items
    remove_system_keys(json, ignore_id)
    return json

DEFAULT_MAX_RESULTS = 20000

class Endpoint:

    def __init__(self, session, endpoint, host="http://localhost:5100/api"):
        self._s = session
        self._endpoint = endpoint
        self._host = host

    def get(self, **kwargs):
        # adjust args
        parse = kwargs.pop('parse', True)
        if kwargs.get('max_results') is None: kwargs['max_results'] = DEFAULT_MAX_RESULTS
        
        args = '&'.join([key + '=' + _json.dumps(kwargs[key]) for key in kwargs.keys()])
        if len(args) > 0:
            args = '?'+args    
        response = self._s.get(url = self._host + '/' + self._endpoint + args)
        if parse:
            return parse_response(response)
        else:
            return response
                        
    def get_one(self, id, parse=True):
        response = self._s.get(url = self._host + '/' + self._endpoint + '/' + id)
        if parse:
            return parse_response(response)
        else:
            return response

    def post(self, json):
        return self._s.post(url = self._host + '/' + self._endpoint)

    def patch(self, id, update):
        response = self.get_one(id, parse=False)
        if (response.status_code // 200 != 1): return response

        json = response.json()
        etag = json['_etag']
        json = parse_response(response, ignore_id=False)
        json.update(update)

        self._s.headers['If-Match'] = etag
        response = self._s.patch(url = self._host + '/' + self._endpoint + '/' + id, json=json)

        self._s.headers['If-Match'] = None
        return response

class Client:

    def __init__(self, api_key, host="http://localhost:5100/api"):
        self._s = requests.Session()
        self._s.headers["Authorization"] = '{ "id_token": "%s" }'%api_key
        self._host = host

    @property
    def buildings(self):
        return Endpoint(self._s, 'buildings', self._host)
    
    @property
    def accounts(self):
        return Endpoint(self._s, 'accounts', self._host)
    
    @property
    def benchmarks(self):
        return Endpoint(self._s, 'benchmarks', self._host)
    
    @property
    def occupant_responses(self):
        return Endpoint(self._s, 'occupant_responses', self._host)

    @property
    def partners(self):
        return Endpoint(self._s, 'partners', self._host)

    @property
    def questions(self):
        return Endpoint(self._s, 'questions', self._host)

    @property
    def surveys(self):
        return Endpoint(self._s, 'surveys', self._host)
