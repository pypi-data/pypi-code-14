# coding=utf-8
"""
This code was generated by
\ / _    _  _|   _  _
 | (_)\/(_)(_|\/| |(/_  v1.0.0
      /       /       
"""

from twilio import values
from twilio.instance_context import InstanceContext
from twilio.instance_resource import InstanceResource
from twilio.list_resource import ListResource
from twilio.page import Page


class CountryList(ListResource):

    def __init__(self, version):
        """
        Initialize the CountryList
        
        :param Version version: Version that contains the resource
        
        :returns: CountryList
        :rtype: CountryList
        """
        super(CountryList, self).__init__(version)
        
        # Path Solution
        self._solution = {}
        self._uri = '/Voice/Countries'.format(**self._solution)

    def stream(self, limit=None, page_size=None):
        """
        Streams CountryInstance records from the API as a generator stream.
        This operation lazily loads records as efficiently as possible until the limit
        is reached.
        The results are returned as a generator, so this operation is memory efficient.
        
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
            page_size=limits['page_size'],
        )
        
        return self._version.stream(page, limits['limit'], limits['page_limit'])

    def list(self, limit=None, page_size=None):
        """
        Lists CountryInstance records from the API as a list.
        Unlike stream(), this operation is eager and will load `limit` records into
        memory before returning.
        
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
            limit=limit,
            page_size=page_size,
        ))

    def page(self, page_token=values.unset, page_number=values.unset,
             page_size=values.unset):
        """
        Retrieve a single page of CountryInstance records from the API.
        Request is executed immediately
        
        :param str page_token: PageToken provided by the API
        :param int page_number: Page Number, this value is simply for client state
        :param int page_size: Number of records to return, defaults to 50
        
        :returns: Page of CountryInstance
        :rtype: Page
        """
        params = values.of({
            'PageToken': page_token,
            'Page': page_number,
            'PageSize': page_size,
        })
        
        response = self._version.page(
            'GET',
            self._uri,
            params=params,
        )
        
        return CountryPage(self._version, response, self._solution)

    def get(self, iso_country):
        """
        Constructs a CountryContext
        
        :param iso_country: The iso_country
        
        :returns: CountryContext
        :rtype: CountryContext
        """
        return CountryContext(
            self._version,
            iso_country=iso_country,
        )

    def __call__(self, iso_country):
        """
        Constructs a CountryContext
        
        :param iso_country: The iso_country
        
        :returns: CountryContext
        :rtype: CountryContext
        """
        return CountryContext(
            self._version,
            iso_country=iso_country,
        )

    def __repr__(self):
        """
        Provide a friendly representation
        
        :returns: Machine friendly representation
        :rtype: str
        """
        return '<Twilio.Pricing.V1.CountryList>'


class CountryPage(Page):

    def __init__(self, version, response, solution):
        """
        Initialize the CountryPage
        
        :param Version version: Version that contains the resource
        :param Response response: Response from the API
        
        :returns: CountryPage
        :rtype: CountryPage
        """
        super(CountryPage, self).__init__(version, response)
        
        # Path Solution
        self._solution = solution

    def get_instance(self, payload):
        """
        Build an instance of CountryInstance
        
        :param dict payload: Payload response from the API
        
        :returns: CountryInstance
        :rtype: CountryInstance
        """
        return CountryInstance(
            self._version,
            payload,
        )

    def __repr__(self):
        """
        Provide a friendly representation
        
        :returns: Machine friendly representation
        :rtype: str
        """
        return '<Twilio.Pricing.V1.CountryPage>'


class CountryContext(InstanceContext):

    def __init__(self, version, iso_country):
        """
        Initialize the CountryContext
        
        :param Version version: Version that contains the resource
        :param iso_country: The iso_country
        
        :returns: CountryContext
        :rtype: CountryContext
        """
        super(CountryContext, self).__init__(version)
        
        # Path Solution
        self._solution = {
            'iso_country': iso_country,
        }
        self._uri = '/Voice/Countries/{iso_country}'.format(**self._solution)

    def fetch(self):
        """
        Fetch a CountryInstance
        
        :returns: Fetched CountryInstance
        :rtype: CountryInstance
        """
        params = values.of({})
        
        payload = self._version.fetch(
            'GET',
            self._uri,
            params=params,
        )
        
        return CountryInstance(
            self._version,
            payload,
            iso_country=self._solution['iso_country'],
        )

    def __repr__(self):
        """
        Provide a friendly representation
        
        :returns: Machine friendly representation
        :rtype: str
        """
        context = ' '.join('{}={}'.format(k, v) for k, v in self._solution.items())
        return '<Twilio.Pricing.V1.CountryContext {}>'.format(context)


class CountryInstance(InstanceResource):

    def __init__(self, version, payload, iso_country=None):
        """
        Initialize the CountryInstance
        
        :returns: CountryInstance
        :rtype: CountryInstance
        """
        super(CountryInstance, self).__init__(version)
        
        # Marshaled Properties
        self._properties = {
            'country': payload['country'],
            'iso_country': payload['iso_country'],
            'url': payload['url'],
            'outbound_prefix_prices': payload.get('outbound_prefix_prices'),
            'inbound_call_prices': payload.get('inbound_call_prices'),
            'price_unit': payload.get('price_unit'),
        }
        
        # Context
        self._context = None
        self._solution = {
            'iso_country': iso_country or self._properties['iso_country'],
        }

    @property
    def _proxy(self):
        """
        Generate an instance context for the instance, the context is capable of
        performing various actions.  All instance actions are proxied to the context
        
        :returns: CountryContext for this CountryInstance
        :rtype: CountryContext
        """
        if self._context is None:
            self._context = CountryContext(
                self._version,
                iso_country=self._solution['iso_country'],
            )
        return self._context

    @property
    def country(self):
        """
        :returns: The country
        :rtype: unicode
        """
        return self._properties['country']

    @property
    def iso_country(self):
        """
        :returns: The iso_country
        :rtype: unicode
        """
        return self._properties['iso_country']

    @property
    def outbound_prefix_prices(self):
        """
        :returns: The outbound_prefix_prices
        :rtype: unicode
        """
        return self._properties['outbound_prefix_prices']

    @property
    def inbound_call_prices(self):
        """
        :returns: The inbound_call_prices
        :rtype: unicode
        """
        return self._properties['inbound_call_prices']

    @property
    def price_unit(self):
        """
        :returns: The price_unit
        :rtype: unicode
        """
        return self._properties['price_unit']

    @property
    def url(self):
        """
        :returns: The url
        :rtype: unicode
        """
        return self._properties['url']

    def fetch(self):
        """
        Fetch a CountryInstance
        
        :returns: Fetched CountryInstance
        :rtype: CountryInstance
        """
        return self._proxy.fetch()

    def __repr__(self):
        """
        Provide a friendly representation
        
        :returns: Machine friendly representation
        :rtype: str
        """
        context = ' '.join('{}={}'.format(k, v) for k, v in self._solution.items())
        return '<Twilio.Pricing.V1.CountryInstance {}>'.format(context)
