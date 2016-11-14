__date__ = "4/9/16"
__author__ = "Sharon Lev"
__email__ = "sharon_lev@yahoo.com"

from unittest import TestCase
from src.unittestextras import DataProvider, DataSet

class TestDataProvider(TestCase):
  """
  test data driven tests functionality
  """
  class decorated_class(object):

    _cause_error_at_setup = False
    _cause_error_in_test = False
    _raise_assertion_in_test = False
    _setup_count = 0
    _method_count = 0
    _tear_down_count = 0

    def setUp(self):
      print 'setup',
      self._setup_count += 1
      if self._cause_error_at_setup: raise IOError("generic setup error")

    def tearDown(self):
      print 'teardown'
      self._tear_down_count += 1

    data_dict = DataSet(
      dict(key1=1, key2=2),
      dict(key1=3, key2=4)
    )

    data_list = DataSet(
      [1,2,3],
      [4,5,6]
    )

    data_strings = DataSet(
      "string_1",
      "string_2"
    )

    @DataProvider(data_dict)
    def dict_driven_method(self, key1, key2):
      print key1, key2,
      if self._cause_error_in_test: raise IOError("generic test error")
      assert not self._raise_assertion_in_test , "generic assertion error"
      self._method_count += 1

    @DataProvider(data_dict, id_key='key2')
    def dict_driven_method_with_key(self, key1, key2):
      print key1, key2,
      if self._cause_error_in_test: raise IOError("generic test error")
      assert not self._raise_assertion_in_test , "generic assertion error"
      self._method_count += 1


    @DataProvider(data_list)
    def list_driven_method(self, a, b, c):
      print a, b, c,
      if self._cause_error_in_test: raise IOError("generic test error")
      assert not self._raise_assertion_in_test , "generic assertion error"
      self._method_count += 1

    @DataProvider(data_list, id_index=2)
    def list_driven_method_with_index(self, a, b, c):
      print a, b, c,
      if self._cause_error_in_test: raise IOError("generic test error")
      assert not self._raise_assertion_in_test , "generic assertion error"
      self._method_count += 1

    @DataProvider(data_strings)
    def string_driven_method(self, a_string):
      print a_string,
      if self._cause_error_in_test: raise IOError("generic test error")
      assert not self._raise_assertion_in_test , "generic assertion error"
      self._method_count += 1


  def setUp(self):
    self.test_class = self.decorated_class()


  def test__dict_driven_testing(self):
    """
    validate that all sets containing dict are fed to 'test' method
    """
    self.test_class.setUp()
    self.test_class.dict_driven_method()
    self.test_class.tearDown()
    for counter in [self.test_class._method_count, self.test_class._setup_count, self.test_class._tear_down_count]:
      self.assertEqual(counter, 2)


  def test__list_driven_testing(self):
    """
    validate that all sets containing list are fed to 'test' method
    """
    self.test_class.setUp()
    self.test_class.list_driven_method()
    self.test_class.tearDown()
    for counter in [self.test_class._method_count, self.test_class._setup_count, self.test_class._tear_down_count]:
      self.assertEqual(counter, 2)


  def test__string_driven_testing(self):
    """
    validate that all sets containing primitive are fed to 'test' method
    """
    self.test_class.setUp()
    self.test_class.string_driven_method()
    self.test_class.tearDown()
    for counter in [self.test_class._method_count, self.test_class._setup_count, self.test_class._tear_down_count]:
      self.assertEqual(counter, 2)


  def test__raise_error_in_setup(self):
    """
    validate that errors raised in setUp are not breaking the cycle
    """
    self.test_class.setUp()
    self.test_class._cause_error_at_setup = True
    assertion = None
    try:
      self.test_class.string_driven_method()
    except Exception, e:
      assertion = e

    self.assertIsInstance(e, Exception)


  def test__raise_error_in_test(self):
    """
    validate that errors in test cases are tracked in results properly
    """
    self.test_class.setUp()
    self.test_class._cause_error_in_test = True
    assertion = False
    try:
      self.test_class.string_driven_method()
    except Exception, e:
      print type(e.message), e.message
      assertion = e

    self.assertIsInstance(assertion, Exception)
    self.assertEqual(len(assertion.errors), 2, assertion.errors)

  def test__raise_assertion_in_test(self):
    """
    validate that assertion in test cases (test failures) are tracked in results properly, and by default listed by passed set index
    """
    self.test_class.setUp()
    self.test_class._raise_assertion_in_test = True
    assertion = False
    try:
      self.test_class.string_driven_method()
    except AssertionError, e:
      print type(e.message), e.message
      assertion = e

    self.assertIsInstance(assertion, AssertionError)
    self.assertEqual(len(assertion.failures), 2)
    self.assertTrue(all(id in assertion.message for id in ['Data set [%d]:' % i for i in range(2)]), 'could not locate proper indexes for failed tests')

  def test_assert_by_key(self):
    """
    validate that passed id keys result in properly keyed/taged failures per data set
    """
    self.test_class.setUp()
    self.test_class._raise_assertion_in_test = True
    assertion = False
    try:
      self.test_class.dict_driven_method_with_key()
    except AssertionError, e:
      print type(e.message), e.message
      assertion = e

    self.assertTrue(all(id in assertion.message for id in ['Data set [%d]:' % i for i in [2, 4]]), 'could not locate proper keys for failed tests')

  def test_assert_by_index(self):
    """
    validate that passed id indices result in properly indexed/taged failures per data set
    """
    self.test_class.setUp()
    self.test_class._raise_assertion_in_test = True
    assertion = False
    try:
      self.test_class.list_driven_method_with_index()
    except AssertionError, e:
      print type(e.message), e.message
      assertion = e

    self.assertTrue(all(id in assertion.message for id in ['Data set [%d]:' % i for i in [3, 6]]), 'could not locate proper indexes for failed tests')
