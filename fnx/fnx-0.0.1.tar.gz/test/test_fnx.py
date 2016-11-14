import unittest
import datetime

import fnx

class BasicTest(unittest.TestCase):
    def test_xirr(self):

        test_dates = [datetime.date(2010, 12, 29), datetime.date(2012, 1, 25), datetime.date(2012, 3, 8)]
        test_values = [-10000, 20, 10100]

        result = 0.010061265164920336

        self.assertEqual(fnx.xirr(test_values, test_dates), result)

if __name__ == '__main__':
    unittest.main()
