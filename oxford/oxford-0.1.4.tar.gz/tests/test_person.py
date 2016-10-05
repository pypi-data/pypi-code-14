import os
import sys
import unittest
import uuid

rootDirectory = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
if rootDirectory not in sys.path:
    sys.path.insert(0, rootDirectory)

from oxford.person import Person
from oxford.face import Face

class TestPerson(unittest.TestCase):
    '''Tests the Project Oxford Face API'''

    @classmethod
    def setUpClass(cls):
        # set up client for tests
        cls.client = Face(os.environ['OXFORD_FACE_API_KEY'])

        # detect two faces
        cls.knownFaceIds = [];
        localFilePrefix = os.path.join(rootDirectory, 'tests', 'images')
        face1 = cls.client.detect({'path': os.path.join(localFilePrefix, 'face1.jpg')})
        face2 = cls.client.detect({'path': os.path.join(localFilePrefix, 'face2.jpg')})
        cls.knownFaceIds.append(face1[0]['faceId'])
        cls.knownFaceIds.append(face2[0]['faceId'])
        
        # create a person group
        cls.personGroupId = str(uuid.uuid4())
        cls.client.personGroup.create(cls.personGroupId, 'test-person-group')

    @classmethod
    def tearDownClass(cls):
        cls.client.personGroup.delete(cls.personGroupId)

    def test_person_create_update_get_delete(self):
        # create
        result = self.client.person.create(self.personGroupId, 'billg', 'test-person')
        personId = result['personId']
        self.assertIsInstance(personId, object, 'person id was returned')

        # update
        result = self.client.person.update(self.personGroupId, personId, 'bill gates', 'test-person')
        self.assertIsNone(result, 'person was updated')

        # get
        result = self.client.person.get(self.personGroupId, personId)
        personIdVerify = result['personId']
        self.assertEqual(personId, personIdVerify, 'person id was verified')

        # delete
        self.client.person.delete(self.personGroupId, personId)
        self.assertTrue(True, 'person was deleted')

    def test_person_face_add_update_delete(self):
        # create
        result = self.client.person.create(self.personGroupId, 'billg', 'test-person')
        personId = result['personId']
        self.assertIsInstance(personId, object, 'create succeeded')

        # add a new face ID
        self.client.person.addFace(self.personGroupId, personId, {'path': os.path.join(os.path.join(rootDirectory, 'tests', 'images'), 'face1.jpg')})
        self.assertTrue(True, 'add succeeded')

        # update a face ID
        self.client.person.updateFace(self.personGroupId,self.knownFaceIds[0], 'billg2', 'test-bill')
        personId = result['personId']
        self.assertIsInstance(personId, object, 'update succeeded')
        
        # delete the original face ID
        self.client.person.deleteFace(self.personGroupId, personId, self.knownFaceIds[0])
        self.assertTrue(True, 'delete succeeded')
        
        # clean up
        self.client.person.delete(self.personGroupId, personId)

    def test_person_list(self):
        # create some people
        self.client.person.create(self.personGroupId, 'billg1', 'test-person')
        self.client.person.create(self.personGroupId, 'billg2', 'test-person')
        
        # list them
        listResult = self.client.person.list(self.personGroupId)
        self.assertEqual(len(listResult), 2)

        # remove them
        for person in listResult:
            self.client.person.delete(self.personGroupId, person['personId'])
