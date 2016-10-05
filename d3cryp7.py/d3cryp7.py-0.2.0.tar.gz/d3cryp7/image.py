'''
Image

This module defines functions for image processing. The RESTful API uses these
functions to generate a result. See the documentation for each function and the
unit tests for more information.
'''

import base64
import subprocess

def recognize(image):
	'''
	Recognizes text in an image by using Google's Tesseract engine and returns a
	dictionary containing the result and any error messages that occurred

	Args:
		image (string): A base64 encoded image

	Returns:
		A dictionary containing the result and any error messages

	This function does not use file IO. Instead, the image is recognized by
	first decoding the base64 image and then piping the data directly to
	Tesseract. If the result from Tesseract is empty, the result will be None.
	If no error occurred, the dictionary will not contain an error.
	'''

	proc = subprocess.Popen(
		'tesseract - stdout',
		stdin = subprocess.PIPE,
		stdout = subprocess.PIPE,
		stderr = subprocess.PIPE,
		shell = True
	)

	data = base64.b64decode(image)
	out, err = proc.communicate(input = data)
	out = out.decode().strip()
	err = err.decode().strip()

	result = {
		'result': out if out else None
	}

	if err:
		result['error'] = err

	return result
