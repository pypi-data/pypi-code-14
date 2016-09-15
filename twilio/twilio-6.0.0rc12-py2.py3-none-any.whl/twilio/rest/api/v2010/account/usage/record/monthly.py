# coding=utf-8
"""
This code was generated by
\ / _    _  _|   _  _
 | (_)\/(_)(_|\/| |(/_  v1.0.0
      /       /       
"""

from twilio import deserialize
from twilio import serialize
from twilio import values
from twilio.instance_resource import InstanceResource
from twilio.list_resource import ListResource
from twilio.page import Page


class MonthlyList(ListResource):

    def __init__(self, version, account_sid):
        """
        Initialize the MonthlyList
        
        :param Version version: Version that contains the resource
        :param account_sid: A 34 character string that uniquely identifies this resource.
        
        :returns: MonthlyList
        :rtype: MonthlyList
        """
        super(MonthlyList, self).__init__(version)
        
        # Path Solution
        self._solution = {
            'account_sid': account_sid,
        }
        self._uri = '/Accounts/{account_sid}/Usage/Records/Monthly.json'.format(**self._solution)

    def stream(self, category=values.unset, start_date_before=values.unset,
               start_date=values.unset, start_date_after=values.unset,
               end_date_before=values.unset, end_date=values.unset,
               end_date_after=values.unset, limit=None, page_size=None):
        """
        Streams MonthlyInstance records from the API as a generator stream.
        This operation lazily loads records as efficiently as possible until the limit
        is reached.
        The results are returned as a generator, so this operation is memory efficient.
        
        :param monthly.category category: The category
        :param date start_date_before: The start_date
        :param date start_date: The start_date
        :param date start_date_after: The start_date
        :param date end_date_before: The end_date
        :param date end_date: The end_date
        :param date end_date_after: The end_date
        :param int limit: Upper limit for the number of records to return. stream()
                          guarantees to never return more than limit.  Default is no limit
        :param int page_size: Number of records to fetch per request, when not set will use
                              the default value of 50 records.  If no page_size is defined
                              but a limit is defined, stream() will attempt to read the
                              limit with the most efficient page size, i.e. min(limit, 1000)
        
        :returns: Generator that will yield up to limit results
        :rtype: generator
        """
        limits = self._version.read_limits(limit, page_size)
        
        page = self.page(
            category=category,
            start_date_before=start_date_before,
            start_date=start_date,
            start_date_after=start_date_after,
            end_date_before=end_date_before,
            end_date=end_date,
            end_date_after=end_date_after,
            page_size=limits['page_size'],
        )
        
        return self._version.stream(page, limits['limit'], limits['page_limit'])

    def list(self, category=values.unset, start_date_before=values.unset,
             start_date=values.unset, start_date_after=values.unset,
             end_date_before=values.unset, end_date=values.unset,
             end_date_after=values.unset, limit=None, page_size=None):
        """
        Lists MonthlyInstance records from the API as a list.
        Unlike stream(), this operation is eager and will load `limit` records into
        memory before returning.
        
        :param monthly.category category: The category
        :param date start_date_before: The start_date
        :param date start_date: The start_date
        :param date start_date_after: The start_date
        :param date end_date_before: The end_date
        :param date end_date: The end_date
        :param date end_date_after: The end_date
        :param int limit: Upper limit for the number of records to return. list() guarantees
                          never to return more than limit.  Default is no limit
        :param int page_size: Number of records to fetch per request, when not set will use
                              the default value of 50 records.  If no page_size is defined
                              but a limit is defined, list() will attempt to read the limit
                              with the most efficient page size, i.e. min(limit, 1000)
        
        :returns: Generator that will yield up to limit results
        :rtype: generator
        """
        return list(self.stream(
            category=category,
            start_date_before=start_date_before,
            start_date=start_date,
            start_date_after=start_date_after,
            end_date_before=end_date_before,
            end_date=end_date,
            end_date_after=end_date_after,
            limit=limit,
            page_size=page_size,
        ))

    def page(self, category=values.unset, start_date_before=values.unset,
             start_date=values.unset, start_date_after=values.unset,
             end_date_before=values.unset, end_date=values.unset,
             end_date_after=values.unset, page_token=values.unset,
             page_number=values.unset, page_size=values.unset):
        """
        Retrieve a single page of MonthlyInstance records from the API.
        Request is executed immediately
        
        :param monthly.category category: The category
        :param date start_date_before: The start_date
        :param date start_date: The start_date
        :param date start_date_after: The start_date
        :param date end_date_before: The end_date
        :param date end_date: The end_date
        :param date end_date_after: The end_date
        :param str page_token: PageToken provided by the API
        :param int page_number: Page Number, this value is simply for client state
        :param int page_size: Number of records to return, defaults to 50
        
        :returns: Page of MonthlyInstance
        :rtype: Page
        """
        params = values.of({
            'Category': category,
            'StartDate<': serialize.iso8601_date(start_date_before),
            'StartDate': serialize.iso8601_date(start_date),
            'StartDate>': serialize.iso8601_date(start_date_after),
            'EndDate<': serialize.iso8601_date(end_date_before),
            'EndDate': serialize.iso8601_date(end_date),
            'EndDate>': serialize.iso8601_date(end_date_after),
            'PageToken': page_token,
            'Page': page_number,
            'PageSize': page_size,
        })
        
        response = self._version.page(
            'GET',
            self._uri,
            params=params,
        )
        
        return MonthlyPage(self._version, response, self._solution)

    def __repr__(self):
        """
        Provide a friendly representation
        
        :returns: Machine friendly representation
        :rtype: str
        """
        return '<Twilio.Api.V2010.MonthlyList>'


