from .base import Base
from .person import Person
from .persongroup import PersonGroup
from .facelist import FaceList

_detectUrl = 'https://api.projectoxford.ai/face/v1.0/detect'
_similarUrl = 'https://api.projectoxford.ai/face/v1.0/findsimilars'
_groupingUrl = 'https://api.projectoxford.ai/face/v1.0/group'
_identifyUrl = 'https://api.projectoxford.ai/face/v1.0/identify'
_verifyUrl = 'https://api.projectoxford.ai/face/v1.0/verify'


class Face(Base):
    """Client for using the Project Oxford face APIs"""

    def __init__(self, key):
        """Initializes a new instance of the class.
        Args:
            key (str). the API key to use for this client.
        """
        Base.__init__(self, key)
        self.person = Person(self.key)
        self.personGroup = PersonGroup(self.key)
        self.faceList = FaceList(self.key)

    def detect(self, options):
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
            options.returnFaceLandmarks (boolean). The Analyze face landmarks?
            options.returnFaceAttributes (string). The attributes to return.

        Returns:
            object. The resulting JSON
        """

        # build params query string
        params = {
            'returnFaceLandmarks': 'true' if 'returnFaceLandmarks' in options else 'false'
        }

        if 'returnFaceAttributes' in options:
            params['returnFaceAttributes'] = options['returnFaceAttributes']

        return Base._postWithOptions(self, _detectUrl, options, params)

    def similar(self, sourceFace, candidateFaces=None, candidateFaceListId=None, maxNumOfCandidatesReturned=20):
        """Detect similar faces using faceIds (as returned from the detect API)

        Args:
            sourceFace (str). The source face
            candidateFaces (str[]). The candidate faces

        Returns:
            object. The resulting JSON
        """

        if candidateFaces and candidateFaceListId:
            raise Exception("You can't provide both a face list id and faces to find similar.")

        body = {
            'faceId': sourceFace,
            'maxNumOfCandidatesReturned': maxNumOfCandidatesReturned
        }

        if candidateFaces:
            body['faceIds'] = candidateFaces

        if candidateFaceListId:
            body['faceListId'] = candidateFaceListId

        return self._invoke('post', _similarUrl, json=body, headers={'Ocp-Apim-Subscription-Key': self.key})

    def grouping(self, faceIds):
        """Divides candidate faces into groups based on face similarity using faceIds.
        The output is one or more disjointed face groups and a MessyGroup.
        A face group contains the faces that have similar looking, often of the same person.
        There will be one or more face groups ranked by group size, i.e. number of face.
        Faces belonging to the same person might be split into several groups in the result.
        The MessyGroup is a special face group that each face is not similar to any other
        faces in original candidate faces. The messyGroup will not appear in the result if
        all faces found their similar counterparts. The candidate face list has a
        limit of 100 faces.

        Args:
            faceIds (str[]). Array of faceIds to use

        Returns:
            object. The resulting JSON
        """

        body = {'faceIds': faceIds}

        return self._invoke('post', _groupingUrl, json=body, headers={'Ocp-Apim-Subscription-Key': self.key})

    def identify(self, personGroupId, faces, maxNumOfCandidatesReturned=1):
        """Identifies persons from a person group by one or more input faces.
        To recognize which person a face belongs to, Face Identification needs a person group
        that contains number of persons. Each person contains one or more faces. After a person
        group prepared, it should be trained to make it ready for identification. Then the
        identification API compares the input face to those persons' faces in person group and
        returns the best-matched candidate persons, ranked by confidence.

        Args:
            faces (str[]). Array of faceIds to use
            personGroupId (str). The person group ID to use
            maxNumOfCandidatesReturned (str). Optional maximum number of candidates to return

        Returns:
            object. The resulting JSON
        """

        body = {
            'faceIds': faces,
            'personGroupId': personGroupId,
            'maxNumOfCandidatesReturned': maxNumOfCandidatesReturned
        }

        return self._invoke('post', _identifyUrl, json=body, headers={'Ocp-Apim-Subscription-Key': self.key})

    def verify(self, faceId1, faceId2):
        """Analyzes two faces and determine whether they are from the same person.
        Verification works well for frontal and near-frontal faces.
        For the scenarios that are sensitive to accuracy please use with own judgment.

        Args:
            faceId1 (str). The first face to compare
            faceId2 (str). The second face to compare

        Returns:
            object. The resulting JSON
        """

        body = {
            'faceId1': faceId1,
            'faceId2': faceId2
        }

        return self._invoke('post', _verifyUrl, json=body, headers={'Ocp-Apim-Subscription-Key': self.key})
