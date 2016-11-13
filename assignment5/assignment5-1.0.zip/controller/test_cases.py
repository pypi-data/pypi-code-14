import unittest
from controller import healthdata

#class for creating test cases
class TestingClass(unittest.TestCase):
    # creation of objects to check for various test cases including some corner test cases as well
    def setUp(self):
        self.date_obj1 = healthdata.friend_health_control.get_friends('vaibhav')
    #checking for test case1

    def test_cases1(self):
        self.assertEqual(self.date_obj1, ['gou'])