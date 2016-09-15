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
from twilio.rest.chat.v1.service.channel import ChannelList
from twilio.rest.chat.v1.service.role import RoleList
from twilio.rest.chat.v1.service.user import UserList


class ServiceList(ListResource):

    def __init__(self, version):
        """
        Initialize the ServiceList
        
        :param Version version: Version that contains the resource
        
        :returns: ServiceList
        :rtype: ServiceList
        """
        super(ServiceList, self).__init__(version)
        
        # Path Solution
        self._solution = {}
        self._uri = '/Services'.format(**self._solution)

    def create(self, friendly_name):
        """
        Create a new ServiceInstance
        
        :param unicode friendly_name: The friendly_name
        
        :returns: Newly created ServiceInstance
        :rtype: ServiceInstance
        """
        data = values.of({
            'FriendlyName': friendly_name,
        })
        
        payload = self._version.create(
            'POST',
            self._uri,
            data=data,
        )
        
        return ServiceInstance(
            self._version,
            payload,
        )

    def stream(self, limit=None, page_size=None):
        """
        Streams ServiceInstance records from the API as a generator stream.
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
        Lists ServiceInstance records from the API as a list.
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
        Retrieve a single page of ServiceInstance records from the API.
        Request is executed immediately
        
        :param str page_token: PageToken provided by the API
        :param int page_number: Page Number, this value is simply for client state
        :param int page_size: Number of records to return, defaults to 50
        
        :returns: Page of ServiceInstance
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
        
        return ServicePage(self._version, response, self._solution)

    def get(self, sid):
        """
        Constructs a ServiceContext
        
        :param sid: The sid
        
        :returns: ServiceContext
        :rtype: ServiceContext
        """
        return ServiceContext(
            self._version,
            sid=sid,
        )

    def __call__(self, sid):
        """
        Constructs a ServiceContext
        
        :param sid: The sid
        
        :returns: ServiceContext
        :rtype: ServiceContext
        """
        return ServiceContext(
            self._version,
            sid=sid,
        )

    def __repr__(self):
        """
        Provide a friendly representation
        
        :returns: Machine friendly representation
        :rtype: str
        """
        return '<Twilio.Chat.V1.ServiceList>'


class ServicePage(Page):

    def __init__(self, version, response, solution):
        """
        Initialize the ServicePage
        
        :param Version version: Version that contains the resource
        :param Response response: Response from the API
        
        :returns: ServicePage
        :rtype: ServicePage
        """
        super(ServicePage, self).__init__(version, response)
        
        # Path Solution
        self._solution = solution

    def get_instance(self, payload):
        """
        Build an instance of ServiceInstance
        
        :param dict payload: Payload response from the API
        
        :returns: ServiceInstance
        :rtype: ServiceInstance
        """
        return ServiceInstance(
            self._version,
            payload,
        )

    def __repr__(self):
        """
        Provide a friendly representation
        
        :returns: Machine friendly representation
        :rtype: str
        """
        return '<Twilio.Chat.V1.ServicePage>'


class ServiceContext(InstanceContext):

    def __init__(self, version, sid):
        """
        Initialize the ServiceContext
        
        :param Version version: Version that contains the resource
        :param sid: The sid
        
        :returns: ServiceContext
        :rtype: ServiceContext
        """
        super(ServiceContext, self).__init__(version)
        
        # Path Solution
        self._solution = {
            'sid': sid,
        }
        self._uri = '/Services/{sid}'.format(**self._solution)
        
        # Dependents
        self._channels = None
        self._roles = None
        self._users = None

    def fetch(self):
        """
        Fetch a ServiceInstance
        
        :returns: Fetched ServiceInstance
        :rtype: ServiceInstance
        """
        params = values.of({})
        
        payload = self._version.fetch(
            'GET',
            self._uri,
            params=params,
        )
        
        return ServiceInstance(
            self._version,
            payload,
            sid=self._solution['sid'],
        )

    def delete(self):
        """
        Deletes the ServiceInstance
        
        :returns: True if delete succeeds, False otherwise
        :rtype: bool
        """
        return self._version.delete('delete', self._uri)

    def update(self, friendly_name=values.unset,
               default_service_role_sid=values.unset,
               default_channel_role_sid=values.unset,
               default_channel_creator_role_sid=values.unset,
               read_status_enabled=values.unset,
               typing_indicator_timeout=values.unset,
               consumption_report_interval=values.unset, webhooks=values.unset):
        """
        Update the ServiceInstance
        
        :param unicode friendly_name: The friendly_name
        :param unicode default_service_role_sid: The default_service_role_sid
        :param unicode default_channel_role_sid: The default_channel_role_sid
        :param unicode default_channel_creator_role_sid: The default_channel_creator_role_sid
        :param bool read_status_enabled: The read_status_enabled
        :param unicode typing_indicator_timeout: The typing_indicator_timeout
        :param unicode consumption_report_interval: The consumption_report_interval
        :param dict webhooks: The webhooks
        
        :returns: Updated ServiceInstance
        :rtype: ServiceInstance
        """
        data = values.of({
            'FriendlyName': friendly_name,
            'DefaultServiceRoleSid': default_service_role_sid,
            'DefaultChannelRoleSid': default_channel_role_sid,
            'DefaultChannelCreatorRoleSid': default_channel_creator_role_sid,
            'ReadStatusEnabled': read_status_enabled,
            'TypingIndicatorTimeout': typing_indicator_timeout,
            'ConsumptionReportInterval': consumption_report_interval,
            'Webhooks': webhooks,
        })
        
        payload = self._version.update(
            'POST',
            self._uri,
            data=data,
        )
        
        return ServiceInstance(
            self._version,
            payload,
            sid=self._solution['sid'],
        )

    @property
    def channels(self):
        """
        Access the channels
        
        :returns: ChannelList
        :rtype: ChannelList
        """
        if self._channels is None:
            self._channels = ChannelList(
                self._version,
                service_sid=self._solution['sid'],
            )
        return self._channels

    @property
    def roles(self):
        """
        Access the roles
        
        :returns: RoleList
        :rtype: RoleList
        """
        if self._roles is None:
            self._roles = RoleList(
                self._version,
                service_sid=self._solution['sid'],
            )
        return self._roles

    @property
    def users(self):
        """
        Access the users
        
        :returns: UserList
        :rtype: UserList
        """
        if self._users is None:
            self._users = UserList(
                self._version,
                service_sid=self._solution['sid'],
            )
        return self._users

    def __repr__(self):
        """
        Provide a friendly representation
        
        :returns: Machine friendly representation
        :rtype: str
        """
        context = ' '.join('{}={}'.format(k, v) for k, v in self._solution.items())
        return '<Twilio.Chat.V1.ServiceContext {}>'.format(context)


class ServiceInstance(InstanceResource):

    def __init__(self, version, payload, sid=None):
        """
        Initialize the ServiceInstance
        
        :returns: ServiceInstance
        :rtype: ServiceInstance
        """
        super(ServiceInstance, self).__init__(version)
        
        # Marshaled Properties
        self._properties = {
            'sid': payload['sid'],
            'account_sid': payload['account_sid'],
            'friendly_name': payload['friendly_name'],
            'date_created': deserialize.iso8601_datetime(payload['date_created']),
            'date_updated': deserialize.iso8601_datetime(payload['date_updated']),
            'default_service_role_sid': payload['default_service_role_sid'],
            'default_channel_role_sid': payload['default_channel_role_sid'],
            'default_channel_creator_role_sid': payload['default_channel_creator_role_sid'],
            'read_status_enabled': payload['read_status_enabled'],
            'typing_indicator_timeout': deserialize.integer(payload['typing_indicator_timeout']),
            'consumption_report_interval': deserialize.integer(payload['consumption_report_interval']),
            'webhooks': payload['webhooks'],
            'url': payload['url'],
            'links': payload['links'],
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
        
        :returns: ServiceContext for this ServiceInstance
        :rtype: ServiceContext
        """
        if self._context is None:
            self._context = ServiceContext(
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
    def default_service_role_sid(self):
        """
        :returns: The default_service_role_sid
        :rtype: unicode
        """
        return self._properties['default_service_role_sid']

    @property
    def default_channel_role_sid(self):
        """
        :returns: The default_channel_role_sid
        :rtype: unicode
        """
        return self._properties['default_channel_role_sid']

    @property
    def default_channel_creator_role_sid(self):
        """
        :returns: The default_channel_creator_role_sid
        :rtype: unicode
        """
        return self._properties['default_channel_creator_role_sid']

    @property
    def read_status_enabled(self):
        """
        :returns: The read_status_enabled
        :rtype: bool
        """
        return self._properties['read_status_enabled']

    @property
    def typing_indicator_timeout(self):
        """
        :returns: The typing_indicator_timeout
        :rtype: unicode
        """
        return self._properties['typing_indicator_timeout']

    @property
    def consumption_report_interval(self):
        """
        :returns: The consumption_report_interval
        :rtype: unicode
        """
        return self._properties['consumption_report_interval']

    @property
    def webhooks(self):
        """
        :returns: The webhooks
        :rtype: dict
        """
        return self._properties['webhooks']

    @property
    def url(self):
        """
        :returns: The url
        :rtype: unicode
        """
        return self._properties['url']

    @property
    def links(self):
        """
        :returns: The links
        :rtype: unicode
        """
        return self._properties['links']

    def fetch(self):
        """
        Fetch a ServiceInstance
        
        :returns: Fetched ServiceInstance
        :rtype: ServiceInstance
        """
        return self._proxy.fetch()

    def delete(self):
        """
        Deletes the ServiceInstance
        
        :returns: True if delete succeeds, False otherwise
        :rtype: bool
        """
        return self._proxy.delete()

    def update(self, friendly_name=values.unset,
               default_service_role_sid=values.unset,
               default_channel_role_sid=values.unset,
               default_channel_creator_role_sid=values.unset,
               read_status_enabled=values.unset,
               typing_indicator_timeout=values.unset,
               consumption_report_interval=values.unset, webhooks=values.unset):
        """
        Update the ServiceInstance
        
        :param unicode friendly_name: The friendly_name
        :param unicode default_service_role_sid: The default_service_role_sid
        :param unicode default_channel_role_sid: The default_channel_role_sid
        :param unicode default_channel_creator_role_sid: The default_channel_creator_role_sid
        :param bool read_status_enabled: The read_status_enabled
        :param unicode typing_indicator_timeout: The typing_indicator_timeout
        :param unicode consumption_report_interval: The consumption_report_interval
        :param dict webhooks: The webhooks
        
        :returns: Updated ServiceInstance
        :rtype: ServiceInstance
        """
        return self._proxy.update(
            friendly_name=friendly_name,
            default_service_role_sid=default_service_role_sid,
            default_channel_role_sid=default_channel_role_sid,
            default_channel_creator_role_sid=default_channel_creator_role_sid,
            read_status_enabled=read_status_enabled,
            typing_indicator_timeout=typing_indicator_timeout,
            consumption_report_interval=consumption_report_interval,
            webhooks=webhooks,
        )

    @property
    def channels(self):
        """
        Access the channels
        
        :returns: channels
        :rtype: channels
        """
        return self._proxy.channels

    @property
    def roles(self):
        """
        Access the roles
        
        :returns: roles
        :rtype: roles
        """
        return self._proxy.roles

    @property
    def users(self):
        """
        Access the users
        
        :returns: users
        :rtype: users
        """
        return self._proxy.users

    def __repr__(self):
        """
        Provide a friendly representation
        
        :returns: Machine friendly representation
        :rtype: str
        """
        context = ' '.join('{}={}'.format(k, v) for k, v in self._solution.items())
        return '<Twilio.Chat.V1.ServiceInstance {}>'.format(context)
