from .base import Base

_personUrl = 'https://api.projectoxford.ai/face/v1.0/persongroups'


class Person(Base):
    """Client for using the Project Oxford person APIs"""

    def __init__(self, key):
        """Initializes a new instance of the class.
        Args:
            key (str). the API key to use for this client.
        """
        Base.__init__(self, key)

    def addFace(self, personGroupId, personId, options):
        """Detects human faces in an image and returns face locations, face landmarks, and
        optional attributes including head-pose, gender, and age. Detection is an essential
        API that provides faceId to other APIs like Identification, Verification,
        and Find Similar.

        Note: exactly one of url, path, or stream must be provided in the options object

        Args:
            options (object). The Options object
            options.url (str). The URL to image to be used
            options.path (str). The Path to image to be used
            options.stream (stream). The stream of the image to be used
            options.userData (string). The Analyze face landmarks?
            options.targetFace (string). The attributes to return.

        Returns:
            object. The resulting JSON
        """

        # build params query string
        params = {}

        if 'userData' in options:
            params['userData'] = options['userData']
            del options['userData']

        if 'targetFace' in options:
            params['targetFace'] = options['targetFace']
            del options['targetFace']

        return Base._postWithOptions(self, _personUrl + '/' + personGroupId + '/persons/' + personId + '/persistedFaces', options, params)

    def create(self, personGroupId, name, userData=None):
        """Creates a new person in a specified person group for identification.
        The number of persons has a subscription limit. Free subscription amount is 1000 persons.
        The maximum face count for each person is 32.

        Args:
            personGroupId (str). The target person's person group.
            faceIds ([str]). Array of face id's for the target person
            name (str). Target person's display name. The maximum length is 128.
            userData (str). Optional fields for user-provided data attached to a person. Size limit is 16KB.

        Returns:
            object. The resulting JSON
        """

        body = {
            'name': name
        }

        if userData is not None:
            body['userData'] = userData

        uri = _personUrl + '/' + personGroupId + '/persons'
        return self._invoke('post', uri, json=body, headers={'Ocp-Apim-Subscription-Key': self.key})

    def delete(self, personGroupId, personId):
        """Deletes an existing person from a person group.

        Args:
            personGroupId (str). The target person's person group.
            personId (str). The target person to delete.

        Returns:
            object. The resulting JSON
        """

        uri = _personUrl + '/' + personGroupId + '/persons/' + personId
        return self._invoke('delete', uri, headers={'Ocp-Apim-Subscription-Key': self.key})

    def deleteFace(self, personGroupId, personId, faceId):
        """Deletes a face from a person.

        Args:
            personGroupId (str). The target person's person group.
            personId (str). The target person that the face is removed from.
            faceId (str). The ID of the face to be deleted.

        Returns:
            object. The resulting JSON
        """

        uri = _personUrl + '/' + personGroupId + '/persons/' + personId + '/persistedFaces/' + faceId
        return self._invoke('delete', uri, headers={'Ocp-Apim-Subscription-Key': self.key})

    def get(self, personGroupId, personId):
        """Gets an existing person from a person group.

        Args:
            personGroupId (str). The target person's person group.
            personId (str). The target person to get.

        Returns:
            object. The resulting JSON
        """

        uri = _personUrl + '/' + personGroupId + '/persons/' + personId
        return self._invoke('get', uri, headers={'Ocp-Apim-Subscription-Key': self.key})

    def getFace(self, personGroupId, personId, faceId):
        """Get a face for a person.

        Args:
            personGroupId (str). The target person's person group.
            personId (str). The target person that the face is to get from.
            faceId (str). The ID of the face to get.

        Returns:
            object. The resulting JSON
        """

        uri = _personUrl + '/' + personGroupId + '/persons/' + personId + '/persistedFaces/' + faceId
        return self._invoke('get', uri, headers={'Ocp-Apim-Subscription-Key': self.key})

    def list(self, personGroupId):
        """Lists all persons in a person group, with the person information.

        Args:
            personGroupId (str). The target person's person group.

        Returns:
            object. The resulting JSON
        """

        uri = _personUrl + '/' + personGroupId + '/persons'
        return self._invoke('get', uri, headers={'Ocp-Apim-Subscription-Key': self.key})

    def update(self, personGroupId, personId, name, userData=None):
        """Updates a person's information.

        Args:
            personGroupId (str). The target person's person group.
            personId (str). The target persons Id.
            faceIds ([str]). Array of face id's for the target person.
            name (str). Target person's display name. The maximum length is 128.
            userData (str). Optional fields for user-provided data attached to a person. Size limit is 16KB.

        Returns:
            object. The resulting JSON
        """

        body = {
            'name': name
        }

        if userData is not None:
            body['userData'] = userData

        uri = _personUrl + '/' + personGroupId + '/persons/' + personId
        return self._invoke('patch', uri, json=body, headers={'Ocp-Apim-Subscription-Key': self.key})

    def updateFace(self, personGroupId, personId, persistedFaceId, userData=None):
        """Updates a face for a person.

        Args:
            personGroupId (str). The target person's person group.
            personId (str). The target person that the face is updated on.
            faceId (str). The ID of the face to be updated.
            userData (str). Optional. Attach user data to person's face. The maximum length is 1024.

        Returns:
            object. The resulting JSON
        """

        body = {} if userData is None else {'userData': userData}

        uri = _personUrl + '/' + personGroupId + '/persons/' + personId + '/persistedFaces/' + persistedFaceId
        return self._invoke('patch', uri, json=body, headers={'Ocp-Apim-Subscription-Key': self.key})
