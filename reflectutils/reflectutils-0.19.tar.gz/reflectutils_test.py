import os
import numpy
import unittest

import Queue
import UserDict

import reflectutils

import django
import django.conf
from django.db.models.query import QuerySet



class Foo(object):
	"""A mock class"""
	def bar(self):
		"""Does nothing"""
		pass


class TypeutilsTest(unittest.TestCase):
	def test_classify(self):
		f = Foo()
		self.assertEqual(reflectutils.classify(f), "object")
		self.assertEqual(reflectutils.classify(Foo), "type")
		self.assertEqual(reflectutils.classify(reflectutils), "module")
		self.assertEqual(reflectutils.classify(Foo.bar), "function")
		self.assertEqual(reflectutils.classify(f.bar), "function")

	def test_classify_builtins(self):
		self.assertEqual(reflectutils.classify(str), "type")
		self.assertEqual(reflectutils.classify(str.join), "function")
		self.assertEqual(reflectutils.classify(type(str.join)), "type")
		self.assertEqual(reflectutils.classify(os), "module")
		self.assertEqual(reflectutils.classify(object), "type")
		self.assertEqual(reflectutils.classify(type), "type")

	def test_classify_numpy(self):
		self.assertEqual(reflectutils.classify(numpy), "module")
		self.assertEqual(reflectutils.classify(numpy.ndarray), "type")
		self.assertEqual(reflectutils.classify(numpy.ndarray.sum), "function")
		self.assertEqual(reflectutils.classify(numpy.zeros), "function")

	def type_fullname_from_str(self):
		s = "<subprocess.Popen at 0x105630bd0>"
		self.assertEqual(reflectutils.fullname_from_str(s), "subprocess.Popen")

		s = "<built-in method search of _sre.SRE_Pattern object at 0x105648558>"
		self.assertEqual(reflectutils.fullname_from_str(s), "_sre.SRE_Pattern.search")

		s = "<method 'search' of '_sre.SRE_Pattern' objects>"
		self.assertEqual(reflectutils.fullname_from_str(s), "_sre.SRE_Pattern.search")

		s = "<method 'flush' of 'file' objects>"
		self.assertEqual(reflectutils.fullname_from_str(s), "__builtin__.file.flush")

		s = "<bound method Popen.kill of <subprocess.Popen object at 0x1056309d0>>"
		self.assertEqual(reflectutils.fullname_from_str(s), "subprocess.Popen.kill")

		s = "<unbound method Popen.kill>"
		self.assertEqual(reflectutils.fullname_from_str(s, pkg="subprocess"), "subprocess.Popen.kill")

		s = "<attribute 'ndim' of 'numpy.ndarray' objects>"
		self.assertEqual(reflectutils.fullname_from_str(s), "numpy.ndarray.ndim")

		s = "<bound method Queue.put of <Queue.Queue instance at 0x101d811b8>>"
		self.assertEqual(reflectutils.fullname_from_str(s, pkg="Queue"), "Queue.Queue.put")

	def test_name_boundmethod(self):
		self.assertEqual(reflectutils.name_boundmethod(Queue.Queue().put), "Queue.put")
		self.assertEqual(reflectutils.name_boundmethod(UserDict.UserDict().popitem), "UserDict.popitem")

	def test_fullname(self):
		f = Foo()
		self.assertEqual(reflectutils.fullname(unittest), "unittest")
		self.assertEqual(reflectutils.fullname(unittest.TestCase), "unittest.case.TestCase")
		self.assertEqual(reflectutils.fullname(unittest.TestCase.assertEqual), "unittest.case.TestCase.assertEqual")
		self.assertEqual(reflectutils.fullname(1), None)
		self.assertEqual(reflectutils.fullname(Queue.Queue().put), "Queue.Queue.put")
		self.assertEqual(reflectutils.fullname(UserDict.UserDict().popitem), "UserDict.UserDict.popitem")

	def test_fullname_django(self):
		 # this ensures that django has a settings module and an app
		django.conf.settings.configure()
		django.setup()
		self.assertEqual(reflectutils.fullname(QuerySet()), None)

	def test_fullname_builtins(self):
		self.assertEqual(reflectutils.fullname(str), "__builtin__.str")
		self.assertEqual(reflectutils.fullname(str.join), "__builtin__.str.join")
		self.assertEqual(reflectutils.fullname(type(str.join)), "__builtin__.method_descriptor")
		self.assertEqual(reflectutils.fullname(os), "os")
		self.assertEqual(reflectutils.fullname(object), "__builtin__.object")
		self.assertEqual(reflectutils.fullname(type), "__builtin__.type")

	def test_fullname_descriptor(self):
		import numpy
		self.assertEqual(reflectutils.fullname(numpy.ndarray.ndim), "numpy.ndarray.ndim")

	def test_package(self):
		f = Foo()
		self.assertEqual(reflectutils.package(unittest), "unittest")
		self.assertEqual(reflectutils.package(unittest.TestCase), "unittest.case")
		self.assertEqual(reflectutils.package(unittest.TestCase.assertEqual), "unittest.case")
		self.assertEqual(reflectutils.package(1), None)

	def test_doc(self):
		self.assertEqual(reflectutils.doc(Foo), "A mock class")
		self.assertEqual(reflectutils.doc(Foo.bar), "Does nothing")
	
	def test_isboundmethod(self):
		self.assertTrue(reflectutils.isboundmethod("".format))
		self.assertFalse(reflectutils.isboundmethod(len))
		self.assertTrue(reflectutils.isboundmethod({}.update))
		self.assertTrue(reflectutils.isboundmethod(getattr(os.confstr_names, "items")))
