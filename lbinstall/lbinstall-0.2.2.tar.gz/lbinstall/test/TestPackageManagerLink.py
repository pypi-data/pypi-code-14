'''
Created on 10 Aug 2016

@author: Ben Couturier
'''
import os
import unittest
import logging

from lbinstall.PackageManager import PackageManager


class Test(unittest.TestCase):

    def setUp(self):

        self.filename = "LBSCRIPTS_v8r7-1.0.0-1.noarch.rpm"
        self.url = "http://lhcbproject.web.cern.ch/lhcbproject/"\
                   "dist/rpm/lhcb/%s" % self.filename
        logging.basicConfig()
        if not os.path.exists(self.filename):
            import urllib
            urllib.urlretrieve(self.url, self.filename)

    def tearDown(self):
        pass

    def testHardLinks(self):
        ''' Checks the method that returns the list of files'''
        pm = PackageManager(self.filename)
        res = pm.getFileMetadata()
        from pprint import pprint
        pprint(res)
        
if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testFindPackage']
    unittest.main()
