"""
The events module contains 2 functions to access event data:

	.get_time_of_click:: retrieves event level data attributed to time of click
	.get_time_of_conversion:: retrieves event level data attributed to time of conversion

"""
from datetime import date, timedelta
from nanigans.utils import generate_dates
from nanigans.models import PreparedRequest, Response

def get_time_of_click(fields=None, start=None, end=None):
	"""Retrieves specific events given set of parameters. The events 
	are attributed to the time of click.

	Endpoint:
	/sites/:siteId/events
	
	:param metrics: list/str, metrics fields
	:param start: str, start date in %Y-%m-%d format 
	:param end: str, end date in %Y-%m-%d format 
	"""
	if isinstance(fields, str):
		fields = [fields]

	if not fields:
		fields = ['client_user_id,','placement_id', 'placement_datetime']

	if start == None or end == None:
		start = (date.today()-timedelta(days=7)).strftime('%Y-%m-%d')
		end = (date.today()-timedelta(days=1)).strftime('%Y-%m-%d')

	dates = generate_dates(start,end)
	response = Response()
	required_fields = {'attribution':'click'}

	for day in dates:
		parameters = {'fields[]=':fields,'date':day}
		request = PreparedRequest('events', required_fields, parameters)
		record = request.send()

		response += record
		if response.errors:
			break

	return response 


def get_time_of_conversion(fields=None, start=None, end=None):
	"""Retrieves specific events given set of parameters. The events 
	are attributed to the time of conversion.

	Endpoint:
	/sites/:siteId/events
	
	:param metrics: list/str, metrics fields
	:param start: str, start date in %Y-%m-%d format 
	:param end: str, end date in %Y-%m-%d format 
	"""
	if isinstance(fields, str):
		fields = [fields]

	if not fields:
		fields = ['client_user_id,','placement_id', 'placement_datetime']

	if start == None or end == None:
		start = (date.today()-timedelta(days=7)).strftime('%Y-%m-%d')
		end = (date.today()-timedelta(days=1)).strftime('%Y-%m-%d')

	dates = generate_dates(start,end)
	response = Response()
	required_fields = {'attribution':'conversion'}

	for day in dates:
		parameters = {'fields[]=':fields,'date':day}
		request = PreparedRequest('events', required_fields, parameters)
		record = request.send()

		response += record
		if response.errors:
			break

	return response 




