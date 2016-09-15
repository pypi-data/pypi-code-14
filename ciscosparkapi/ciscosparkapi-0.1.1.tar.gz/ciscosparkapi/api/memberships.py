"""Cisco Spark Memberships-API wrapper classes.

Classes:
    Membership: Models a Spark 'membership' JSON object as a native Python
        object.
    MembershipsAPI: Wrappers the Cisco Spark Memberships-API and exposes the
        API calls as Python method calls that return native Python objects.

"""


from ciscosparkapi.exceptions import ciscosparkapiException
from ciscosparkapi.helper import utf8, generator_container
from ciscosparkapi.restsession import RestSession
from ciscosparkapi.sparkdata import SparkData


class Membership(SparkData):
    """Model a Spark 'membership' JSON object as a native Python object."""

    def __init__(self, json):
        """Init a new Membership data object from a JSON dictionary or string.

        Args:
            json(dict, unicode, str): Input JSON object.

        Raises:
            TypeError: If the input object is not a dictionary or string.

        """
        super(Membership, self).__init__(json)

    @property
    def id(self):
        return self._json[u'id']

    @property
    def roomId(self):
        return self._json[u'roomId']

    @property
    def personId(self):
        return self._json[u'personId']

    @property
    def personEmail(self):
        return self._json[u'personEmail']

    @property
    def personDisplayName(self):
        return self._json[u'personDisplayName']

    @property
    def isModerator(self):
        return self._json[u'isModerator']

    @property
    def isMonitor(self):
        return self._json[u'isMonitor']

    @property
    def created(self):
        return self._json[u'created']


