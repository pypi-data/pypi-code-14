import json
import logging
import os.path
import re
import itertools
from itertools import islice, imap
from time import sleep

from requests import Session
from requests.exceptions import ConnectionError

from utils import retry, join_urls, add_exception_info, strip_prefix

log = logging.getLogger(__name__)


class Client(object):
    def __init__(self,
                 server='https://app.businessoptics.biz',
                 base_url='',
                 auth=None,
                 session=None,
                 ):
        super(Client, self).__init__()
        self.server = server
        self.base_url = strip_prefix(base_url, server)
        assert not (auth and session), "A Client can't take both auth details and an existing session"
        if session:
            self.session = session
        else:
            self.session = Session()
            if not auth or isinstance(auth, basestring):
                username = auth
                path = os.path.join(os.path.expanduser('~'), '.businessoptics_client.config')
                try:
                    with open(path) as f:
                        config = json.load(f)
                except (IOError, ValueError):
                    add_exception_info('Failed to load JSON credentials file at ~/.businessoptics_client.config. '
                                       'Create or fix the file or specify auth=(username, apikey).')
                    raise
                if not username:
                    try:
                        username = config['default']
                    except KeyError:
                        raise Exception('No auth specified and no default username found in config.')
                try:
                    apikey = config[username]
                except KeyError:
                    raise Exception('No API key found for username %s in config' % username)
                auth = (username, apikey)
            assert (isinstance(auth, (list, tuple)) and
                    len(auth) == 2 and
                    all(isinstance(x, basestring) for x in auth)), \
                'auth must be a pair of strings: (username, apikey)'
            self.session.headers.update({
                'Authorization': 'ApiKey {}:{}'.format(*auth)
            })

    @classmethod
    def at(cls, client, base_url=None):
        if base_url is None:
            base_url = client.base_url
        return cls(server=client.server,
                   base_url=base_url,
                   session=client.session)

    @classmethod
    def local(cls, auth=('development@businessoptics.biz', 'development'), *args, **kwargs):
        return cls(server='http://app.businessoptics.dev', auth=auth, *args, **kwargs)

    @classmethod
    def staging(cls, *args, **kwargs):
        return cls(server='https://app.businessoptics.net', *args, **kwargs)

    @classmethod
    def production(cls, *args, **kwargs):
        # Production is the default server
        return cls(*args, **kwargs)

    @retry(5, ConnectionError, log)
    def request(self, method, url='', **kwargs):
        url = join_urls(self.server, self.base_url, url)
        response = self.session.request(method, url, **kwargs)
        try:
            response.raise_for_status()
            result = response.json()
            assert result['status'] == 'ok'
            assert result.get('state') != 'error'
            assert not result.get('error')
            return result
        except Exception:
            add_exception_info('Error in response at %s: %s' % (url, response.text[:5000]))
            raise

    def get(self, url='', **kwargs):
        kwargs.setdefault('allow_redirects', True)
        return self.request('GET', url, **kwargs)

    def options(self, url='', **kwargs):
        kwargs.setdefault('allow_redirects', True)
        return self.request('OPTIONS', url, **kwargs)

    def head(self, url='', **kwargs):
        kwargs.setdefault('allow_redirects', False)
        return self.request('HEAD', url, **kwargs)

    def post(self, url='', **kwargs):
        return self.request('POST', url, **kwargs)

    def put(self, url='', **kwargs):
        return self.request('PUT', url, **kwargs)

    def patch(self, url='', **kwargs):
        return self.request('PATCH', url, **kwargs)

    def delete(self, url='', **kwargs):
        return self.request('DELETE', url, **kwargs)

    def __div__(self, other):
        result = Client.at(self)
        result.base_url = join_urls(self.base_url, other)
        return result

    @property
    def root(self):
        return Client.at(self, '')

    @property
    def api(self):
        return Client.at(self, '/api/v2')

    @property
    def internal(self):
        return Client.at(self, '/api/internal')

    def workspace(self, resource_id):
        return Workspace.at(self.api / 'workspace' / resource_id)

    def dashboard(self, resource_id):
        return Dashboard.at(self.api / 'dashboard' / resource_id)

    def dataset(self, resource_id):
        return Dataset.at(self.api / 'dataset' / resource_id)

    def __repr__(self):
        return self.__class__.__name__ + '@' + self.base_url

    def close(self):
        self.session.close()

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.close()


