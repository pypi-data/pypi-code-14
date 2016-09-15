# coding=utf-8
"""
This code was generated by
\ / _    _  _|   _  _
 | (_)\/(_)(_|\/| |(/_  v1.0.0
      /       /       
"""

from twilio import deserialize
from twilio import values
from twilio.instance_resource import InstanceResource
from twilio.list_resource import ListResource
from twilio.page import Page


class FeedbackList(ListResource):

    def __init__(self, version, account_sid, message_sid):
        """
        Initialize the FeedbackList
        
        :param Version version: Version that contains the resource
        :param account_sid: The account_sid
        :param message_sid: The message_sid
        
        :returns: FeedbackList
        :rtype: FeedbackList
        """
        super(FeedbackList, self).__init__(version)
        
        # Path Solution
        self._solution = {
            'account_sid': account_sid,
            'message_sid': message_sid,
        }
        self._uri = '/Accounts/{account_sid}/Messages/{message_sid}/Feedback.json'.format(**self._solution)

    def create(self, outcome=values.unset):
        """
        Create a new FeedbackInstance
        
        :param feedback.outcome outcome: The outcome
        
        :returns: Newly created FeedbackInstance
        :rtype: FeedbackInstance
        """
        data = values.of({
            'Outcome': outcome,
        })
        
        payload = self._version.create(
            'POST',
            self._uri,
            data=data,
        )
        
        return FeedbackInstance(
            self._version,
            payload,
            account_sid=self._solution['account_sid'],
            message_sid=self._solution['message_sid'],
        )

    def __repr__(self):
        """
        Provide a friendly representation
        
        :returns: Machine friendly representation
        :rtype: str
        """
        return '<Twilio.Api.V2010.FeedbackList>'


class FeedbackPage(Page):

    def __init__(self, version, response, solution):
        """
        Initialize the FeedbackPage
        
        :param Version version: Version that contains the resource
        :param Response response: Response from the API
        :param account_sid: The account_sid
        :param message_sid: The message_sid
        
        :returns: FeedbackPage
        :rtype: FeedbackPage
        """
        super(FeedbackPage, self).__init__(version, response)
        
        # Path Solution
        self._solution = solution

    def get_instance(self, payload):
        """
        Build an instance of FeedbackInstance
        
        :param dict payload: Payload response from the API
        
        :returns: FeedbackInstance
        :rtype: FeedbackInstance
        """
        return FeedbackInstance(
            self._version,
            payload,
            account_sid=self._solution['account_sid'],
            message_sid=self._solution['message_sid'],
        )

    def __repr__(self):
        """
        Provide a friendly representation
        
        :returns: Machine friendly representation
        :rtype: str
        """
        return '<Twilio.Api.V2010.FeedbackPage>'


class FeedbackInstance(InstanceResource):

    def __init__(self, version, payload, account_sid, message_sid):
        """
        Initialize the FeedbackInstance
        
        :returns: FeedbackInstance
        :rtype: FeedbackInstance
        """
        super(FeedbackInstance, self).__init__(version)
        
        # Marshaled Properties
        self._properties = {
            'account_sid': payload['account_sid'],
            'message_sid': payload['message_sid'],
            'outcome': payload['outcome'],
            'date_created': deserialize.rfc2822_datetime(payload['date_created']),
            'date_updated': deserialize.rfc2822_datetime(payload['date_updated']),
            'uri': payload['uri'],
        }
        
        # Context
        self._context = None
        self._solution = {
            'account_sid': account_sid,
            'message_sid': message_sid,
        }

    @property
    def account_sid(self):
        """
        :returns: The account_sid
        :rtype: unicode
        """
        return self._properties['account_sid']

    @property
    def message_sid(self):
        """
        :returns: The message_sid
        :rtype: unicode
        """
        return self._properties['message_sid']

    @property
    def outcome(self):
        """
        :returns: The outcome
        :rtype: feedback.outcome
        """
        return self._properties['outcome']

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
    def uri(self):
        """
        :returns: The uri
        :rtype: unicode
        """
        return self._properties['uri']

    def __repr__(self):
        """
        Provide a friendly representation
        
        :returns: Machine friendly representation
        :rtype: str
        """
        return '<Twilio.Api.V2010.FeedbackInstance>'
