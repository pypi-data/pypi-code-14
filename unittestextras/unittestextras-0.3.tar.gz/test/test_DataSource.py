__date__ = "4/9/16"
__author__ = "Sharon Lev"
__email__ = "sharon_lev@yahoo.com"

from os.path import join, dirname
from unittest import TestCase, TestLoader, TextTestRunner
from src.unittestextras import DataProvider, DataSource

class Counters(object):
  iterations = 0
  values = []
  def __init__(self, iterations, values):
    self.iterations = iterations
    self.values = values
global counters

loaded_iterations = [3]
loaded_values = [1,2,3,4,5,6]

class TestDataSource(TestCase):

  class mock_test_class_json(TestCase):

    @DataProvider(DataSource(join(dirname(__file__), 'resources/test_a.json')))
    def test_TestDataJson(self, key1, key2):
      print key1, key2,
      counters.iterations -= 1
      for key in [key1, key2]:
        counters.values.remove(key)

  class mock_test_class_json_list(TestCase):

    @DataProvider(DataSource(join(dirname(__file__), 'resources/test_a_list.json')))
    def test_TestDataJson(self, key1, key2):
      print key1, key2,
      counters.iterations -= 1
      for key in [key1, key2]:
        counters.values.remove(key)

  class mock_test_class_plist(TestCase):

    @DataProvider(DataSource(join(dirname(__file__), 'resources/test_a.plist')))
    def test_TestDataJson(self, key1, key2):
      print key1, key2,
      counters.iterations -= 1
      for key in [key1, key2]:
        counters.values.remove(key)

  def test__json_source(self):
    global counters
    counters = Counters(3, [1, 2, 3, 4, 5, 6])
    suite = TestLoader().loadTestsFromTestCase(self.mock_test_class_json)
    results = TextTestRunner().run(suite)
    print results
    self.assertEqual(counters.iterations, 0)
    self.assertEqual(counters.values, [])

  def test__json_list_source(self):
    global counters
    counters = Counters(3, [10, 20, 30, 40, 50, 60])
    suite = TestLoader().loadTestsFromTestCase(self.mock_test_class_json_list)
    results = TextTestRunner().run(suite)
    print results
    self.assertEqual(counters.iterations, 0)
    self.assertEqual(counters.values, [])

  def test__plist_source(self):
    global counters
    counters = Counters(3, [1, 2, 3, 4, 5, 6])
    suite = TestLoader().loadTestsFromTestCase(self.mock_test_class_plist)
    results = TextTestRunner().run(suite)
    print results
    self.assertEqual(counters.iterations, 0)
    self.assertEqual(counters.values, [])
