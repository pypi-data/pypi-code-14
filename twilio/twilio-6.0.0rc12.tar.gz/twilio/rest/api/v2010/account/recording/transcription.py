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


class TranscriptionList(ListResource):

    def __init__(self, version, account_sid, recording_sid):
        """
        Initialize the TranscriptionList
        
        :param Version version: Version that contains the resource
        :param account_sid: The account_sid
        :param recording_sid: The recording_sid
        
        :returns: TranscriptionList
        :rtype: TranscriptionList
        """
        super(TranscriptionList, self).__init__(version)
        
        # Path Solution
        self._solution = {
            'account_sid': account_sid,
            'recording_sid': recording_sid,
        }
        self._uri = '/Accounts/{account_sid}/Recordings/{recording_sid}/Transcriptions.json'.format(**self._solution)

    def stream(self, limit=None, page_size=None):
        """
        Streams TranscriptionInstance records from the API as a generator stream.
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
        Lists TranscriptionInstance records from the API as a list.
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
        Retrieve a single page of TranscriptionInstance records from the API.
        Request is executed immediately
        
        :param str page_token: PageToken provided by the API
        :param int page_number: Page Number, this value is simply for client state
        :param int page_size: Number of records to return, defaults to 50
        
        :returns: Page of TranscriptionInstance
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
        
        return TranscriptionPage(self._version, response, self._solution)

    def get(self, sid):
        """
        Constructs a TranscriptionContext
        
        :param sid: The sid
        
        :returns: TranscriptionContext
        :rtype: TranscriptionContext
        """
        return TranscriptionContext(
            self._version,
            account_sid=self._solution['account_sid'],
            recording_sid=self._solution['recording_sid'],
            sid=sid,
        )

    def __call__(self, sid):
        """
        Constructs a TranscriptionContext
        
        :param sid: The sid
        
        :returns: TranscriptionContext
        :rtype: TranscriptionContext
        """
        return TranscriptionContext(
            self._version,
            account_sid=self._solution['account_sid'],
            recording_sid=self._solution['recording_sid'],
            sid=sid,
        )

    def __repr__(self):
        """
        Provide a friendly representation
        
        :returns: Machine friendly representation
        :rtype: str
        """
        return '<Twilio.Api.V2010.TranscriptionList>'


class TranscriptionPage(Page):

    def __init__(self, version, response, solution):
        """
        Initialize the TranscriptionPage
        
        :param Version version: Version that contains the resource
        :param Response response: Response from the API
        :param account_sid: The account_sid
        :param recording_sid: The recording_sid
        
        :returns: TranscriptionPage
        :rtype: TranscriptionPage
        """
        super(TranscriptionPage, self).__init__(version, response)
        
        # Path Solution
        self._solution = solution

    def get_instance(self, payload):
        """
        Build an instance of TranscriptionInstance
        
        :param dict payload: Payload response from the API
        
        :returns: TranscriptionInstance
        :rtype: TranscriptionInstance
        """
        return TranscriptionInstance(
            self._version,
            payload,
            account_sid=self._solution['account_sid'],
            recording_sid=self._solution['recording_sid'],
        )

    def __repr__(self):
        """
        Provide a friendly representation
        
        :returns: Machine friendly representation
        :rtype: str
        """
        return '<Twilio.Api.V2010.TranscriptionPage>'


class TranscriptionContext(InstanceContext):

    def __init__(self, version, account_sid, recording_sid, sid):
        """
        Initialize the TranscriptionContext
        
        :param Version version: Version that contains the resource
        :param account_sid: The account_sid
        :param recording_sid: The recording_sid
        :param sid: The sid
        
        :returns: TranscriptionContext
        :rtype: TranscriptionContext
        """
        super(TranscriptionContext, self).__init__(version)
        
        # Path Solution
        self._solution = {
            'account_sid': account_sid,
            'recording_sid': recording_sid,
            'sid': sid,
        }
        self._uri = '/Accounts/{account_sid}/Recordings/{recording_sid}/Transcriptions/{sid}.json'.format(**self._solution)

    def fetch(self):
        """
        Fetch a TranscriptionInstance
        
        :returns: Fetched TranscriptionInstance
        :rtype: TranscriptionInstance
        """
        params = values.of({})
        
        payload = self._version.fetch(
            'GET',
            self._uri,
            params=params,
        )
        
        return TranscriptionInstance(
            self._version,
            payload,
            account_sid=self._solution['account_sid'],
            recording_sid=self._solution['recording_sid'],
            sid=self._solution['sid'],
        )

    def delete(self):
        """
        Deletes the TranscriptionInstance
        
        :returns: True if delete succeeds, False otherwise
        :rtype: bool
        """
        return self._version.delete('delete', self._uri)

    def __repr__(self):
        """
        Provide a friendly representation
        
        :returns: Machine friendly representation
        :rtype: str
        """
        context = ' '.join('{}={}'.format(k, v) for k, v in self._solution.items())
        return '<Twilio.Api.V2010.TranscriptionContext {}>'.format(context)


class TranscriptionInstance(InstanceResource):

    def __init__(self, version, payload, account_sid, recording_sid, sid=None):
        """
        Initialize the TranscriptionInstance
        
        :returns: TranscriptionInstance
        :rtype: TranscriptionInstance
        """
        super(TranscriptionInstance, self).__init__(version)
        
        # Marshaled Properties
        self._properties = {
            'account_sid': payload['account_sid'],
            'api_version': payload['api_version'],
            'date_created': deserialize.rfc2822_datetime(payload['date_created']),
            'date_updated': deserialize.rfc2822_datetime(payload['date_updated']),
            'duration': payload['duration'],
            'price': deserialize.decimal(payload['price']),
            'price_unit': payload['price_unit'],
            'recording_sid': payload['recording_sid'],
            'sid': payload['sid'],
            'status': payload['status'],
            'transcription_text': payload['transcription_text'],
            'type': payload['type'],
            'uri': payload['uri'],
        }
        
        # Context
        self._context = None
        self._solution = {
            'account_sid': account_sid,
            'recording_sid': recording_sid,
            'sid': sid or self._properties['sid'],
        }

    @property
    def _proxy(self):
        """
        Generate an instance context for the instance, the context is capable of
        performing various actions.  All instance actions are proxied to the context
        
        :returns: TranscriptionContext for this TranscriptionInstance
        :rtype: TranscriptionContext
        """
        if self._context is None:
            self._context = TranscriptionContext(
                self._version,
                account_sid=self._solution['account_sid'],
                recording_sid=self._solution['recording_sid'],
                sid=self._solution['sid'],
            )
        return self._context

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
    def duration(self):
        """
        :returns: The duration
        :rtype: unicode
        """
        return self._properties['duration']

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
    def recording_sid(self):
        """
        :returns: The recording_sid
        :rtype: unicode
        """
        return self._properties['recording_sid']

    @property
    def sid(self):
        """
        :returns: The sid
        :rtype: unicode
        """
        return self._properties['sid']

    @property
    def status(self):
        """
        :returns: The status
        :rtype: transcription.status
        """
        return self._properties['status']

    @property
    def transcription_text(self):
        """
        :returns: The transcription_text
        :rtype: unicode
        """
        return self._properties['transcription_text']

    @property
    def type(self):
        """
        :returns: The type
        :rtype: unicode
        """
        return self._properties['type']

    @property
    def uri(self):
        """
        :returns: The uri
        :rtype: unicode
        """
        return self._properties['uri']

    def fetch(self):
        """
        Fetch a TranscriptionInstance
        
        :returns: Fetched TranscriptionInstance
        :rtype: TranscriptionInstance
        """
        return self._proxy.fetch()

    def delete(self):
        """
        Deletes the TranscriptionInstance
        
        :returns: True if delete succeeds, False otherwise
        :rtype: bool
        """
        return self._proxy.delete()

    def __repr__(self):
        """
        Provide a friendly representation
        
        :returns: Machine friendly representation
        :rtype: str
        """
        context = ' '.join('{}={}'.format(k, v) for k, v in self._solution.items())
        return '<Twilio.Api.V2010.TranscriptionInstance {}>'.format(context)
