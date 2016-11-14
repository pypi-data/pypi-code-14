__author__ = 'Sharon lev'
__email__ = 'sharon_lev@yahoo.com'
__date__ = '8/31/15 16:19'


def DataProvider(data_set, id_key=None, id_index=None):
  """
  Data provider decorator, allows another callable to provide the data for the test

  :param data_set: a DataSet instance that can provide sets of data as expected by the test method decorated
  :param id_key: optional key to use for reporting failures
  :param id_index: optional index of argument to use for reporting failures
  """
  def test_decorator(test_method):
    def decorated(self, *args, **kwargs):
      firstCall = True
      lastrun = sum(1 for _ in data_set()) - 1
      failures = []
      errors = []
      for counter, args in enumerate(data_set()):
        try:
          if not firstCall: self.setUp()
          firstCall = False

          if isinstance(args, dict): test_method(self, **args)
          elif isinstance(args, list): test_method(self, *args)
          else: test_method(self, args)

        except AssertionError as AE:
          if hasattr(self, 'logger'): self.logger.error(AE)
          failures.append(str(explicit_exception(AE, args, id_key, id_index, counter).message))
        except Exception as err:
          if hasattr(self, 'logger'): self.logger.error(err)
          errors.append((str(explicit_exception(err, args, id_key, id_index, counter).message)))

        if (counter < lastrun):
          self.tearDown()

      #after running all datasets:
      if len(errors) > 0:
        ex = Exception('The following errors occured: {}'.format(str(errors + failures)))
        ex.errors = errors
        ex.failures = failures
        raise ex
      if len(failures) > 0:
        assertion = AssertionError('The following Assertions occurred: {}'.format(str(failures)))
        assertion.errors = []
        assertion.failures = failures
        raise assertion
    return decorated
  return test_decorator

def explicit_exception(exception, args, id_key, id_index, id):
  """
  rename exception message with explicit ID to make it easier to identify failures to data sets
  :param exception: an Exception instance
  :param args: test args set
  :return: updated Exception with explicit message
  """
  try:
    id = args[id_key] if id_key else args[id_index] if id_index else id
  except:
    id = id

#  if isinstance(args, dict) and 'DataProviderSetID' in args: id = args['DataProviderSetID']
  exception.message = 'Data set [%s]: %s' % (id, exception.message)
  return exception