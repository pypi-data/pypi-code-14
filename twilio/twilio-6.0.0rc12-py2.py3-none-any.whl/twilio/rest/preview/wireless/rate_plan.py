# coding=utf-8
"""
This code was generated by
\ / _    _  _|   _  _
 | (_)\/(_)(_|\/| |(/_  v1.0.0
      /       /       
"""

from twilio import deserialize
from twilio import values
from twilio.instance_context import InstanceContext
from twilio.instance_resource import InstanceResource
from twilio.list_resource import ListResource
from twilio.page import Page


class RatePlanList(ListResource):

    def __init__(self, version):
        """
        Initialize the RatePlanList
        
        :param Version version: Version that contains the resource
        
        :returns: RatePlanList
        :rtype: RatePlanList
        """
        super(RatePlanList, self).__init__(version)
        
        # Path Solution
        self._solution = {}
        self._uri = '/RatePlans'.format(**self._solution)

    def stream(self, limit=None, page_size=None):
        """
        Streams RatePlanInstance records from the API as a generator stream.
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
        Lists RatePlanInstance records from the API as a list.
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
        Retrieve a single page of RatePlanInstance records from the API.
        Request is executed immediately
        
        :param str page_token: PageToken provided by the API
        :param int page_number: Page Number, this value is simply for client state
        :param int page_size: Number of records to return, defaults to 50
        
        :returns: Page of RatePlanInstance
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
        
        return RatePlanPage(self._version, response, self._solution)

    def get(self, sid):
        """
        Constructs a RatePlanContext
        
        :param sid: The sid
        
        :returns: RatePlanContext
        :rtype: RatePlanContext
        """
        return RatePlanContext(
            self._version,
            sid=sid,
        )

    def __call__(self, sid):
        """
        Constructs a RatePlanContext
        
        :param sid: The sid
        
        :returns: RatePlanContext
        :rtype: RatePlanContext
        """
        return RatePlanContext(
            self._version,
            sid=sid,
        )

    def __repr__(self):
        """
        Provide a friendly representation
        
        :returns: Machine friendly representation
        :rtype: str
        """
        return '<Twilio.Preview.Wireless.RatePlanList>'


class RatePlanPage(Page):

    def __init__(self, version, response, solution):
        """
        Initialize the RatePlanPage
        
        :param Version version: Version that contains the resource
        :param Response response: Response from the API
        
        :returns: RatePlanPage
        :rtype: RatePlanPage
        """
        super(RatePlanPage, self).__init__(version, response)
        
        # Path Solution
        self._solution = solution

    def get_instance(self, payload):
        """
        Build an instance of RatePlanInstance
        
        :param dict payload: Payload response from the API
        
        :returns: RatePlanInstance
        :rtype: RatePlanInstance
        """
        return RatePlanInstance(
            self._version,
            payload,
        )

    def __repr__(self):
        """
        Provide a friendly representation
        
        :returns: Machine friendly representation
        :rtype: str
        """
        return '<Twilio.Preview.Wireless.RatePlanPage>'


class RatePlanContext(InstanceContext):

    def __init__(self, version, sid):
        """
        Initialize the RatePlanContext
        
        :param Version version: Version that contains the resource
        :param sid: The sid
        
        :returns: RatePlanContext
        :rtype: RatePlanContext
        """
        super(RatePlanContext, self).__init__(version)
        
        # Path Solution
        self._solution = {
            'sid': sid,
        }
        self._uri = '/RatePlans/{sid}'.format(**self._solution)

    def fetch(self):
        """
        Fetch a RatePlanInstance
        
        :returns: Fetched RatePlanInstance
        :rtype: RatePlanInstance
        """
        params = values.of({})
        
        payload = self._version.fetch(
            'GET',
            self._uri,
            params=params,
        )
        
        return RatePlanInstance(
            self._version,
            payload,
            sid=self._solution['sid'],
        )

    def __repr__(self):
        """
        Provide a friendly representation
        
        :returns: Machine friendly representation
        :rtype: str
        """
        context = ' '.join('{}={}'.format(k, v) for k, v in self._solution.items())
        return '<Twilio.Preview.Wireless.RatePlanContext {}>'.format(context)


class RatePlanInstance(InstanceResource):

    def __init__(self, version, payload, sid=None):
        """
        Initialize the RatePlanInstance
        
        :returns: RatePlanInstance
        :rtype: RatePlanInstance
        """
        super(RatePlanInstance, self).__init__(version)
        
        # Marshaled Properties
        self._properties = {
            'sid': payload['sid'],
            'alias': payload['alias'],
            'account_sid': payload['account_sid'],
            'friendly_name': payload['friendly_name'],
            'data_metering': payload['data_metering'],
            'capabilities': payload['capabilities'],
            'voice_cap': deserialize.integer(payload['voice_cap']),
            'messaging_cap': deserialize.integer(payload['messaging_cap']),
            'commands_cap': deserialize.integer(payload['commands_cap']),
            'data_cap': deserialize.integer(payload['data_cap']),
            'cap_period': deserialize.integer(payload['cap_period']),
            'cap_unit': payload['cap_unit'],
            'date_created': deserialize.iso8601_datetime(payload['date_created']),
            'date_updated': deserialize.iso8601_datetime(payload['date_updated']),
            'url': payload['url'],
        }
        
        # Context
        self._context = None
        self._solution = {
            'sid': sid or self._properties['sid'],
        }

    @property
    def _proxy(self):
        """
        Generate an instance context for the instance, the context is capable of
        performing various actions.  All instance actions are proxied to the context
        
        :returns: RatePlanContext for this RatePlanInstance
        :rtype: RatePlanContext
        """
        if self._context is None:
            self._context = RatePlanContext(
                self._version,
                sid=self._solution['sid'],
            )
        return self._context

    @property
    def sid(self):
        """
        :returns: The sid
        :rtype: unicode
        """
        return self._properties['sid']

    @property
    def alias(self):
        """
        :returns: The alias
        :rtype: unicode
        """
        return self._properties['alias']

    @property
    def account_sid(self):
        """
        :returns: The account_sid
        :rtype: unicode
        """
        return self._properties['account_sid']

    @property
    def friendly_name(self):
        """
        :returns: The friendly_name
        :rtype: unicode
        """
        return self._properties['friendly_name']

    @property
    def data_metering(self):
        """
        :returns: The data_metering
        :rtype: unicode
        """
        return self._properties['data_metering']

    @property
    def capabilities(self):
        """
        :returns: The capabilities
        :rtype: dict
        """
        return self._properties['capabilities']

    @property
    def voice_cap(self):
        """
        :returns: The voice_cap
        :rtype: unicode
        """
        return self._properties['voice_cap']

    @property
    def messaging_cap(self):
        """
        :returns: The messaging_cap
        :rtype: unicode
        """
        return self._properties['messaging_cap']

    @property
    def commands_cap(self):
        """
        :returns: The commands_cap
        :rtype: unicode
        """
        return self._properties['commands_cap']

    @property
    def data_cap(self):
        """
        :returns: The data_cap
        :rtype: unicode
        """
        return self._properties['data_cap']

    @property
    def cap_period(self):
        """
        :returns: The cap_period
        :rtype: unicode
        """
        return self._properties['cap_period']

    @property
    def cap_unit(self):
        """
        :returns: The cap_unit
        :rtype: unicode
        """
        return self._properties['cap_unit']

    @property
    def date_created(self):
        """
        :returns: The date_created
        :rtype: datetime
        """
        return self._properties['date_created']

    @property
    def date_updated(self):
        """
        :returns: The date_updated
        :rtype: datetime
        """
        return self._properties['date_updated']

    @property
    def url(self):
        """
        :returns: The url
        :rtype: unicode
        """
        return self._properties['url']

    def fetch(self):
        """
        Fetch a RatePlanInstance
        
        :returns: Fetched RatePlanInstance
        :rtype: RatePlanInstance
        """
        return self._proxy.fetch()

    def __repr__(self):
        """
        Provide a friendly representation
        
        :returns: Machine friendly representation
        :rtype: str
        """
        context = ' '.join('{}={}'.format(k, v) for k, v in self._solution.items())
        return '<Twilio.Preview.Wireless.RatePlanInstance {}>'.format(context)
