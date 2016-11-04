"""
The multichannel module contains the core functions used to retrieve multi-channel data
(e.g. Twitter, Instagram, Facebook):

	.get_timeranges:: used to retrieve built-in time range for data sources
	.get_attributes:: used to retrieve all dimensions available for data source
	.get_metrics:: used to retrieve all metrics available for data source
	.get_view:: used to retrieve a specific view created in the Nanigans interface
	.get_stats:: used to retrieve data for user-defined queries

"""
from datetime import date, timedelta
from nanigans.utils import generate_dates
from nanigans.models import PreparedRequest, Response

def get_timeranges():
	"""Retrieves available time ranges for given data source.

	Endpoint:
	/sites/:siteId/datasources/componentplacements/timeRanges
	"""
	required_fields = {'source':'componentplacements'}
	response = PreparedRequest('timeranges', required_fields).send()

	return response

def get_attributes():
	"""Retrieves available attributes for given data source.

	Endpoint:
	/sites/:siteId/datasources/componentplacements/attributes
	"""
	required_fields = {'source':'componentplacements'}
	response = PreparedRequest('attributes', required_fields).send()

	return response

def get_metrics():
	"""Retrieves available metrics for given data source.

	Endpoint:
	/sites/:siteId/datasources/componentplacements/metrics
	"""
	required_fields = {'source':'componentplacements'}
	response = PreparedRequest('metrics', required_fields).send()

	return response

def get_view(view, depth=0):
	"""Retrieves data for a specific view id. 

	Endpoint:
	/sites/:siteId/datasources/componentplacements/views/:viewId
	:param view: str, view id of created view
	:param depth: int, dimensions depth of data
	"""
	required_fields = {'source':'componentplacements','view':view}
	parameters = {'depth':depth}
	response = PreparedRequest('view', required_fields, parameters).send()

	# Remove commas from fbSpend value

	if response.ok: 
		if response.data[0].get('fbSpend'): 
			for record in response.data:
				record['fbSpend'] = record['fbSpend'].replace(',','')
		
	return response

def get_stats(attributes=None, metrics=None, start=None, end=None, depth=0):
	"""Retrieves specific data requested given set of parameters.

	Endpoint:
	/sites/:siteId/datasources/componentplacements/views/adhoc
	
	:param attributes: list/str, attributes fields 
	:param metrics: list/str, metrics fields
	:param start: str, start date in %Y-%m-%d format 
	:param end: str, end date in %Y-%m-%d format
	:param depth: int, dimensions depth of data
	"""
	if isinstance(metrics, str):
		metrics = [metrics]
	if not metrics:
		metrics = ['impressions','clicks','fbSpend']
	if isinstance(attributes, str):
		attributes = [attributes]
	if not attributes:
		attributes = ['budgetPool','strategyGroup','adPlan']

	if start == None or end == None:
		start = (date.today()-timedelta(days=7)).strftime('%Y-%m-%d')
		end = (date.today()-timedelta(days=1)).strftime('%Y-%m-%d')

	dates = generate_dates(start,end)
	response = Response()
	required_fields = {'source':'componentplacements'}

	for day in dates:
		parameters = {'metrics[]=':metrics,
					  'attributes[]=':attributes,
					  'start':day,
					  'end':day,
					  'depth':depth}
		request = PreparedRequest('adhoc', required_fields, parameters)
		record = request.send()

		# Remove commas from fbSpend value
		if record.ok:
			for item in record.data:
				if item.get('fbSpend'):
					item['fbSpend'] = item['fbSpend'].replace(',','')
		response += record
		if response.errors:
			break

	return response 










