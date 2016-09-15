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


class WorkerChannelList(ListResource):

    def __init__(self, version, workspace_sid, worker_sid):
        """
        Initialize the WorkerChannelList
        
        :param Version version: Version that contains the resource
        :param workspace_sid: The workspace_sid
        :param worker_sid: The worker_sid
        
        :returns: WorkerChannelList
        :rtype: WorkerChannelList
        """
        super(WorkerChannelList, self).__init__(version)
        
        # Path Solution
        self._solution = {
            'workspace_sid': workspace_sid,
            'worker_sid': worker_sid,
        }
        self._uri = '/Workspaces/{workspace_sid}/Workers/{worker_sid}/Channels'.format(**self._solution)

    def stream(self, limit=None, page_size=None):
        """
        Streams WorkerChannelInstance records from the API as a generator stream.
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
        Lists WorkerChannelInstance records from the API as a list.
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
        Retrieve a single page of WorkerChannelInstance records from the API.
        Request is executed immediately
        
        :param str page_token: PageToken provided by the API
        :param int page_number: Page Number, this value is simply for client state
        :param int page_size: Number of records to return, defaults to 50
        
        :returns: Page of WorkerChannelInstance
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
        
        return WorkerChannelPage(self._version, response, self._solution)

    def get(self, sid):
        """
        Constructs a WorkerChannelContext
        
        :param sid: The sid
        
        :returns: WorkerChannelContext
        :rtype: WorkerChannelContext
        """
        return WorkerChannelContext(
            self._version,
            workspace_sid=self._solution['workspace_sid'],
            worker_sid=self._solution['worker_sid'],
            sid=sid,
        )

    def __call__(self, sid):
        """
        Constructs a WorkerChannelContext
        
        :param sid: The sid
        
        :returns: WorkerChannelContext
        :rtype: WorkerChannelContext
        """
        return WorkerChannelContext(
            self._version,
            workspace_sid=self._solution['workspace_sid'],
            worker_sid=self._solution['worker_sid'],
            sid=sid,
        )

    def __repr__(self):
        """
        Provide a friendly representation
        
        :returns: Machine friendly representation
        :rtype: str
        """
        return '<Twilio.Taskrouter.V1.WorkerChannelList>'


class WorkerChannelPage(Page):

    def __init__(self, version, response, solution):
        """
        Initialize the WorkerChannelPage
        
        :param Version version: Version that contains the resource
        :param Response response: Response from the API
        :param workspace_sid: The workspace_sid
        :param worker_sid: The worker_sid
        
        :returns: WorkerChannelPage
        :rtype: WorkerChannelPage
        """
        super(WorkerChannelPage, self).__init__(version, response)
        
        # Path Solution
        self._solution = solution

    def get_instance(self, payload):
        """
        Build an instance of WorkerChannelInstance
        
        :param dict payload: Payload response from the API
        
        :returns: WorkerChannelInstance
        :rtype: WorkerChannelInstance
        """
        return WorkerChannelInstance(
            self._version,
            payload,
            workspace_sid=self._solution['workspace_sid'],
            worker_sid=self._solution['worker_sid'],
        )

    def __repr__(self):
        """
        Provide a friendly representation
        
        :returns: Machine friendly representation
        :rtype: str
        """
        return '<Twilio.Taskrouter.V1.WorkerChannelPage>'


class WorkerChannelContext(InstanceContext):

    def __init__(self, version, workspace_sid, worker_sid, sid):
        """
        Initialize the WorkerChannelContext
        
        :param Version version: Version that contains the resource
        :param workspace_sid: The workspace_sid
        :param worker_sid: The worker_sid
        :param sid: The sid
        
        :returns: WorkerChannelContext
        :rtype: WorkerChannelContext
        """
        super(WorkerChannelContext, self).__init__(version)
        
        # Path Solution
        self._solution = {
            'workspace_sid': workspace_sid,
            'worker_sid': worker_sid,
            'sid': sid,
        }
        self._uri = '/Workspaces/{workspace_sid}/Workers/{worker_sid}/Channels/{sid}'.format(**self._solution)

    def fetch(self):
        """
        Fetch a WorkerChannelInstance
        
        :returns: Fetched WorkerChannelInstance
        :rtype: WorkerChannelInstance
        """
        params = values.of({})
        
        payload = self._version.fetch(
            'GET',
            self._uri,
            params=params,
        )
        
        return WorkerChannelInstance(
            self._version,
            payload,
            workspace_sid=self._solution['workspace_sid'],
            worker_sid=self._solution['worker_sid'],
            sid=self._solution['sid'],
        )

    def update(self, capacity=values.unset, available=values.unset):
        """
        Update the WorkerChannelInstance
        
        :param unicode capacity: The capacity
        :param bool available: The available
        
        :returns: Updated WorkerChannelInstance
        :rtype: WorkerChannelInstance
        """
        data = values.of({
            'Capacity': capacity,
            'Available': available,
        })
        
        payload = self._version.update(
            'POST',
            self._uri,
            data=data,
        )
        
        return WorkerChannelInstance(
            self._version,
            payload,
            workspace_sid=self._solution['workspace_sid'],
            worker_sid=self._solution['worker_sid'],
            sid=self._solution['sid'],
        )

    def __repr__(self):
        """
        Provide a friendly representation
        
        :returns: Machine friendly representation
        :rtype: str
        """
        context = ' '.join('{}={}'.format(k, v) for k, v in self._solution.items())
        return '<Twilio.Taskrouter.V1.WorkerChannelContext {}>'.format(context)


class WorkerChannelInstance(InstanceResource):

    def __init__(self, version, payload, workspace_sid, worker_sid, sid=None):
        """
        Initialize the WorkerChannelInstance
        
        :returns: WorkerChannelInstance
        :rtype: WorkerChannelInstance
        """
        super(WorkerChannelInstance, self).__init__(version)
        
        # Marshaled Properties
        self._properties = {
            'account_sid': payload['account_sid'],
            'assigned_tasks': deserialize.integer(payload['assigned_tasks']),
            'available': payload['available'],
            'available_capacity_percentage': deserialize.integer(payload['available_capacity_percentage']),
            'configured_capacity': deserialize.integer(payload['configured_capacity']),
            'date_created': deserialize.iso8601_datetime(payload['date_created']),
            'date_updated': deserialize.iso8601_datetime(payload['date_updated']),
            'sid': payload['sid'],
            'task_channel_sid': payload['task_channel_sid'],
            'task_channel_unique_name': payload['task_channel_unique_name'],
            'worker_sid': payload['worker_sid'],
            'workspace_sid': payload['workspace_sid'],
            'links': payload['links'],
            'url': payload['url'],
        }
        
        # Context
        self._context = None
        self._solution = {
            'workspace_sid': workspace_sid,
            'worker_sid': worker_sid,
            'sid': sid or self._properties['sid'],
        }

    @property
    def _proxy(self):
        """
        Generate an instance context for the instance, the context is capable of
        performing various actions.  All instance actions are proxied to the context
        
        :returns: WorkerChannelContext for this WorkerChannelInstance
        :rtype: WorkerChannelContext
        """
        if self._context is None:
            self._context = WorkerChannelContext(
                self._version,
                workspace_sid=self._solution['workspace_sid'],
                worker_sid=self._solution['worker_sid'],
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
    def assigned_tasks(self):
        """
        :returns: The assigned_tasks
        :rtype: unicode
        """
        return self._properties['assigned_tasks']

    @property
    def available(self):
        """
        :returns: The available
        :rtype: bool
        """
        return self._properties['available']

    @property
    def available_capacity_percentage(self):
        """
        :returns: The available_capacity_percentage
        :rtype: unicode
        """
        return self._properties['available_capacity_percentage']

    @property
    def configured_capacity(self):
        """
        :returns: The configured_capacity
        :rtype: unicode
        """
        return self._properties['configured_capacity']

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
    def sid(self):
        """
        :returns: The sid
        :rtype: unicode
        """
        return self._properties['sid']

    @property
    def task_channel_sid(self):
        """
        :returns: The task_channel_sid
        :rtype: unicode
        """
        return self._properties['task_channel_sid']

    @property
    def task_channel_unique_name(self):
        """
        :returns: The task_channel_unique_name
        :rtype: unicode
        """
        return self._properties['task_channel_unique_name']

    @property
    def worker_sid(self):
        """
        :returns: The worker_sid
        :rtype: unicode
        """
        return self._properties['worker_sid']

    @property
    def workspace_sid(self):
        """
        :returns: The workspace_sid
        :rtype: unicode
        """
        return self._properties['workspace_sid']

    @property
    def links(self):
        """
        :returns: The links
        :rtype: unicode
        """
        return self._properties['links']

    @property
    def url(self):
        """
        :returns: The url
        :rtype: unicode
        """
        return self._properties['url']

    def fetch(self):
        """
        Fetch a WorkerChannelInstance
        
        :returns: Fetched WorkerChannelInstance
        :rtype: WorkerChannelInstance
        """
        return self._proxy.fetch()

    def update(self, capacity=values.unset, available=values.unset):
        """
        Update the WorkerChannelInstance
        
        :param unicode capacity: The capacity
        :param bool available: The available
        
        :returns: Updated WorkerChannelInstance
        :rtype: WorkerChannelInstance
        """
        return self._proxy.update(
            capacity=capacity,
            available=available,
        )

    def __repr__(self):
        """
        Provide a friendly representation
        
        :returns: Machine friendly representation
        :rtype: str
        """
        context = ' '.join('{}={}'.format(k, v) for k, v in self._solution.items())
        return '<Twilio.Taskrouter.V1.WorkerChannelInstance {}>'.format(context)
