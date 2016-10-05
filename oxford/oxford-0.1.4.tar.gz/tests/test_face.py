import copy
import os
import sys
import unittest
import time
import uuid

rootDirectory = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
if rootDirectory not in sys.path:
    sys.path.insert(0, rootDirectory)

from oxford.face import Face

class TestFace(unittest.TestCase):
    '''Tests the Project Oxford Face API'''

    @classmethod
    def setUpClass(cls):
        # set up self.client for tests
        cls.client = Face(os.environ['OXFORD_FACE_API_KEY'])

        # detect two faces
        cls.knownFaceIds = [];
        cls.localFilePrefix = os.path.join(rootDirectory, 'tests', 'images')
        face1 = cls.client.detect({'path': os.path.join(cls.localFilePrefix, 'face1.jpg')})
        face2 = cls.client.detect({'path': os.path.join(cls.localFilePrefix, 'face2.jpg')})
        cls.knownFaceIds.append(face1[0]['faceId'])
        cls.knownFaceIds.append(face2[0]['faceId'])

        # set common detect options
        cls.detectOptions = {
            'returnFaceLandmarks': True,
            'returnFaceAttributes': 'age,gender,headPose,smile,facialHair'
        }
        

    #
    # test the detect API
    #
    def _verifyDetect(self, detectResult):
        faceIdResult = detectResult[0]
        
        self.assertIsInstance(faceIdResult['faceId'], object, 'face ID is returned')
        self.assertIsInstance(faceIdResult['faceRectangle'], object, 'faceRectangle is returned')
        self.assertIsInstance(faceIdResult['faceLandmarks'], object, 'faceLandmarks are returned')
        
        attributes = faceIdResult['faceAttributes']
        self.assertIsInstance(attributes, object, 'attributes are returned')
        self.assertIsInstance(attributes['gender'], object, 'gender is returned')
        self.assertIsInstance(attributes['age'], float, 'age is returned')

    def test_face_detect_url(self):
        options = copy.copy(self.detectOptions)
        options['url'] = 'https://upload.wikimedia.org/wikipedia/commons/1/19/Bill_Gates_June_2015.jpg'
        detectResult = self.client.detect(options)
        self._verifyDetect(detectResult)

    def test_face_detect_file(self):
        options = copy.copy(self.detectOptions)
        options['path'] = os.path.join(self.localFilePrefix, 'face1.jpg')
        detectResult = self.client.detect(options)
        self._verifyDetect(detectResult)

    def test_face_detect_stream(self):
        options = copy.copy(self.detectOptions)
        with open(os.path.join(self.localFilePrefix, 'face1.jpg'), 'rb') as file:
            options['stream'] = file.read()
            detectResult = self.client.detect(options)
        self._verifyDetect(detectResult)

    def test_face_detect_throws_invalid_options(self):
        self.assertRaises(Exception, self.client.detect, {})

    #
    # test the similar API
    #
    def test_face_similar(self):
        similarResult = self.client.similar(self.knownFaceIds[0], [self.knownFaceIds[1]])
        self.assertIsInstance(similarResult, list, 'similar result is returned')
        self.assertEqual(self.knownFaceIds[1], similarResult[0]['faceId'], 'expected similar face is returned')

    # def test_face_similar(self):
    #     similarResult = self.client.similar(self.knownFaceIds[0], [self.knownFaceIds[1]])
    #     self.assertIsInstance(similarResult, list, 'similar result is returned')
    #     self.assertEqual(self.knownFaceIds[1], similarResult[0]['faceId'], 'expected similar face is returned')
    
    #
    # test the grouping API
    #
    def test_face_grouping(self):
        faces = self.client.detect({'path': os.path.join(self.localFilePrefix, 'face-group.jpg')})


        faceIds = []
        for face in faces:
            faceIds.append(face['faceId'])

        groupingResult = self.client.grouping(faceIds)
        self.assertIsInstance(groupingResult, object, 'grouping result is returned')
        self.assertIsInstance(groupingResult['groups'], list, 'groups list is returned')
        self.assertIsInstance(groupingResult['messyGroup'], list, 'messygroup list is returned')

    #
    # test the verify API
    #
    def test_face_verify(self):
        verifyResult = self.client.verify(self.knownFaceIds[0], self.knownFaceIds[1])
        self.assertIsInstance(verifyResult, object, 'grouping result is returned')
        self.assertEqual(verifyResult['isIdentical'], True, 'verify succeeded')
        self.assertGreaterEqual(verifyResult['confidence'], 0.5, 'confidence is returned')

    #
    # test the identify API
    #
    def test_face_identify(self):
        fpath = os.path.join(self.localFilePrefix, 'face1.jpg')
        group_id = 'testgroup'
        group_name = 'testgroup'
        try:
            self.client.personGroup.create(group_id, group_name)
        except Exception as e:
            if "PersonGroupExists" not in e: 
                self.assertRaises(Exception, "Error creating persongroup", {})
        faceId = self.client.detect({'path': fpath})[0]['faceId']
        person_id = self.client.person.create(group_id, 'billG')['personId']
        faceId = self.client.person.addFace(group_id, person_id, {'path':fpath})
        status = self.client.personGroup.trainingStart(group_id)
        while status is None or status['status'] not in ['succeeded', 'failed']:
            time.sleep(1)
            status = self.client.personGroup.trainingStatus(group_id)
        if status and status['status'] == 'failed':
            self.client.personGroup.delete(group_id)
            self.assertRaises(Exception, "Failed to train group.", {})
        faceId2 = self.client.detect({'path': os.path.join(self.localFilePrefix, 'face2.jpg')})[0]['faceId']
        identifyResult = self.client.identify(group_id, [faceId2])
        self.assertIsInstance(identifyResult, object, 'identify result is returned')
        self.assertEqual(identifyResult[0]['candidates'][0]['personId'], person_id)
        self.client.personGroup.delete(group_id)