class MonthlyPage(Page):

    def __init__(self, version, response, solution):
        """
        Initialize the MonthlyPage
        
        :param Version version: Version that contains the resource
        :param Response response: Response from the API
        :param account_sid: A 34 character string that uniquely identifies this resource.
        
        :returns: MonthlyPage
        :rtype: MonthlyPage
        """
        super(MonthlyPage, self).__init__(version, response)
        
        # Path Solution
        self._solution = solution

    def get_instance(self, payload):
        """
        Build an instance of MonthlyInstance
        
        :param dict payload: Payload response from the API
        
        :returns: MonthlyInstance
        :rtype: MonthlyInstance
        """
        return MonthlyInstance(
            self._version,
            payload,
            account_sid=self._solution['account_sid'],
        )

    def __repr__(self):
        """
        Provide a friendly representation
        
        :returns: Machine friendly representation
        :rtype: str
        """
        return '<Twilio.Api.V2010.MonthlyPage>'


class MonthlyInstance(InstanceResource):

    def __init__(self, version, payload, account_sid):
        """
        Initialize the MonthlyInstance
        
        :returns: MonthlyInstance
        :rtype: MonthlyInstance
        """
        super(MonthlyInstance, self).__init__(version)
        
        # Marshaled Properties
        self._properties = {
            'account_sid': payload['account_sid'],
            'api_version': payload['api_version'],
            'category': payload['category'],
            'count': payload['count'],
            'count_unit': payload['count_unit'],
            'description': payload['description'],
            'end_date': deserialize.iso8601_datetime(payload['end_date']),
            'price': deserialize.decimal(payload['price']),
            'price_unit': payload['price_unit'],
            'start_date': deserialize.iso8601_datetime(payload['start_date']),
            'subresource_uris': payload['subresource_uris'],
            'uri': payload['uri'],
            'usage': payload['usage'],
            'usage_unit': payload['usage_unit'],
        }
        
        # Context
        self._context = None
        self._solution = {
            'account_sid': account_sid,
        }

    @property
    def account_sid(self):
        """
        :returns: The account_sid
        :rtype: unicode
        """
        return self._properties['account_sid']

    @property
    def api_version(self):
        """
        :returns: The api_version
        :rtype: unicode
        """
        return self._properties['api_version']

    @property
    def category(self):
        """
        :returns: The category
        :rtype: monthly.category
        """
        return self._properties['category']

    @property
    def count(self):
        """
        :returns: The count
        :rtype: unicode
        """
        return self._properties['count']

    @property
    def count_unit(self):
        """
        :returns: The count_unit
        :rtype: unicode
        """
        return self._properties['count_unit']

    @property
    def description(self):
        """
        :returns: The description
        :rtype: unicode
        """
        return self._properties['description']

    @property
    def end_date(self):
        """
        :returns: The end_date
        :rtype: datetime
        """
        return self._properties['end_date']

    @property
    def price(self):
        """
        :returns: The price
        :rtype: unicode
        """
        return self._properties['price']

    @property
    def price_unit(self):
        """
        :returns: The price_unit
        :rtype: unicode
        """
        return self._properties['price_unit']

    @property
    def start_date(self):
        """
        :returns: The start_date
        :rtype: datetime
        """
        return self._properties['start_date']

    @property
    def subresource_uris(self):
        """
        :returns: The subresource_uris
        :rtype: unicode
        """
        return self._properties['subresource_uris']

    @property
    def uri(self):
        """
        :returns: The uri
        :rtype: unicode
        """
        return self._properties['uri']

    @property
    def usage(self):
        """
        :returns: The usage
        :rtype: unicode
        """
        return self._properties['usage']

    @property
    def usage_unit(self):
        """
        :returns: The usage_unit
        :rtype: unicode
        """
        return self._properties['usage_unit']

    def __repr__(self):
        """
        Provide a friendly representation
        
        :returns: Machine friendly representation
        :rtype: str
        """
        return '<Twilio.Api.V2010.MonthlyInstance>'