class Workspace(Client):
    def query(self, ideas, parameters=None):
        if isinstance(ideas, basestring):
            ideas = re.split('[,\s]+', ideas)
        parameters = parameters or {}
        response = self.post('query', json=dict(knowledge_parameters=parameters,
                                                ideanames=ideas))
        query = Query.at(self, response['uri'])
        query.ideas = ideas
        return query


class Query(Client):
    def __init__(self, *args, **kwargs):
        super(Query, self).__init__(*args, **kwargs)
        self.finished = False
        self.ideas = None

    def await(self):
        while not self.finished and self.get()['state'] != 'complete':
            sleep(2)
        self.finished = True

    def result(self, information_id=None):
        ideas = self.ideas
        if information_id is None:
            if ideas and len(ideas) == 1:
                information_id = ideas[0]
            else:
                raise ValueError(
                    'You must specify an information identifier for a result unless only one idea was queried')
        self.await()
        return IdeaResult.at(self / 'result' / information_id)

    def tuples(self, information_id=None, limit=None, offset=0):
        return self.result(information_id).tuples(limit, offset)


class HasTuples(Client):
    def tuples(self, limit=None, offset=0):
        limit = self._check_infinite_limit(limit)

        result = []
        while True:
            request_limit = min(2000, limit)
            response = self.get('tuples', params=dict(limit=request_limit, offset=offset))
            result.extend(response['tuples'])
            offset += request_limit
            limit -= request_limit
            if offset >= response['meta']['count'] or limit <= 0:
                return result

    @staticmethod
    def _check_infinite_limit(limit):
        if limit in (0, -1, None):
            limit = 99999999
        return limit

    def stream(self):
        return imap(json.loads,
                    self.session.get(join_urls(self.server, self.base_url, 'stream'),
                                     stream=True
                                     ).iter_lines())


class IdeaResult(HasTuples):
    pass


class Dashboard(Client):
    def query_parameters(self):
        return Query.at(self, self.post('query_parameters')['uri'])

    def parameter_options(self):
        query = self.query_parameters()
        result = []

        def add_parameters_from(obj):
            map(add_parameter, obj['parameters'])

        def add_parameter(parameter):
            def add_to_result():
                parameter['options_tuples'] = tuples
                result.append(parameter)

            if parameter['type'] == 'section':
                add_parameters_from(parameter)
            elif parameter['type'] == 'multi_select':
                options_idea = parameter['options_idea']
                tuples = query.tuples(options_idea)
                tuples = [{selector['idea']: tup[selector['dimension']]
                           for selector in parameter['selectors']}
                          for tup in tuples]
                add_to_result()
            else:
                idea = parameter['idea']
                if parameter['type'] == 'hidden':
                    values = [parameter['value']]
                elif parameter['type'] == 'select':
                    options = parameter['options']
                    options_source = options['options_source']
                    if options_source == 'idea':
                        dimension = options['dimension']
                        tuples = query.tuples(options['idea'])
                        values = [t[dimension] for t in tuples]
                    elif options_source == 'list':
                        values = options['options']
                    else:
                        raise ValueError('Unknown options source %s' % options_source)
                else:
                    raise ValueError('Unknown parameter type %s', parameter['type'])
                tuples = [{idea: value} for value in values]
                add_to_result()

        add_parameters_from(self.get('display'))
        return result


class Dataset(HasTuples):
    @property
    def tableset(self):
        return Tableset.at(self / 'tableset')


class Tableset(Client):
    def upload_tuples(self, tuples):
        batch_size = 2000
        for start in itertools.count(step=batch_size):
            batch = list(islice(tuples, start, start + batch_size))
            if not batch:
                break
            self.post('tuples', json={'tuples': batch})
