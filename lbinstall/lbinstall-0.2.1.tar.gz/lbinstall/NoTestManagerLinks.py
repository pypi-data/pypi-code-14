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

        self.filename = "COMPAT-1.17.0-0.noarch.rpm"
        self.url = "http://lhcbproject.web.cern.ch/lhcbproject/dist/rpm/" \
                   "lhcb/%s" % self.filename
        logging.basicConfig()
        if not os.path.exists(self.filename):
            import urllib
            urllib.urlretrieve(self.url, self.filename)

    def tearDown(self):
        pass

    def testGetGroup(self):
        ''' Check that we can get the group of a given RPM  '''
        pm = PackageManager(self.filename)
        print "RPM Group: %s" % pm.getGroup()
        self.assertEqual(pm.getGroup(), "LHCb", "Could not get group")

    def testExtract(self):
        ''' Check that we can extract a file  '''
        pm = PackageManager(self.filename)
        prefixmap = {pm.getPrefixes()[0]: "/tmp"}
        pm.setrelocatemap(prefixmap)
        pm.extract(prefixmap)
        pm.checkFileSizesOnDisk()
        # pm.removeFiles()

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testFindPackage']
    unittest.main()
