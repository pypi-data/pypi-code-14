'''
Created on Aug 9, 2016

@author: lben
'''
import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from lbinstall.db.model import *

class Test(unittest.TestCase):


    def setUp(self):
        self.engine = create_engine('sqlite:///:memory:', echo=True)
        Base.metadata.create_all(self.engine)    
        Base.metadata.bind = self.engine
        self.DBSession = sessionmaker(bind=self.engine)

    def tearDown(self):
        pass

    def testAddPackage(self):
        session = self.DBSession()
        
        p = Package(name='PACKAGE1', version="1.0.0", release="1", group="LHCb")
        req = Require(name="REQ_PACKAGE0", version="2.1.2")
        req2 = Require(name="REQ_PACKAGE2", version="1.1.0")
        prov = Provide(name="PROV_PACKAGE1", version="1.0.0")
        p.provides.append(prov)
        p.requires.append(req)
        p.requires.append(req2)
        session.add(p)
        session.commit()
        
        session = self.DBSession()
        packages = session.query(Package).filter_by(name="PACKAGE1").all()
        self.assert_(len(packages) == 1, "There should be one package in the DB called PACKAGE1")
        
        p2 = packages[0]
        for r2 in p2.requires:
            print "REQ: ", r2.name , " ", p2.version
        for r in p2.provides:
            print "PROV:", r.name, " ", r.version

        for p in session.query(Provide).filter(Provide.name == "PROV_PACKAGE1").all():
            print p.name, p.version
            
if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testInsert']
    unittest.main()
