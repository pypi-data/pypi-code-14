import unittest
import tempfile
from should_dsl import *
from options.Prefs import Prefs

class PrefsTest(unittest.TestCase):
	def setUp(self):
		self.prefs = Prefs()

	def tests_if_prefs_is_an_singleton_class(self):
		new_instance_of_prefs = Prefs() #creates a new instance of press, this instance will have the same value of self.prefs

		key_shared_between_the_instances = "foo"
		value_shared_between_the_instances = "bar"

		self.prefs.set_setting(key_shared_between_the_instances, value_shared_between_the_instances)
		new_instance_of_prefs.myprefs[key_shared_between_the_instances] |should| equal_to(value_shared_between_the_instances)

	def test_if_set_an_setting(self):
		self.prefs.set_setting("teste","teste")
		self.prefs.myprefs["teste"] |should| equal_to("teste")

	def test_if_get_a_setting(self):
		self.prefs.set_setting("foo","bar")
		self.prefs.get_setting("foo") |should| equal_to("bar")
