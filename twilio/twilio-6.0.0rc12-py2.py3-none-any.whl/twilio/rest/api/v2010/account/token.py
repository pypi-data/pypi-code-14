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


class TokenList(ListResource):

    def __init__(self, version, account_sid):
        """
        Initialize the TokenList
        
        :param Version version: Version that contains the resource
        :param account_sid: The unique sid that identifies this account
        
        :returns: TokenList
        :rtype: TokenList
        """
        super(TokenList, self).__init__(version)
        
        # Path Solution
        self._solution = {
            'account_sid': account_sid,
        }
        self._uri = '/Accounts/{account_sid}/Tokens.json'.format(**self._solution)

    def create(self, ttl=values.unset):
        """
        Create a new TokenInstance
        
        :param unicode ttl: The duration in seconds the credentials are valid
        
        :returns: Newly created TokenInstance
        :rtype: TokenInstance
        """
        data = values.of({
            'Ttl': ttl,
        })
        
        payload = self._version.create(
            'POST',
            self._uri,
            data=data,
        )
        
        return TokenInstance(
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
        return '<Twilio.Api.V2010.TokenList>'


class TokenPage(Page):

    def __init__(self, version, response, solution):
        """
        Initialize the TokenPage
        
        :param Version version: Version that contains the resource
        :param Response response: Response from the API
        :param account_sid: The unique sid that identifies this account
        
        :returns: TokenPage
        :rtype: TokenPage
        """
        super(TokenPage, self).__init__(version, response)
        
        # Path Solution
        self._solution = solution

    def get_instance(self, payload):
        """
        Build an instance of TokenInstance
        
        :param dict payload: Payload response from the API
        
        :returns: TokenInstance
        :rtype: TokenInstance
        """
        return TokenInstance(
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
        return '<Twilio.Api.V2010.TokenPage>'


class TokenInstance(InstanceResource):

    def __init__(self, version, payload, account_sid):
        """
        Initialize the TokenInstance
        
        :returns: TokenInstance
        :rtype: TokenInstance
        """
        super(TokenInstance, self).__init__(version)
        
        # Marshaled Properties
        self._properties = {
            'account_sid': payload['account_sid'],
            'date_created': deserialize.rfc2822_datetime(payload['date_created']),
            'date_updated': deserialize.rfc2822_datetime(payload['date_updated']),
            'ice_servers': payload['ice_servers'],
            'password': payload['password'],
            'ttl': payload['ttl'],
            'username': payload['username'],
        }
        
        # Context
        self._context = None
        self._solution = {
            'account_sid': account_sid,
        }

    @property
    def account_sid(self):
        """
        :returns: The unique sid that identifies this account
        :rtype: unicode
        """
        return self._properties['account_sid']

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
    def ice_servers(self):
        """
        :returns: An array representing the ephemeral credentials
        :rtype: unicode
        """
        return self._properties['ice_servers']

    @property
    def password(self):
        """
        :returns: The temporary password used for authenticating
        :rtype: unicode
        """
        return self._properties['password']

    @property
    def ttl(self):
        """
        :returns: The duration in seconds the credentials are valid
        :rtype: unicode
        """
        return self._properties['ttl']

    @property
    def username(self):
        """
        :returns: The temporary username that uniquely identifies a Token.
        :rtype: unicode
        """
        return self._properties['username']

    def __repr__(self):
        """
        Provide a friendly representation
        
        :returns: Machine friendly representation
        :rtype: str
        """
        return '<Twilio.Api.V2010.TokenInstance>'
