import unittest
import reflectutils
import inspect

obj = unittest.TestCase.assertEqual
print obj
print "ismethod:", inspect.ismethod(obj)
print "isboundmethod:", reflectutils.isboundmethod(obj)
print reflectutils.fullname(obj)