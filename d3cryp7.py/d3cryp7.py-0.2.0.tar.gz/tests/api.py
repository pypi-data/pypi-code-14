from requests import get, post
import os
import unittest

PANGRAM = None

# Locate data file and read it
for root, dirs, files in os.walk(os.getcwd()):
	if 'pangram' in files:
		PANGRAM = os.path.join(root, 'pangram')
		PANGRAM = open(PANGRAM, 'rb').read()

class ApiTest(unittest.TestCase):
	'''
	Tests the RESTful API to verify that it works correctly
	'''

	@classmethod
	def setUpClass(self):
		'''
		Verifies that the application is running
		'''

		try:
			get('http://localhost')
		except:
			self.fail(
				'Could not connect, the application is not running on port 80'
			)

	def test_version(self):
		'''
		Tests that the API handles the version route correctly
		'''

		data = get('http://localhost/api/version').json()
		self.assertTrue('version' in data)

	def test_statistics(self):
		'''
		Tests that the API handles the statistics route correctly
		'''

		data = get('http://localhost/api/statistics').json()
		self.assertTrue('d3cryp7' in data)
		self.assertTrue('status' in data['d3cryp7'])
		self.assertTrue('status_code' in data['d3cryp7'])
		self.assertTrue('version' in data['d3cryp7'])
		self.assertTrue('python' in data)
		self.assertTrue('platform' in data['python'])
		self.assertTrue('version' in data['python'])
		self.assertTrue('time' in data)
		self.assertTrue('current' in data['time'])
		self.assertTrue('running' in data['time'])
		self.assertTrue('start' in data['time'])

	def test_recognize(self):
		'''
		Tests that the API handles the recognize route correctly
		'''

		data = {'image': PANGRAM}
		data = post('http://localhost/api/recognize', data = data).json()
		self.assertTrue('result' in data)
		self.assertEqual(
			data['result'],
			'The quick brown fox jumps over the lazy dog.'
		)

if __name__ == '__main__':
	unittest.main()
