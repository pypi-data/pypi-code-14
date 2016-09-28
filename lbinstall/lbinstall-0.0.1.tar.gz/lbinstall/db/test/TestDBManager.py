'''
Created on Aug 9, 2016

@author: lben
'''
import unittest

from lbinstall.db.DBManager import DBManager

class Test(unittest.TestCase):


    def setUp(self):
        self.db = DBManager(':memory:')

    def tearDown(self):
        pass

    def testAddPackage(self):
        
        from lbinstall.DependencyManager import Package as dmPackage
        from lbinstall.DependencyManager import Provides as dmProvides
        from lbinstall.DependencyManager import Requires as dmRequires
        
        provides = [ dmProvides("P1", "1.0.0", "1"), dmProvides("P", None, None)]
        requires = [ dmRequires("P0", "4.2.0", "1")]
        p1 = dmPackage("P1", "1.0.0", "1", group = "LHCb")
        for t in provides:
            p1.provides.append(t)        
        for t in requires:
            p1.requires.append(t)        
        self.db.addPackage(p1)
        
        p2 = dmPackage("P2", "1.0.0", "1", group = "LHCb")                
        for t in [ dmProvides("P2", "1.0.0", "1"), dmProvides("P", None, None)]:
            p2.provides.append(t)
            
        for t in [ dmRequires("P1", "1.0.0", "1")]:
            p2.requires.append(t)            
        self.db.addPackage(p2)
        
        test = self.db.findProvidesByName("P")
        self.assertEquals(len(list(test)), 2, "Make sure two packages provide P")
            
if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testInsert']
    unittest.main()
