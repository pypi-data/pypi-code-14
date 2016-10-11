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

from lbinstall.db.model import Provide, Require, Package, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import and_
import json
import gzip

from lbinstall.Model import Provides as dmProvides
from lbinstall.Model import Requires as dmRequires


class DBManager:
    '''
    Class that allows interacting with the SQLite DB  containing thelist
    of installed packages.

    '''
    def __init__(self, filename):
        self._filename = filename
        self.log = logging.getLogger(__name__)
        self._filestore = os.path.join(os.path.dirname(filename), "files")
        # Checking if there is a DB already...
        if not os.path.exists(self._filename):
            self.log.warn("Creating new local package DB at %s"
                          % self._filename)
            self.engine = create_engine('sqlite:///%s' % self._filename)
            Base.metadata.create_all(self.engine)
            Base.metadata.bind = self.engine
        else:
            self.engine = create_engine('sqlite:///%s' % self._filename)

        self.DBSession = sessionmaker(bind=self.engine)
        self.session = None

    # File metada storage is list of files on disk
    ################################################################
    def _getFMDataStoreName(self, packagename):
        ''' Returns the path for the file that should contain
        the package file metadata '''
        if packagename is None:
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
            if f is not None:
                f.close()

    def loadFMData(self, name):
        ''' Save the file list  to disk '''
        filename = self._getFMDataStoreName(name)
        ret = None
        # This because in python 2.6 you cannot use
        # with with GzipFile...
        f = None
        try:
            f = gzip.open(filename, "r")
            ret = json.load(f)
        finally:
            if f is not None:
                f.close()
        return ret

    def removeFMData(self, name):
        ''' Save the file list  to disk '''
        filename = self._getFMDataStoreName(name)
        if os.path.exists(filename):
            os.unlink(filename)

    def _getSession(self):
        ''' Return new session if needed '''
        if self.session is None:
            self.session = self.DBSession()
        return self.session

    def addPackage(self, dmpackage, filemetadata):
        '''
        takes a package object from the DependencyManager and stores
        it to the DB. Just matches the two structures, probably can be
        done better need to review those classes in view of the new
        integration of SQLAlchemy...
        '''

        # First saving the metadata in a file...
        self.dumpFMData(dmpackage.rpmName(), filemetadata)
        # Now the DB part
        session = self._getSession()
        pack = Package(name=dmpackage.name,
                       version=dmpackage.version,
                       release=dmpackage.release,
                       group=dmpackage.group,
                       location=dmpackage.location,
                       relocatedLocation=dmpackage.relocatedLocation)

        for r in dmpackage.requires:
            req = Require(name=r.name,
                          version=r.version,
                          flags=r.flags)
            pack.requires.append(req)

        for p in dmpackage.provides:
            prov = Provide(name=p.name,
                           version=p.version,
                           flags=p.flags)
            pack.provides.append(prov)
        session.add(pack)
        session.commit()

    def setPostInstallRun(self, dbpackage, value):
        '''
        Sets the postInstallRunFlag...
        '''
        session = self._getSession()
        matching = session.query(Package) \
                          .filter(and_(Package.name == dbpackage.name,
                                       Package.version == dbpackage.version,
                                       Package.release == dbpackage.release)) \
                          .all()
        matching[0].postinstallrun = value
        # package = session.merge(package) # Didn't work for some reason...
        dbpackage.postinstallrun = value
        session.commit()

    def removePackage(self, dmpackage):
        '''
        takes a package object from the DependencyManager and remove
        the related entries in the DB
        '''
        # Find the DB part
        session = self._getSession()
        matching = session.query(Package) \
                          .filter(and_(Package.name == dmpackage.name,
                                       Package.version == dmpackage.version,
                                       Package.release == dmpackage.release)) \
                          .all()
        # Delete without forgetting provides and requires
        for p in matching:
            for r in p.requires:
                session.delete(r)
            for r in p.provides:
                session.delete(r)
            session.delete(p)
        session.commit()

        # Removing the metadata for the package
        self.removeFMData(dmpackage.rpmFileName())

    def dbStats(self):
        ''' Global DB stats used for tests '''
        session = self._getSession()
        return (session.query(Package).count(),
                session.query(Provide).count(),
                session.query(Require).count())

    def findPackagesWithProv(self, reqname):
        '''
        Return a list of packages providing a specific req
        '''
        session = self._getSession()
        ids = []
        for p in session.query(Provide).filter(Provide.name == reqname).all():
            ids.append(p.package.id)

        ret = []
        for pid in ids:
            for p in session.query(Package).filter(Package.id == pid):
                dmpack = p.toDmPackage()
                for prov in p.provides:
                    dmpack.provides.append(prov.toDmProvides())
                for req in p.requires:
                    dmpack.requires.append(req.toDmRequires())
                ret.append(dmpack)
        return ret

    def findPackagesWithReq(self, reqname):
        '''
        Return a list of packages requiring a specific req
        '''
        session = self._getSession()
        ids = []
        for p in session.query(Require).filter(Require.name == reqname).all():
            ids.append(p.package.id)

        ret = []
        for pid in ids:
            for p in session.query(Package).filter(Package.id == pid):
                dmpack = p.toDmPackage()
                for prov in p.provides:
                    dmpack.provides.append(prov.toDmProvides())
                for req in p.requires:
                    dmpack.requires.append(req.toDmRequires())
                ret.append(dmpack)
        return ret

    def findRequiresByName(self, reqname):
        '''
        Return a list of requirements with a specific name
        The matching is done directly in python
        '''
        session = self._getSession()
        ret = []
        for p in session.query(Require).filter(Require.name == reqname).all():
            ret.append(dmRequires(p.name,
                                  p.version,
                                  p.release,
                                  flags=p.flags))

        return ret

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
                                  flags=p.flags))
        return ret

    # Tool to check whether the DB provides a specific requirement
    # #############################################################################
    def provides(self, requirement):
        '''
        Check if some software provides a specific requirement
        '''
        allprovides = self.findProvidesByName(requirement.name)
        matching = [pr for pr in allprovides if requirement.provideMatches(pr)]

        return len(matching) > 0

    # Listing the installed packages and check whether one is installed
    # #############################################################################
    def isPackagesInstalled(self, p):
        '''
        Check whether a matching package is installed
        '''
        session = self._getSession()
        matching = session.query(Package) \
                          .filter(and_(Package.name == p.name,
                                       Package.version == p.version,
                                       Package.release == p.release)).all()
        return len(matching) > 0

    def listPackages(self, match=None, vermatch=None, relmatch=None):
        '''
        List the triplets name, version, release
        '''
        for p in self.getPackages(match, vermatch, relmatch):
            yield (p.name, p.version, p.release)

    def getPackages(self, match=None, vermatch=None, relmatch=None):
        '''
        Return the packages matching a given name
        '''
        if match is None:
            match = "%"
        else:
            match = match + "%"
        if vermatch is None:
            vermatch = "%"
        if relmatch is None:
            relmatch = "%"

        session = self._getSession()
        for p in session.query(Package) \
                        .filter(and_(Package.name.like(match),
                                     Package.version.like(vermatch),
                                     Package.release.like(relmatch))).all():
            yield p

    # Checking dependencies between installed packages
    # #############################################################################
    def findPackagesRequiringPackage(self, package):
        '''
        Return list of packages depending on this one
        '''
        ret = []
        for p in package.provides:
            corresp_req = dmRequires(p.name, p.version,
                                     p.release, flags=p.flags)

            requiring = set()
            # Look for packages requiring this
            allrequiring = self.findPackagesWithReq(p.name)
            for pack in allrequiring:
                for req in pack.requires:
                    if req.provideMatches(p):
                        requiring.add(pack)
                        break
            self.log.debug("%s packages require %s" % (len(requiring), p.name))
            if len(requiring) > 0:
                # In this case we need to check that nobody else is providing
                # the requirement
                matching = set()
                allproviding = self.findPackagesWithProv(p.name)
                for pack in allproviding:
                    for prov in pack.provides:
                        if corresp_req.provideMatches(prov):
                            matching.add(pack)
                            break
                self.log.debug("Nb packages matching %s: %s"
                               % (p.name, len(matching)))
                if (len(matching) == 1):
                    if (p.name, p.version, p.release) not in \
                       [(v1.name, v1.version, v1.release) for (v1, _) in ret]:
                            self.log.debug("Adding dependency for %s %s %s"
                                           % (p.name, p.version, p.release))
                            ret.append((p, requiring))
        return ret