class MembershipsAPI(object):
    """Cisco Spark Memberships-API wrapper class.

    Wrappers the Cisco Spark Memberships-API and exposes the API calls as
    Python method calls that return native Python objects.

    Attributes:
        session(RestSession): The RESTful session object to be used for API
            calls to the Cisco Spark service.

    """

    def __init__(self, session):
        """Init a new MembershipsAPI object with the provided RestSession.

        Args:
            session(RestSession): The RESTful session object to be used for
                API calls to the Cisco Spark service.

        Raises:
            AssertionError: If the parameter types are incorrect.

        """
        assert isinstance(session, RestSession)
        super(MembershipsAPI, self).__init__()
        self.session = session

    @generator_container
    def list(self, roomId=None, personId=None, personEmail=None, max=None):
        """List room memberships.

        By default, lists memberships for rooms to which the authenticated
        user belongs.

        Use query parameters to filter the response.

        Use roomId to list memberships for a room, by ID.

        Use either personId or personEmail to filter the results.

        This method supports Cisco Spark's implementation of RFC5988 Web
        Linking to provide pagination support.  It returns a generator
        container that incrementally yield all memberships returned by the
        query.  The generator will automatically request additional 'pages' of
        responses from Spark as needed until all responses have been returned.
        The container makes the generator safe for reuse.  A new API call will
        be made, using the same parameters that were specified when the
        generator was created, every time a new iterator is requested from the
        container.

        Args:
            roomId(unicode, str): List memberships for the room with roomId.
            personId(unicode, str): Filter results to include only those with
                personId.
            personEmail(unicode, str): Filter results to include only those
                with personEmail.
            max(int): Limits the maximum number of memberships returned from
                the Spark service per request.


        Yields:
            Membership: The the next membership from the Cisco Spark query.

        Raises:
            AssertionError: If the parameter types are incorrect.
            ciscosparkapiException: If a personId or personEmail argument is
                specified without providing a roomId argument.
            SparkApiError: If the Cisco Spark cloud returns an error.

        """
        # Process args
        assert roomId is None or isinstance(roomId, basestring)
        assert personId is None or isinstance(personId, basestring)
        assert personEmail is None or isinstance(personEmail, basestring)
        assert max is None or isinstance(max, int)
        params = {}
        if roomId:
            params[u'roomId'] = utf8(roomId)
            if personId:
                params[u'personId'] = utf8(personId)
            elif personEmail:
                params[u'personEmail'] = utf8(personEmail)
        elif personId or personEmail:
            error_message = "A roomId must be specified. A personId or " \
                            "personEmail filter may only be specified when " \
                            "requesting the memberships for a room with the " \
                            "roomId argument."
            raise ciscosparkapiException(error_message)
        if max:
            params[u'max'] = max
        # API request - get items
        items = self.session.get_items('memberships', params=params)
        # Yield Person objects created from the returned items JSON objects
        for item in items:
            yield Membership(item)

    def create(self, roomId, personId=None, personEmail=None,
               isModerator=False):
        """Add someone to a room by Person ID or email address.

        Add someone to a room by Person ID or email address; optionally
        making them a moderator.

        Args:
            roomId(unicode, str): ID of the room to which the person will be
                added.
            personId(unicode, str): ID of the person to be added to the room.
            personEmail(unicode, str): Email address of the person to be added
                to the room.
            isModerator(bool): If True, adds the person as a moderator for the
                room. If False, adds the person as normal member of the room.

        Returns:
            Membership: With the details of the created membership.

        Raises:
            AssertionError: If the parameter types are incorrect.
            ciscosparkapiException: If neither a personId or personEmail are
                provided.
            SparkApiError: If the Cisco Spark cloud returns an error.

        """
        # Process args
        assert isinstance(roomId, basestring)
        assert personId is None or isinstance(personId, basestring)
        assert personEmail is None or isinstance(personEmail, basestring)
        assert isModerator is None or isinstance(isModerator, bool)
        post_data = {}
        post_data[u'roomId'] = utf8(roomId)
        if personId:
            post_data[u'personId'] = utf8(personId)
        elif personEmail:
            post_data[u'personEmail'] = utf8(personEmail)
        else:
            error_message = "personId or personEmail must be provided to " \
                            "add a person to a room.  Neither were provided."
            raise ciscosparkapiException(error_message)
        post_data[u'isModerator'] = isModerator
        # API request
        json_obj = self.session.post('memberships', json=post_data)
        # Return a Membership object created from the response JSON data
        return Membership(json_obj)

    def get(self, membershipId):
        """Get details for a membership by ID.

        Args:
            membershipId(unicode, str): The membershipId of the membership.

        Returns:
            Membership: With the details of the requested membership.

        Raises:
            AssertionError: If the parameter types are incorrect.
            SparkApiError: If the Cisco Spark cloud returns an error.

        """
        # Process args
        assert isinstance(membershipId, basestring)
        # API request
        json_obj = self.session.get('memberships/'+membershipId)
        # Return a Membership object created from the response JSON data
        return Membership(json_obj)

    def update(self, membershipId, **update_attributes):
        """Update details for a membership.

        Args:
            membershipId(unicode, str): The membershipId of the membership to
                be updated.

        **update_attributes:
            isModerator(bool): If True, sets the person as a moderator for the
                room. If False, removes the person as a moderator for the room.

        Returns:
            Membership: With the updated Spark membership details.

        Raises:
            AssertionError: If the parameter types are incorrect.
            ciscosparkapiException: If an update attribute is not provided.
            SparkApiError: If the Cisco Spark cloud returns an error.

        """
        # Process args
        assert isinstance(membershipId, basestring)
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
        json_obj = self.session.post('memberships/'+membershipId,
                                     json=put_data)
        # Return a Membership object created from the response JSON data
        return Membership(json_obj)

    def delete(self, membershipId):
        """Delete a membership, by ID.

        Args:
            membershipId(unicode, str): The membershipId of the membership to
                be deleted.

        Raises:
            AssertionError: If the parameter types are incorrect.
            SparkApiError: If the Cisco Spark cloud returns an error.

        """
        # Process args
        assert isinstance(membershipId, basestring)
        # API request
        self.session.delete('memberships/'+membershipId)
