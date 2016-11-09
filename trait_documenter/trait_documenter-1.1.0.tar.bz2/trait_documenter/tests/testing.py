def is_python_26():
    import sys
    return sys.version_info[:2] == (2, 6)

if is_python_26():
    import unittest2 as unittest
else:
    import unittest

class expected_failure_when(object):

    def __init__(self, condition):
        self.condition = condition

    def __call__(self, function):
        if self.condition:
            return unittest.expectedFailure(function)
        else:
            return function
