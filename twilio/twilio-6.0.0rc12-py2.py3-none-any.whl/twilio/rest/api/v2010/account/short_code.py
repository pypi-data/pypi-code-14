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


class ShortCodeList(ListResource):

    def __init__(self, version, account_sid):
        """
        Initialize the ShortCodeList
        
        :param Version version: Version that contains the resource
        :param account_sid: The unique sid that identifies this account
        
        :returns: ShortCodeList
        :rtype: ShortCodeList
        """
        super(ShortCodeList, self).__init__(version)
        
        # Path Solution
        self._solution = {
            'account_sid': account_sid,
        }
        self._uri = '/Accounts/{account_sid}/SMS/ShortCodes.json'.format(**self._solution)

    def stream(self, friendly_name=values.unset, short_code=values.unset,
               limit=None, page_size=None):
        """
        Streams ShortCodeInstance records from the API as a generator stream.
        This operation lazily loads records as efficiently as possible until the limit
        is reached.
        The results are returned as a generator, so this operation is memory efficient.
        
        :param unicode friendly_name: Filter by friendly name
        :param unicode short_code: Filter by ShortCode
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
            friendly_name=friendly_name,
            short_code=short_code,
            page_size=limits['page_size'],
        )
        
        return self._version.stream(page, limits['limit'], limits['page_limit'])

    def list(self, friendly_name=values.unset, short_code=values.unset, limit=None,
             page_size=None):
        """
        Lists ShortCodeInstance records from the API as a list.
        Unlike stream(), this operation is eager and will load `limit` records into
        memory before returning.
        
        :param unicode friendly_name: Filter by friendly name
        :param unicode short_code: Filter by ShortCode
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
            friendly_name=friendly_name,
            short_code=short_code,
            limit=limit,
            page_size=page_size,
        ))

    def page(self, friendly_name=values.unset, short_code=values.unset,
             page_token=values.unset, page_number=values.unset,
             page_size=values.unset):
        """
        Retrieve a single page of ShortCodeInstance records from the API.
        Request is executed immediately
        
        :param unicode friendly_name: Filter by friendly name
        :param unicode short_code: Filter by ShortCode
        :param str page_token: PageToken provided by the API
        :param int page_number: Page Number, this value is simply for client state
        :param int page_size: Number of records to return, defaults to 50
        
        :returns: Page of ShortCodeInstance
        :rtype: Page
        """
        params = values.of({
            'FriendlyName': friendly_name,
            'ShortCode': short_code,
            'PageToken': page_token,
            'Page': page_number,
            'PageSize': page_size,
        })
        
        response = self._version.page(
            'GET',
            self._uri,
            params=params,
        )
        
        return ShortCodePage(self._version, response, self._solution)

    def get(self, sid):
        """
        Constructs a ShortCodeContext
        
        :param sid: Fetch by unique short-code Sid
        
        :returns: ShortCodeContext
        :rtype: ShortCodeContext
        """
        return ShortCodeContext(
            self._version,
            account_sid=self._solution['account_sid'],
            sid=sid,
        )

    def __call__(self, sid):
        """
        Constructs a ShortCodeContext
        
        :param sid: Fetch by unique short-code Sid
        
        :returns: ShortCodeContext
        :rtype: ShortCodeContext
        """
        return ShortCodeContext(
            self._version,
            account_sid=self._solution['account_sid'],
            sid=sid,
        )

    def __repr__(self):
        """
        Provide a friendly representation
        
        :returns: Machine friendly representation
        :rtype: str
        """
        return '<Twilio.Api.V2010.ShortCodeList>'


