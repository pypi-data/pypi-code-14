from d3cryp7 import image
import os
import unittest

PANGRAM = None

# Locate data file and read it
for root, dirs, files in os.walk(os.getcwd()):
	if 'pangram' in files:
		PANGRAM = os.path.join(root, 'pangram')
		PANGRAM = open(PANGRAM, 'rb').read()

	if 'hello_world' in files:
		HELLO_WORLD = os.path.join(root, 'hello_world')
		HELLO_WORLD = open(HELLO_WORLD, 'rb').read()

class ImageTest(unittest.TestCase):
	'''
	Tests the functions in the Image module to verify that they work correctly
	'''

	def test_recognize(self):
		'''
		Tests that the function returns the correct result
		'''

		data = image.recognize(PANGRAM)
		self.assertTrue('result' in data)
		self.assertEqual(
			data['result'],
			'The quick brown fox jumps over the lazy dog.'
		)

		data = image.recognize(HELLO_WORLD)
		self.assertTrue('result' in data)
		self.assertTrue('error' in data)
		self.assertEqual(data['result'], 'Hello\nWorld')
		self.assertEqual(
			data['error'],
			'Info in pixReadStreamPng: converting (gray + alpha) ==> RGBA\n' \
			'Error in pixGenHalftoneMask: pix too small: w = 97, h = 63'
		)

if __name__ == '__main__':
	unittest.main()
