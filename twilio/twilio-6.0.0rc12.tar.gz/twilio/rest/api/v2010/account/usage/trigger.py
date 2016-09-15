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


class TriggerList(ListResource):

    def __init__(self, version, account_sid):
        """
        Initialize the TriggerList
        
        :param Version version: Version that contains the resource
        :param account_sid: A 34 character string that uniquely identifies this resource.
        
        :returns: TriggerList
        :rtype: TriggerList
        """
        super(TriggerList, self).__init__(version)
        
        # Path Solution
        self._solution = {
            'account_sid': account_sid,
        }
        self._uri = '/Accounts/{account_sid}/Usage/Triggers.json'.format(**self._solution)

    def create(self, callback_url, trigger_value, usage_category,
               callback_method=values.unset, friendly_name=values.unset,
               recurring=values.unset, trigger_by=values.unset):
        """
        Create a new TriggerInstance
        
        :param unicode callback_url: URL Twilio will request when the trigger fires
        :param unicode trigger_value: the value at which the trigger will fire
        :param trigger.usage_category usage_category: The usage category the trigger watches
        :param unicode callback_method: HTTP method to use with callback_url
        :param unicode friendly_name: A user-specified, human-readable name for the trigger.
        :param trigger.recurring recurring: How this trigger recurs
        :param trigger.trigger_field trigger_by: The field in the UsageRecord that fires the trigger
        
        :returns: Newly created TriggerInstance
        :rtype: TriggerInstance
        """
        data = values.of({
            'CallbackUrl': callback_url,
            'TriggerValue': trigger_value,
            'UsageCategory': usage_category,
            'CallbackMethod': callback_method,
            'FriendlyName': friendly_name,
            'Recurring': recurring,
            'TriggerBy': trigger_by,
        })
        
        payload = self._version.create(
            'POST',
            self._uri,
            data=data,
        )
        
        return TriggerInstance(
            self._version,
            payload,
            account_sid=self._solution['account_sid'],
        )

    def stream(self, recurring=values.unset, trigger_by=values.unset,
               usage_category=values.unset, limit=None, page_size=None):
        """
        Streams TriggerInstance records from the API as a generator stream.
        This operation lazily loads records as efficiently as possible until the limit
        is reached.
        The results are returned as a generator, so this operation is memory efficient.
        
        :param trigger.recurring recurring: Filter by recurring
        :param trigger.trigger_field trigger_by: Filter by trigger by
        :param trigger.usage_category usage_category: Filter by Usage Category
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
            recurring=recurring,
            trigger_by=trigger_by,
            usage_category=usage_category,
            page_size=limits['page_size'],
        )
        
        return self._version.stream(page, limits['limit'], limits['page_limit'])

    def list(self, recurring=values.unset, trigger_by=values.unset,
             usage_category=values.unset, limit=None, page_size=None):
        """
        Lists TriggerInstance records from the API as a list.
        Unlike stream(), this operation is eager and will load `limit` records into
        memory before returning.
        
        :param trigger.recurring recurring: Filter by recurring
        :param trigger.trigger_field trigger_by: Filter by trigger by
        :param trigger.usage_category usage_category: Filter by Usage Category
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
            recurring=recurring,
            trigger_by=trigger_by,
            usage_category=usage_category,
            limit=limit,
            page_size=page_size,
        ))

    def page(self, recurring=values.unset, trigger_by=values.unset,
             usage_category=values.unset, page_token=values.unset,
             page_number=values.unset, page_size=values.unset):
        """
        Retrieve a single page of TriggerInstance records from the API.
        Request is executed immediately
        
        :param trigger.recurring recurring: Filter by recurring
        :param trigger.trigger_field trigger_by: Filter by trigger by
        :param trigger.usage_category usage_category: Filter by Usage Category
        :param str page_token: PageToken provided by the API
        :param int page_number: Page Number, this value is simply for client state
        :param int page_size: Number of records to return, defaults to 50
        
        :returns: Page of TriggerInstance
        :rtype: Page
        """
        params = values.of({
            'Recurring': recurring,
            'TriggerBy': trigger_by,
            'UsageCategory': usage_category,
            'PageToken': page_token,
            'Page': page_number,
            'PageSize': page_size,
        })
        
        response = self._version.page(
            'GET',
            self._uri,
            params=params,
        )
        
        return TriggerPage(self._version, response, self._solution)

    def get(self, sid):
        """
        Constructs a TriggerContext
        
        :param sid: Fetch by unique usage-trigger Sid
        
        :returns: TriggerContext
        :rtype: TriggerContext
        """
        return TriggerContext(
            self._version,
            account_sid=self._solution['account_sid'],
            sid=sid,
        )

    def __call__(self, sid):
        """
        Constructs a TriggerContext
        
        :param sid: Fetch by unique usage-trigger Sid
        
        :returns: TriggerContext
        :rtype: TriggerContext
        """
        return TriggerContext(
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
        return '<Twilio.Api.V2010.TriggerList>'


class TriggerPage(Page):

    def __init__(self, version, response, solution):
        """
        Initialize the TriggerPage
        
        :param Version version: Version that contains the resource
        :param Response response: Response from the API
        :param account_sid: A 34 character string that uniquely identifies this resource.
        
        :returns: TriggerPage
        :rtype: TriggerPage
        """
        super(TriggerPage, self).__init__(version, response)
        
        # Path Solution
        self._solution = solution

    def get_instance(self, payload):
        """
        Build an instance of TriggerInstance
        
        :param dict payload: Payload response from the API
        
        :returns: TriggerInstance
        :rtype: TriggerInstance
        """
        return TriggerInstance(
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
        return '<Twilio.Api.V2010.TriggerPage>'


class TriggerContext(InstanceContext):

    def __init__(self, version, account_sid, sid):
        """
        Initialize the TriggerContext
        
        :param Version version: Version that contains the resource
        :param account_sid: The account_sid
        :param sid: Fetch by unique usage-trigger Sid
        
        :returns: TriggerContext
        :rtype: TriggerContext
        """
        super(TriggerContext, self).__init__(version)
        
        # Path Solution
        self._solution = {
            'account_sid': account_sid,
            'sid': sid,
        }
        self._uri = '/Accounts/{account_sid}/Usage/Triggers/{sid}.json'.format(**self._solution)

    def fetch(self):
        """
        Fetch a TriggerInstance
        
        :returns: Fetched TriggerInstance
        :rtype: TriggerInstance
        """
        params = values.of({})
        
        payload = self._version.fetch(
            'GET',
            self._uri,
            params=params,
        )
        
        return TriggerInstance(
            self._version,
            payload,
            account_sid=self._solution['account_sid'],
            sid=self._solution['sid'],
        )

    def update(self, callback_method=values.unset, callback_url=values.unset,
               friendly_name=values.unset):
        """
        Update the TriggerInstance
        
        :param unicode callback_method: HTTP method to use with callback_url
        :param unicode callback_url: URL Twilio will request when the trigger fires
        :param unicode friendly_name: A user-specified, human-readable name for the trigger.
        
        :returns: Updated TriggerInstance
        :rtype: TriggerInstance
        """
        data = values.of({
            'CallbackMethod': callback_method,
            'CallbackUrl': callback_url,
            'FriendlyName': friendly_name,
        })
        
        payload = self._version.update(
            'POST',
            self._uri,
            data=data,
        )
        
        return TriggerInstance(
            self._version,
            payload,
            account_sid=self._solution['account_sid'],
            sid=self._solution['sid'],
        )

    def delete(self):
        """
        Deletes the TriggerInstance
        
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
        return '<Twilio.Api.V2010.TriggerContext {}>'.format(context)


class TriggerInstance(InstanceResource):

    def __init__(self, version, payload, account_sid, sid=None):
        """
        Initialize the TriggerInstance
        
        :returns: TriggerInstance
        :rtype: TriggerInstance
        """
        super(TriggerInstance, self).__init__(version)
        
        # Marshaled Properties
        self._properties = {
            'account_sid': payload['account_sid'],
            'api_version': payload['api_version'],
            'callback_method': payload['callback_method'],
            'callback_url': payload['callback_url'],
            'current_value': payload['current_value'],
            'date_created': deserialize.rfc2822_datetime(payload['date_created']),
            'date_fired': deserialize.rfc2822_datetime(payload['date_fired']),
            'date_updated': deserialize.rfc2822_datetime(payload['date_updated']),
            'friendly_name': payload['friendly_name'],
            'recurring': payload['recurring'],
            'sid': payload['sid'],
            'trigger_by': payload['trigger_by'],
            'trigger_value': payload['trigger_value'],
            'uri': payload['uri'],
            'usage_category': payload['usage_category'],
            'usage_record_uri': payload['usage_record_uri'],
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
        
        :returns: TriggerContext for this TriggerInstance
        :rtype: TriggerContext
        """
        if self._context is None:
            self._context = TriggerContext(
                self._version,
                account_sid=self._solution['account_sid'],
                sid=self._solution['sid'],
            )
        return self._context

    @property
    def account_sid(self):
        """
        :returns: The account this trigger monitors.
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
    def callback_method(self):
        """
        :returns: HTTP method to use with callback_url
        :rtype: unicode
        """
        return self._properties['callback_method']

    @property
    def callback_url(self):
        """
        :returns: URL Twilio will request when the trigger fires
        :rtype: unicode
        """
        return self._properties['callback_url']

    @property
    def current_value(self):
        """
        :returns: The current value of the field the trigger is watching.
        :rtype: unicode
        """
        return self._properties['current_value']

    @property
    def date_created(self):
        """
        :returns: The date this resource was created
        :rtype: datetime
        """
        return self._properties['date_created']

    @property
    def date_fired(self):
        """
        :returns: The date the trigger was last fired
        :rtype: datetime
        """
        return self._properties['date_fired']

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
        :returns: A user-specified, human-readable name for the trigger.
        :rtype: unicode
        """
        return self._properties['friendly_name']

    @property
    def recurring(self):
        """
        :returns: How this trigger recurs
        :rtype: trigger.recurring
        """
        return self._properties['recurring']

    @property
    def sid(self):
        """
        :returns: The trigger's unique Sid
        :rtype: unicode
        """
        return self._properties['sid']

    @property
    def trigger_by(self):
        """
        :returns: The field in the UsageRecord that fires the trigger
        :rtype: trigger.trigger_field
        """
        return self._properties['trigger_by']

    @property
    def trigger_value(self):
        """
        :returns: the value at which the trigger will fire
        :rtype: unicode
        """
        return self._properties['trigger_value']

    @property
    def uri(self):
        """
        :returns: The URI for this resource
        :rtype: unicode
        """
        return self._properties['uri']

    @property
    def usage_category(self):
        """
        :returns: The usage category the trigger watches
        :rtype: trigger.usage_category
        """
        return self._properties['usage_category']

    @property
    def usage_record_uri(self):
        """
        :returns: The URI of the UsageRecord this trigger is watching
        :rtype: unicode
        """
        return self._properties['usage_record_uri']

    def fetch(self):
        """
        Fetch a TriggerInstance
        
        :returns: Fetched TriggerInstance
        :rtype: TriggerInstance
        """
        return self._proxy.fetch()

    def update(self, callback_method=values.unset, callback_url=values.unset,
               friendly_name=values.unset):
        """
        Update the TriggerInstance
        
        :param unicode callback_method: HTTP method to use with callback_url
        :param unicode callback_url: URL Twilio will request when the trigger fires
        :param unicode friendly_name: A user-specified, human-readable name for the trigger.
        
        :returns: Updated TriggerInstance
        :rtype: TriggerInstance
        """
        return self._proxy.update(
            callback_method=callback_method,
            callback_url=callback_url,
            friendly_name=friendly_name,
        )

    def delete(self):
        """
        Deletes the TriggerInstance
        
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
        return '<Twilio.Api.V2010.TriggerInstance {}>'.format(context)
