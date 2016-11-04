"""
Core models used for accessing Nanigans ads server(s).
"""
import requests

from nanigans import auth
from nanigans.structures import StringDescriptor, DictDescriptor, ListDescriptor

class PreparedRequest(object):
	"""The '<Nanigans Prepared Request [resource]>' object is used to send a
    request to one of the Nanigans resources.
	
	THe following are available resources:

	Timeranges endpoint:
	/sites/:siteId/datasources/:datasourceId/timeRanges
	
	Attributes endpoint:
	/sites/:siteId/datasources/:datasourceId/attributes
	
	Metrics endpoint:
	/sites/:siteId/datasources/:datasourceId/metrics

	View id endpoint:
	/sites/:siteId/datasources/:datasourceId/views/:viewId

	Adhoc View endpoint:
	/sites/:siteId/datasources/:datasourceId/views/adhoc

	:param resource: str, abbreviated name for requested resource
	:param required_fields: dict, typically site id, data source and view id
	:param parameters: dict, attributes, metrics, time range, etc.
	:param filters: dict, similar to parameters will act to limit fields

	"""
	resource = StringDescriptor()
	parameters = DictDescriptor()
	required_fields = DictDescriptor()
	filters = DictDescriptor()
	
	def __init__(self, resource, required_fields, parameters=None, filters=None):
		self.resource = resource
		self.required_fields = required_fields 		
		self.filters = filters if filters else {}
		self.parameters = parameters if parameters else {}

	def send(self):
		adapter = Adapter(self)
		return adapter.get()
	
	def __repr__(self):
		return '<Nanigans Prepared Request [{0}]>'.format(self.resource)
	

class Adapter(object):
	"""The '<Nanigans Adapter [Reporting API]>' object is responsible for 
	managing requests to the Nanigans API 2.0. 

	The get method is written uniquely to handle Nanigans API 2.0 success
	and error responses. This primarily means 2 things.

	Successful requests that retrieve data -- requests to the adhoc and events
	endpoints -- no date is returned. Thus, I have to add in date to each JSON object
	returned. 
	
	All requests will return an HTTP status of 200. Thus to handle errors, I have to 
	either find the error message in the response or process the request text. 

	:param PreparedRequest: list, the entities provided by the resource.

	"""
	_base_endpoint = 'https://app.nanigans.com/reporting-api/sites/{0}'
	_base_datasource_endpoint = _base_endpoint+'/datasources'
	_views_endpoint = _base_datasource_endpoint+'/{1}/views/{2}'
	_adhoc_endpoint = _base_datasource_endpoint+'/{1}/views/adhoc'
	_attrs_endpoint = _base_datasource_endpoint+'/{1}/attributes'
	_metrics_endpoint = _base_datasource_endpoint+'/{1}/metrics'
	_timeranges_endpoint = _base_datasource_endpoint+'/{1}/timeranges'
	_datasource_endpoint = _base_endpoint+'/datasources'
	_events_endpoint = _base_endpoint+'/events'

	def __init__(self, PreparedRequest):
		self._request = PreparedRequest
		self._data = []
		self._errors = []

		# Required parameters that don't need to be repeatedly called in .parameters
		self.request.parameters['access_token'] = auth.credentials['token']
		self.request.parameters['format'] = 'json' 
		if self.request.resource == 'adhoc':
			self.request.parameters['timeRange'] = 'custom'
	
	def get(self):
		resp = requests.get(url=self.endpoint, params=self.params)
		try:
			resp_json = resp.json()
		except:
			self._errors.extend([resp.text])
			return Response(self._data, self._errors)
		if resp.status_code == 200:
			if resp_json['success']:
				if self.request.resource in ('events','adhoc'):
					for item in resp_json['data']:
						item['date'] = self.params['end']
				self._data.extend(resp_json['data'])
			else:
				self._errors.extend([resp_json['error']])
		else:
			self._errors.extend([resp_json['error']])
		return Response(self._data, self._errors)
	
	@property
	def request(self):
		return self._request
	
	@property
	def endpoint(self):
		if self.request.resource == 'view':
			return self._views_endpoint.format(auth.credentials['site'],\
				self.request.required_fields['source'], self.request.required_fields['view'])
		if self.request.resource == 'adhoc':
			return self._adhoc_endpoint.format(auth.credentials['site'],\
				self.request.required_fields['source'])
		if self.request.resource == 'attributes':
			return self._attrs_endpoint.format(auth.credentials['site'],\
				self.request.required_fields['source'])
		if self.request.resource == 'metrics':
			return self._metrics_endpoint.format(auth.credentials['site'],\
				self.request.required_fields['source'])
		if self.request.resource == 'timeranges':
			return self._timeranges_endpoint.format(auth.credentials['site'],\
				self.request.required_fields['source'])
		if self.request.resource == 'datasources':
			return self._datasource_endpoint.format(auth.credentials['site'],\
				self.request.required_fields['source'])
		if self.request.resource == 'events':
			return self._events_endpoint.format(auth.credentials['site'])
		raise TypeError('Do not recognize resource.')
	
	@property
	def params(self):
		return self.request.parameters
	
	def __repr__(self):
		return '<Nanigans Adapter [Reporting API]>'


class Response(object):
    """ A '<Nanigans Response [status]>' object.

    The '<Nanigans Response [status]>' object is a carrier of information
    returned by the adapter. It should only need to be instantiated by the
    adapter.

    The object contains three attributes; data, errors and ok. The first is a
    list of entities returned by the adapter. The second is a list of failed
    requests returned while gathering the entities. The third is a boolean
    that reflects the success of the requests.

    :param data: list, the entities provided by the resource.
    :param errors: dict, any failed requests whilist gathering the resource
    entities.

    """
    data = ListDescriptor()
    errors = ListDescriptor()

    def __init__(self, data=None, errors=None):
        self.data = data if data else []
        self.errors = errors if errors else []

    @property
    def ok(self):
        if not self.errors:
            return True
        return False

    def __bool__(self):	
        return self.ok

    def __repr__(self):
        if self.ok:
            return '<Nanigans Response [OK]>'
        return '<Nanigans Response [Incomplete]>'

    def __add__(self, other):
        if not isinstance(other, Response):
            raise TypeError("Adding a non-Response to a Response is not supported")
        return Response(self.data + other.data, self.errors + other.errors)
