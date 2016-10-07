#!/usr/bin/env python3
"""
this is the mongo DB version of viewModelDB.
import as ViewModelDB

provides a 'baseDB' object as a connection to mongo.
baseDB.db is the access to the database
This could be upgraded to provide fault tolerance in future.
"""
import pymongo
def key(fld):
    #if sqlA return fld.key
    return fld.split('.',1)[1] #for MongoDB
def pclass(fld):
    #if sqlA return fld.key
    return fld.split('.',1)[0] #for MongoDB
class ViewModelDB:
    """ this class manages the mongo connections"""
    def __init__(self,site):
        """ site expecting an ObjDict (but object will quack right now)
            None is the setting to use localhost
        """
        self.dbserver= getattr(site,'dbserver',None)
        self.dbname= getattr(site,'dbname',None)
        if hasattr(site,'dbserver'):
            self._make_con(self.dbserver,self.dbname)

    def _make_con(self,dbserver,dbname):
        print('make con',dbname)
        self.con=pymongo.MongoClient(dbserver)
        if dbname:
            self.db=self.con.get_database(dbname)

    def connect(self,site):
        self.dbserver= getattr(site,'dbserver',self.dbserver)
        self.dbname= getattr(site,'dbname',self.dbname)
        self._make_con(self.dbserver,self.dbname)

try:
    import siteSettings.site as site
except ImportError:
    site= object() #ObjDict(dbserver=False,dbname=None)
#else:
#    engstr= site.dbserver
#    dbstr=site.dbname
baseDB=ViewModelDB(site)
print("loaded modeldb")
