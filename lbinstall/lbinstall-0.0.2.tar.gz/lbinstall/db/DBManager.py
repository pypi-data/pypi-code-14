###############################################################################
# (c) Copyright 2016 CERN                                                     #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "COPYING".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                       #
###############################################################################
'''
Interface with the installed package and file DB on the local filesystem.
'''
import logging
import os

from lbinstall.db.model import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import and_
import json
import gzip

from lbinstall.Model import Provides as dmProvides

class DBManager:
    '''
    Class that allows interacting with the SQLite DB  containing thelist
    of installed packages.

    '''
    def __init__(self, filename):
        self._filename = filename
        self.log  = logging.getLogger(__name__)
        self._filestore = os.path.join(os.path.dirname(filename), "files")
        # Checking if there is a DB already...
        if not os.path.exists(self._filename):
            self.log.warn("Creating new local package DB at %s" % self._filename)
            self.engine = create_engine('sqlite:///%s' % self._filename)
            Base.metadata.create_all(self.engine)
            Base.metadata.bind = self.engine
        else:
            self.engine = create_engine('sqlite:///%s' % self._filename)

        self.DBSession = sessionmaker(bind=self.engine)
        self.session = None

    def _getFMDataStoreName(self, packagename):
        ''' Returns the path for the file that should contain the package file metadata '''
        if packagename == None:
            raise Exception("Please specify the package name")
        middir = packagename[0].lower()
        return os.path.join(self._filestore, middir, packagename + ".dat.gz")

    def dumpFMData(self, name, filemetadata):
        ''' Save the file list  to disk '''
        filename = self._getFMDataStoreName(name)
        if not os.path.exists(os.path.dirname(filename)):
            os.makedirs(os.path.dirname(filename))

        # This because in python 2.6 you cannot use
        # with with GzipFile...
        try:
            f = gzip.open(filename, "w")
            json.dump(filemetadata, f)
        finally:
            f.close()

    def loadFMData(self, name, filemetadata):
        ''' Save the file list  to disk '''
        filename = self._getFMDataStoreName(name)
        ret = None
        # This because in python 2.6 you cannot use
        # with with GzipFile...
        try:
            f = gzip.open(filename, "r")
            json.load(f)
        finally:
            f.close()
        return ret

    def _getSession(self):
        ''' Return new session if needed '''
        if self.session == None:
            self.session =  self.DBSession()
        return self.session

    def addPackage(self, dmpackage, filemetadata):
        '''
        takes a package object from the DependencyManager and stores
        it to the DB. Just matches the two structures, probably can be done better
        need to review those classes in view of the new integration of SQLAlchemy...
        '''

        # First saving the metadata in a file...
        self.dumpFMData(dmpackage.rpmName(), filemetadata)
        # Now the DB part
        session = self._getSession()
        pack = Package(name=dmpackage.name,
                    version=dmpackage.version,
                    release=dmpackage.release,
                    group=dmpackage.group,
                    location= dmpackage.location)

        for r in dmpackage.requires:
            req = Require(name=r.name,
                          version=r.version,
                          flags = r.flags)
            pack.requires.append(req)

        for p in dmpackage.provides:
            prov = Provide(name=p.name,
                           version=p.version,
                           flags = p.flags)
            pack.provides.append(prov)
        session.add(pack)
        session.commit()

    def setPostInstallRun(self, dbpackage, value):
        '''
        Sets the postInstallRunFlag...
        '''
        session = self._getSession()
        matching = session.query(Package).filter(and_(Package.name == dbpackage.name,
                                                      Package.version == dbpackage.version,
                                                      Package.release == dbpackage.release)).all()       
        matching[0].postinstallrun = value
        #package = session.merge(package) # Didn't work for some reason...
        dbpackage.postinstallrun = value
        session.commit()

    def findProvidesByName(self, reqname):
        '''
        Return a list of requirements with a specific name
        The matching is done directly in python
        '''
        session = self._getSession()
        ret = []
        for p in session.query(Provide).filter(Provide.name == reqname).all():
            ret.append(dmProvides(p.name,
                                  p.version,
                                  p.release,
                                  flags = p.flags))

        return ret

    # Tool to check whether the DB provides a specific requirement
    # #############################################################################
    def provides(self, requirement):
        '''
        Check if some software provides a specific requirement
        '''
        allprovides = self.findProvidesByName(requirement.name)
        matching = [ pr for pr in allprovides if requirement.provideMatches(pr)]

        return len(matching) > 0

    # Listing the installed packages and check whether one is installed
    # #############################################################################
    def isPackagesInstalled(self, p):
        '''
        Check whether a matching package is installed
        '''
        session = self._getSession()
        matching = session.query(Package).filter(and_(Package.name == p.name,
                                                      Package.version == p.version,
                                                      Package.release == p.release)).all()
        return len(matching) > 0

    def listPackages(self, match=None, vermatch=None, relmatch=None):
        '''
        List the package installed matching a given name
        '''

        if match == None:
            match = "%"
        if vermatch==None:
            vermatch = "%"
        if relmatch == None:
            relmatch = "%"

        session = self._getSession()
        for p in session.query(Package).filter(and_(Package.name.like(match),
                                                    Package.version.like(vermatch),
                                                    Package.release.like(relmatch))).all():
            yield p.name, p.version, p.release

