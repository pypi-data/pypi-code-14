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
        logging.basicConfig(level=logging.DEBUG)
        siteroot = "/tmp/siteroot"
        dbpath = "%s/var/lib/db/packages.db" % siteroot
        if os.path.exists(dbpath):
            os.unlink(dbpath)
        self._mgr = Installer(siteroot)

    def tearDown(self):
        pass

    def testFindProvides(self):
        ''' Check that we can filter the list of provides in the DB '''
        ps = list(self._mgr.remoteListProvides("BRUNEL_v51r0"))
        self.assertEqual(len(ps), 11, "Checking the number of provides for BRUNEL v51r0")

    def testFindDeps(self):
        '''  Check we can locate a package and its dependencies '''
        packages = self._mgr.remoteFindPackage("BRUNEL_v51r0_x86_64_slc6_gcc49_opt")
        for p in packages:
            url = p.url()
            refurl = "http://lhcbproject.web.cern.ch/lhcbproject/dist/rpm/lhcb/BRUNEL_v51r0_x86_64_slc6_gcc49_opt-1.0.0-1.noarch.rpm"
            self.assertEqual(url, refurl, "Is package URL correct")
            
    def testListPackages(self):
        '''  Test the list of packages '''
        packages = self._mgr.remoteListPackages("BRUNEL_v51r0")
        self.assertEquals(len(list(packages)), 9, "Check that we have 7 packages for v51r0")

    def testListpackagesToInstall(self):
        '''
        test the procedure that queries for the list of packages to install
        ''' 
        plist = self._mgr.remoteFindPackage("BRUNEL_v51r0_x86_64_slc6_gcc49_opt")
        p = plist[0]
                    
        toinstall =  self._mgr._getPackagesToInstall(p)
        print len(toinstall)
        self.assertEqual(len(toinstall), 125, "Brunel v51r0 requires 125 packages on an empty DB")
        
        # Now faking the insertion of xapian-e16be_1.2.21_x86_64_slc6_gcc49_opt
        from lbinstall.DependencyManager import Provides, Package
        xapname = "xapian-e16be_1.2.21_x86_64_slc6_gcc49_opt"
        xapver = "1.0.0"
        xaprel = "1"
        self._mgr._localDB.addPackage(Package(xapname, xapver, xaprel, group="LCG", \
                                                provides= [Provides(xapname, xapver, xaprel) ]))
        toinstall =  self._mgr._getPackagesToInstall(p)
        print len(toinstall)
        self.assertEqual(len(toinstall), 124, "Brunel v51r0 requires 124 packages when xapian is there")
        
        # Now faking the insertion of the whole of LCG plus LHCb up to REC:

        for xapname in ["LCG_84_Python_2.7.10_x86_64_slc6_gcc49_opt",
                  "LCG_84_HepMC_2.06.09_x86_64_slc6_gcc49_opt",
                  "LCGCMT_LCGCMT_84",
                  "REC_v20r0_x86_64_slc6_gcc49_opt",]:
            
            xapver = "1.0.0"
            xaprel = "1"
            self._mgr._localDB.addPackage(Package(xapname, xapver, xaprel, group="LHCb", \
                                                provides= [Provides(xapname, xapver, xaprel) ]))
        
        toinstall =  self._mgr._getPackagesToInstall(p)
        print len(toinstall)
        from pprint import pprint 
        pprint( [p.name for p in toinstall])
        self.assertEqual(len(toinstall), 13, "At this point 13 packages should be needed")
        
                

        
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testFindPackage']
    unittest.main()