class ShortCodePage(Page):

    def __init__(self, version, response, solution):
        """
        Initialize the ShortCodePage
        
        :param Version version: Version that contains the resource
        :param Response response: Response from the API
        :param account_sid: The unique sid that identifies this account
        
        :returns: ShortCodePage
        :rtype: ShortCodePage
        """
        super(ShortCodePage, self).__init__(version, response)
        
        # Path Solution
        self._solution = solution

    def get_instance(self, payload):
        """
        Build an instance of ShortCodeInstance
        
        :param dict payload: Payload response from the API
        
        :returns: ShortCodeInstance
        :rtype: ShortCodeInstance
        """
        return ShortCodeInstance(
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
        return '<Twilio.Api.V2010.ShortCodePage>'


class ShortCodeContext(InstanceContext):

    def __init__(self, version, account_sid, sid):
        """
        Initialize the ShortCodeContext
        
        :param Version version: Version that contains the resource
        :param account_sid: The account_sid
        :param sid: Fetch by unique short-code Sid
        
        :returns: ShortCodeContext
        :rtype: ShortCodeContext
        """
        super(ShortCodeContext, self).__init__(version)
        
        # Path Solution
        self._solution = {
            'account_sid': account_sid,
            'sid': sid,
        }
        self._uri = '/Accounts/{account_sid}/SMS/ShortCodes/{sid}.json'.format(**self._solution)

    def fetch(self):
        """
        Fetch a ShortCodeInstance
        
        :returns: Fetched ShortCodeInstance
        :rtype: ShortCodeInstance
        """
        params = values.of({})
        
        payload = self._version.fetch(
            'GET',
            self._uri,
            params=params,
        )
        
        return ShortCodeInstance(
            self._version,
            payload,
            account_sid=self._solution['account_sid'],
            sid=self._solution['sid'],
        )

    def update(self, friendly_name=values.unset, api_version=values.unset,
               sms_url=values.unset, sms_method=values.unset,
               sms_fallback_url=values.unset, sms_fallback_method=values.unset):
        """
        Update the ShortCodeInstance
        
        :param unicode friendly_name: A human readable description of this resource
        :param unicode api_version: The API version to use
        :param unicode sms_url: URL Twilio will request when receiving an SMS
        :param unicode sms_method: HTTP method to use when requesting the sms url
        :param unicode sms_fallback_url: URL Twilio will request if an error occurs in executing TwiML
        :param unicode sms_fallback_method: HTTP method Twilio will use with sms fallback url
        
        :returns: Updated ShortCodeInstance
        :rtype: ShortCodeInstance
        """
        data = values.of({
            'FriendlyName': friendly_name,
            'ApiVersion': api_version,
            'SmsUrl': sms_url,
            'SmsMethod': sms_method,
            'SmsFallbackUrl': sms_fallback_url,
            'SmsFallbackMethod': sms_fallback_method,
        })
        
        payload = self._version.update(
            'POST',
            self._uri,
            data=data,
        )
        
        return ShortCodeInstance(
            self._version,
            payload,
            account_sid=self._solution['account_sid'],
            sid=self._solution['sid'],
        )

    def __repr__(self):
        """
        Provide a friendly representation
        
        :returns: Machine friendly representation
        :rtype: str
        """
        context = ' '.join('{}={}'.format(k, v) for k, v in self._solution.items())
        return '<Twilio.Api.V2010.ShortCodeContext {}>'.format(context)


class ShortCodeInstance(InstanceResource):

    def __init__(self, version, payload, account_sid, sid=None):
        """
        Initialize the ShortCodeInstance
        
        :returns: ShortCodeInstance
        :rtype: ShortCodeInstance
        """
        super(ShortCodeInstance, self).__init__(version)
        
        # Marshaled Properties
        self._properties = {
            'account_sid': payload['account_sid'],
            'api_version': payload['api_version'],
            'date_created': deserialize.rfc2822_datetime(payload['date_created']),
            'date_updated': deserialize.rfc2822_datetime(payload['date_updated']),
            'friendly_name': payload['friendly_name'],
            'short_code': payload['short_code'],
            'sid': payload['sid'],
            'sms_fallback_method': payload['sms_fallback_method'],
            'sms_fallback_url': payload['sms_fallback_url'],
            'sms_method': payload['sms_method'],
            'sms_url': payload['sms_url'],
            'uri': payload['uri'],
        }
        
        # Context
        self._context = None
        self._solution = {
            'account_sid': account_sid,
            'sid': sid or self._properties['sid'],
        }

    @property
    def _proxy(self):
        """
        Generate an instance context for the instance, the context is capable of
        performing various actions.  All instance actions are proxied to the context
        
        :returns: ShortCodeContext for this ShortCodeInstance
        :rtype: ShortCodeContext
        """
        if self._context is None:
            self._context = ShortCodeContext(
                self._version,
                account_sid=self._solution['account_sid'],
                sid=self._solution['sid'],
            )
        return self._context

    @property
    def account_sid(self):
        """
        :returns: The unique sid that identifies this account
        :rtype: unicode
        """
        return self._properties['account_sid']

    @property
    def api_version(self):
        """
        :returns: The API version to use
        :rtype: unicode
        """
        return self._properties['api_version']

    @property
    def date_created(self):
        """
        :returns: The date this resource was created
        :rtype: datetime
        """
        return self._properties['date_created']

    @property
    def date_updated(self):
        """
        :returns: The date this resource was last updated
        :rtype: datetime
        """
        return self._properties['date_updated']

    @property
    def friendly_name(self):
        """
        :returns: A human readable description of this resource
        :rtype: unicode
        """
        return self._properties['friendly_name']

    @property
    def short_code(self):
        """
        :returns: The short code. e.g., 894546.
        :rtype: unicode
        """
        return self._properties['short_code']

    @property
    def sid(self):
        """
        :returns: A string that uniquely identifies this short-codes
        :rtype: unicode
        """
        return self._properties['sid']

    @property
    def sms_fallback_method(self):
        """
        :returns: HTTP method Twilio will use with sms fallback url
        :rtype: unicode
        """
        return self._properties['sms_fallback_method']

    @property
    def sms_fallback_url(self):
        """
        :returns: URL Twilio will request if an error occurs in executing TwiML
        :rtype: unicode
        """
        return self._properties['sms_fallback_url']

    @property
    def sms_method(self):
        """
        :returns: HTTP method to use when requesting the sms url
        :rtype: unicode
        """
        return self._properties['sms_method']

    @property
    def sms_url(self):
        """
        :returns: URL Twilio will request when receiving an SMS
        :rtype: unicode
        """
        return self._properties['sms_url']

    @property
    def uri(self):
        """
        :returns: The URI for this resource
        :rtype: unicode
        """
        return self._properties['uri']

    def fetch(self):
        """
        Fetch a ShortCodeInstance
        
        :returns: Fetched ShortCodeInstance
        :rtype: ShortCodeInstance
        """
        return self._proxy.fetch()

    def update(self, friendly_name=values.unset, api_version=values.unset,
               sms_url=values.unset, sms_method=values.unset,
               sms_fallback_url=values.unset, sms_fallback_method=values.unset):
        """
        Update the ShortCodeInstance
        
        :param unicode friendly_name: A human readable description of this resource
        :param unicode api_version: The API version to use
        :param unicode sms_url: URL Twilio will request when receiving an SMS
        :param unicode sms_method: HTTP method to use when requesting the sms url
        :param unicode sms_fallback_url: URL Twilio will request if an error occurs in executing TwiML
        :param unicode sms_fallback_method: HTTP method Twilio will use with sms fallback url
        
        :returns: Updated ShortCodeInstance
        :rtype: ShortCodeInstance
        """
        return self._proxy.update(
            friendly_name=friendly_name,
            api_version=api_version,
            sms_url=sms_url,
            sms_method=sms_method,
            sms_fallback_url=sms_fallback_url,
            sms_fallback_method=sms_fallback_method,
        )

    def __repr__(self):
        """
        Provide a friendly representation
        
        :returns: Machine friendly representation
        :rtype: str
        """
        context = ' '.join('{}={}'.format(k, v) for k, v in self._solution.items())
        return '<Twilio.Api.V2010.ShortCodeInstance {}>'.format(context)
