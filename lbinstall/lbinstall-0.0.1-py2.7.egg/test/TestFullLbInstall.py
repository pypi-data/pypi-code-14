'''
Created on 10 Aug 2016

@author: Ben Couturier
'''
import unittest

from lbinstall.Installer import Installer

class Test(unittest.TestCase):


    def setUp(self):
        import os
        import logging
        logging.basicConfig(level=logging.INFO)

        siteroot = "/tmp/siteroot"
        dbpath = "%s/var/lib/db/packages.db" % siteroot
        if os.path.exists(dbpath):
            os.unlink(dbpath)
        self._mgr = Installer(siteroot)

    def tearDown(self):
        pass        
        
    def testInstall(self):
        '''
        test the procedure that queries for the list of packages to install
        ''' 
        plist = self._mgr.remoteFindPackage("BRUNEL_v51r0_x86_64_slc6_gcc49_opt")
        self._mgr.install(plist)
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testFindPackage']
    unittest.main()