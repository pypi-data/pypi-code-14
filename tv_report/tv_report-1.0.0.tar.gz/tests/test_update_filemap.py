import unittest
import os

import tv_report

cur_dir = os.path.abspath(__file__)

class test_update_filemap(unittest.TestCase):
    def test_update_filemap(self):
        data_file = os.path.join(cur_dir, ".test-data-file")
        filemap = {}
        directory = os.path.join(cur_dir, "filemap-test-data")

        expected_filemap = {}

        #filemap = tv_report.update_filemap(data_file, filemap, directory)
        #self.assertEqual(filemap, expected_filemap)
