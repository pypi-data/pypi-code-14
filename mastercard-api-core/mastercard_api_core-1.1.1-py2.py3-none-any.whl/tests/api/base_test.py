import unittest


class BaseTest(unittest.TestCase):
	responses = {}

	@staticmethod
	def putResponse(name,response):
		BaseTest.responses[name] = response


	@staticmethod
	def resolveResponseValue(overrideValue):
		pos = overrideValue.find('.')

		name = overrideValue[:pos]
		print "Example Name: %s" % name
		key = overrideValue[pos+1:]
		print "Key Name: %s" % key


		if name in BaseTest.responses:
			response = BaseTest.responses[name].getObject()
			if key in response:
				return response[key]
			else:
				print "Key:'%s' is not found in the response" % key
		else:
			print "Example:'%s' is not found in the response" % name

		return None


	def customAssertEqual(self,ignoreAsserts,key, actualValue, expectedValue):
		if (key not in ignoreAsserts):
			self.customAssertValue(expectedValue,actualValue)

	def customAssertValue(self,expected,actual):
		if (isinstance(actual,float)):
			self.assertEqual(float(expected), actual)
		else:
			self.assertEqual(expected.lower(), str(actual).lower())








