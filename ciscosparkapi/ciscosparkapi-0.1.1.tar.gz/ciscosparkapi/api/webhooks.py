"""Cisco Spark Webhooks-API wrapper classes.

Classes:
    Webhook: Models a Spark 'webhook' JSON object as a native Python object.
    WebhooksAPI: Wrappers the Cisco Spark Webhooks-API and exposes the API
        calls as Python method calls that return native Python objects.

"""


from ciscosparkapi.exceptions import ciscosparkapiException
from ciscosparkapi.helper import utf8, generator_container
from ciscosparkapi.restsession import RestSession
from ciscosparkapi.sparkdata import SparkData


class Webhook(SparkData):
    """Model a Spark 'webhook' JSON object as a native Python object."""

    def __init__(self, json):
        """Init a new Webhook data object from a JSON dictionary or string.

        Args:
            json(dict, unicode, str): Input JSON object.

        Raises:
            TypeError: If the input object is not a dictionary or string.

        """
        super(Webhook, self).__init__(json)

    @property
    def id(self):
        """Webhook ID."""
        return self._json.get(u'id')

    @property
    def name(self):
        """A user-friendly name for this webhook."""
        return self._json.get(u'name')

    @property
    def targetUrl(self):
        """The URL that receives POST requests for each event."""
        return self._json.get(u'targetUrl')

    @property
    def resource(self):
        """The resource type for the webhook."""
        return self._json.get(u'resource')

    @property
    def event(self):
        """The event type for the webhook."""
        return self._json.get(u'event')

    @property
    def filter(self):
        """The filter that defines the webhook scope."""
        return self._json.get(u'filter')

    @property
    def secret(self):
        """Secret used to generate payload signature."""
        return self._json.get(u'secret')

    @property
    def created(self):
        """Creation date and time in ISO8601 format."""
        return self._json.get(u'created')

    @property
    def data(self):
        """The object representation of the resource triggering the webhook.

        The data property contains the object representation of the resource
        that triggered the webhook. For example, if you registered a webhook
        that triggers when messages are created (i.e. posted into a room) then
        the data property will contain the representation for a message
        resource, as specified in the Messages API documentation.

        """
        object_data = self._json.get(u'data', None)
        if object_data:
            return SparkData(object_data)
        else:
            return None


class WebhooksAPI(object):
    """Cisco Spark Webhooks-API wrapper class.

    Wrappers the Cisco Spark Webhooks-API and exposes the API calls as Python
    method calls that return native Python objects.

    Attributes:
        session(RestSession): The RESTful session object to be used for API
            calls to the Cisco Spark service.

    """

    def __init__(self, session):
        """Init a new WebhooksAPI object with the provided RestSession.

        Args:
            session(RestSession): The RESTful session object to be used for
                API calls to the Cisco Spark service.

        Raises:
            AssertionError: If the parameter types are incorrect.

        """
        assert isinstance(session, RestSession)
        super(WebhooksAPI, self).__init__()
        self.session = session

    @generator_container
    def list(self, max=None):
        """List all of the authenticated user's webhooks.

        This method supports Cisco Spark's implementation of RFC5988 Web
        Linking to provide pagination support.  It returns a generator
        container that incrementally yields all webhooks returned by the
        query.  The generator will automatically request additional 'pages' of
        responses from Spark as needed until all responses have been returned.
        The container makes the generator safe for reuse.  A new API call will
        be made, using the same parameters that were specified when the
        generator was created, every time a new iterator is requested from the
        container.

        Args:
            max(int): Limits the maximum number of webhooks returned from the
                Spark service per request.

        Yields:
            Webhook: The the next webhook from the Cisco Spark query.

        Raises:
            AssertionError: If the parameter types are incorrect.
            SparkApiError: If the Cisco Spark cloud returns an error.

        """
        # Process args
        assert max is None or isinstance(max, int)
        params = {}
        if max:
            params[u'max'] = max
        # API request - get items
        items = self.session.get_items('webhooks', params=params)
        # Yield Webhook objects created from the returned items JSON objects
        for item in items:
            yield Webhook(item)

    def create(self, name, targetUrl, resource, event,
               filter=None, secret=None):
        """Create a webhook.

        Args:
            name(unicode, str): A user-friendly name for this webhook.
            targetUrl(unicode, str): The URL that receives POST requests for
                each event.
            resource(unicode, str): The resource type for the webhook.
            event(unicode, str): The event type for the webhook.
            filter(unicode, str): The filter that defines the webhook scope.
            secret(unicode, str): secret used to generate payload signature.

        Returns:
            Webhook: With the details of the created webhook.

        Raises:
            AssertionError: If the parameter types are incorrect.
            SparkApiError: If the Cisco Spark cloud returns an error.

        """
        # Process args
        assert isinstance(name, basestring)
        assert isinstance(targetUrl, basestring)
        assert isinstance(resource, basestring)
        assert isinstance(event, basestring)
        assert filter is None or isinstance(filter, basestring)
        assert secret is None or isinstance(secret, basestring)
        post_data = {}
        post_data[u'name'] = utf8(name)
        post_data[u'targetUrl'] = utf8(targetUrl)
        post_data[u'resource'] = utf8(resource)
        post_data[u'event'] = utf8(event)
        if filter:
            post_data[u'filter'] = utf8(filter)
        if secret:
            post_data[u'secret'] = utf8(secret)
        # API request
        json_obj = self.session.post('webhooks', json=post_data)
        # Return a Webhook object created from the response JSON data
        return Webhook(json_obj)

    def get(self, webhookId):
        """Get the details of a webhook, by ID.

        Args:
            webhookId(unicode, str): The webhookId of the webhook.

        Returns:
            Webhook: With the details of the requested webhook.

        Raises:
            AssertionError: If the parameter types are incorrect.
            SparkApiError: If the Cisco Spark cloud returns an error.

        """
        # Process args
        assert isinstance(webhookId, basestring)
        # API request
        json_obj = self.session.get('webhooks/' + webhookId)
        # Return a Webhook object created from the response JSON data
        return Webhook(json_obj)

    def update(self, webhookId, **update_attributes):
        """Update details for a webhook.

        Args:
            webhookId(unicode, str): The webhookId of the webhook to be
                updated.

            **update_attributes:
                name(unicode, str): A user-friendly name for this webhook.
                targetUrl(unicode, str): The URL that receives POST requests
                    for each event.

        Returns:
            Webhook: With the updated Spark webhook details.

        Raises:
            AssertionError: If the parameter types are incorrect.
            ciscosparkapiException: If an update attribute is not provided.
            SparkApiError: If the Cisco Spark cloud returns an error.

        """
        # Process args
        assert isinstance(webhookId, basestring)
        # Process update_attributes keyword arguments
        if not update_attributes:
            error_message = "At least one **update_attributes keyword " \
                            "argument must be specified."
            raise ciscosparkapiException(error_message)
        put_data = {}
        for param, value in update_attributes.items():
            if isinstance(value, basestring):
                value = utf8(value)
            put_data[utf8(param)] = value
        # API request
        json_obj = self.session.post('webhooks/' + webhookId, json=put_data)
        # Return a Webhook object created from the response JSON data
        return Webhook(json_obj)

    def delete(self, webhookId):
        """Delete a webhook.

        Args:
            webhookId(unicode, str): The webhookId of the webhook to be
                deleted.

        Raises:
            AssertionError: If the parameter types are incorrect.
            SparkApiError: If the Cisco Spark cloud returns an error.

        """
        # Process args
        assert isinstance(webhookId, basestring)
        # API request
        self.session.delete('webhooks/' + webhookId)
