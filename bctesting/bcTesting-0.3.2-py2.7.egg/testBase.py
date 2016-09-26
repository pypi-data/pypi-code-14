""" Module contains the base class for the testing of core python modules/functions.
"""
import fixtures
import mox
import testtools


class TestCase(testtools.TestCase):
	""" Base class for bcTesting project.
	"""

	def setUp(self):
		""" Method called to prepare the test fixture. This is
		called immediately before calling the test method;
		other than AssertionError or SkipTest, any exception
		raised by this method will be considered an error rather
		than a test failure. The default implementation does nothing
		"""
		super(TestCase, self).setUp()
		self._mox = mox.Mox()

	def tearDown(self):
		""" Method called immediately after the test method has been
		called and the result recorded.
		"""
		super(TestCase, self).tearDown()
		self._mox.UnsetStubs()

	@property
	def mox(self):
		""" Getter method for mox object of TestCase class.

			Return:
				(mox.Mox) mox object of the class.
		"""
		return self._mox

	def monkeyPatch(self, objectName, value):
		""" Method to monkey patch a function or variable of a module
		uses fixtures.MonkeyPatch for this.

		Replace the original with the vlaue given.

		Args:
			objectName (str): Name of the object/function/variable.
			value (type): Any type of value that will replace the original.
		"""
		self.useFixture(fixtures.MonkeyPatch(objectName, value))

	def monkeyPatchObject(self, obj, name, value):
		""" Method to monkey patch a function or variable of a class
		uses fixtures.MockPatchObject for this.

		Replace the original with the vlaue given.

		Args:
			obj (type): Any type of object
			name (str): Name of the object/function/variable.
			value (type): Any type of value that will replace the original.
		"""
		# Renaming the pirvate function/variables to "_object__name" format
		if name.startswith("__"):
			className = obj.__class__.__name__
			name = "_%s%s" % (className, name)

		self.useFixture(fixtures.MockPatchObject(obj, name, value))

	def monkeyPatchEnvironment(self, environment, value):
		""" Method to monkey patch the environment variables.
		Uses fixtures.EnvironmentVariable foor this.

		Replace the existing value with the given new value

		Args:
			environment (str): Name of environment variable.
			value (str): String value that will replace the original.
		"""
		self.useFixture(fixtures.EnvironmentVariable(environment, value))

	def assertType(self, obj, cls):
		""" Method to compare the type of the object and given class
		using isinstance funtion of python. If the object is not of
		cls type raise AssertionError

		Args:
			obj (type): Expecting the object of cls type
			cls (type/list): A class or list of classes derived from type

		Raises:
			AssertionError: An error occurs when the object is not of cls type.
		"""
		if not isinstance(obj, cls):
			raise AssertionError("Object (%r) is not a type of %r" % (obj, cls))
