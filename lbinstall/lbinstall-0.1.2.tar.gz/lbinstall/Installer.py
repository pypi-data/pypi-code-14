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
Installer for the for LHCb Software.
All it needs is the name of a local directory to use to setup the install area
and the yum repository configuration.

@author: Ben Couturier
'''
import logging
import os
import sys
import traceback
from os.path import abspath

from lbinstall.InstallAreaManager import InstallArea
from lbinstall.PackageManager import PackageManager


# Little util to find a file in a directory tree
def findFileInDir(basename, dirname):
    ''' Look for a file with a given basename in a
    directory struture.
    Returns the first file found... '''
    for root, _, files in os.walk(dirname, followlinks=True):
        if basename in files:
            return abspath(os.path.join(root, basename))
    return None


class Installer(object):
    '''
    LHCb Software installer.
    This class can be used to query the remote YUM database,
    and to install packages on disk.
    It create the InstallArea files needed for the installation.
    You can create it either:

    * Passing the siteroot of the Installation, in which case the
    repositories are setup to the default LHCb ones

    * Passing a full InstallAreaConfig as the named parameter config,
    in which case all customizations are possible (by specifying the configType
    parameter). A class like LHCbConfig.py must be created in that case...
    '''

    def __init__(self, siteroot, config=None,
                 localRPMcache=None, disableYumCheck=False):
        '''
        Class to install a set of packages to a specific area
        '''
        self.log = logging.getLogger(__name__)
        self._siteroot = os.path.abspath(siteroot)
        self._lcgDir = os.path.join(self._siteroot, "lcg")
        if config is None:
            from lbinstall.LHCbConfig import Config
            config = Config()
        self._config = config

        # Creating the install area and getting the relevant info
        self.__installArea = InstallArea(self._config, self._siteroot)
        self._lbYumClient = self.__installArea \
                                .createYumClient(not disableYumCheck)
        self._localDB = self.__installArea.createDBManager()
        self._relocateMap = self.__installArea.getRelocateMap()
        self._tmpdir = self.__installArea.getTmpDir()
        self._localRPMcache = []
        if localRPMcache is not None:
            self._localRPMcache = localRPMcache

    # Various utilities to query the yum database
    # ############################################################################
    def remoteListProvides(self, nameRegexp):
        """ List provides matching in the remote repo """
        return self._lbYumClient.listProvides(nameRegexp)

    def remoteFindPackage(self, name, version=None, release=None):
        from Model import Requires
        req = Requires(name, version, release, None, "GE", None)
        pack = self._lbYumClient.findLatestMatchingRequire(req)

        res = [pack] if pack is not None else []
        return res

    def listDependencies(self, package):
        ''' Return the list of dependencies of a given package '''
        return self._getPackagesToInstall(package, ignoreInstalled=True)

    def remoteListPackages(self, nameRegexp=None,
                           versionRegexp=None,
                           releaseRegexp=None):
        packages = self._lbYumClient.listPackages(nameRegexp,
                                                  versionRegexp,
                                                  releaseRegexp)
        return packages

    # Queries to the local DB
    # ############################################################################3
    def localListPackages(self, nameRegexp=None,
                          versionRegexp=None,
                          releaseRegexp=None):
        packages = self._localDB.listPackages(nameRegexp,
                                              versionRegexp,
                                              releaseRegexp)
        return packages

    # Installation routines
    # ############################################################################3
    def install(self, packagelist,
                justdb=False,
                overwrite=False,
                nodeps=False):
        '''
        Installation procedure, it takes a list of package objects...
        '''
        if not packagelist:
            raise Exception("Please specify one or more packages to install")

        # Looking for the files to install
        rpmtoinstall = list()
        if not nodeps:
            for p in packagelist:
                rpmtoinstall += self._getPackagesToInstall(p)
        else:
            rpmtoinstall = packagelist

        # Deduplicating in case some package were there twice
        # but keep the order...
        # There might be two as we take list of packages,
        # and getPackagesToInstall is called multiple
        # times...
        rpmtoinstalldeduprev = []
        for p in rpmtoinstall:
            if p not in rpmtoinstalldeduprev:
                rpmtoinstalldeduprev.append(p)

        # Now downloading
        self.log.warning("%s RPM files to install" % len(rpmtoinstalldeduprev))
        filestoinstall = []
        for package in rpmtoinstalldeduprev:
            localcopy = self._findFileLocally(package)
            if localcopy is not None:
                self.log.info("Using file %s from cache" % localcopy)
                filestoinstall.append((localcopy, True))
            else:
                downloadres = self._downloadfiles([package])
                filestoinstall.append((downloadres[0], False))

        # And installing...
        # We should deal with the order to avoid errors in case of problems
        # Half waythrough XXX
        filesinstalled = []
        # Taking reverse order to start with those
        # that haven't been installed yet
        for (rpm, inLocalCache) in filestoinstall[::-1]:
            self._installpackage(rpm, justdb=justdb,
                                 overwrite=overwrite,
                                 removeAfterInstall=(not inLocalCache))
            filesinstalled.append(rpm)

        if len(filesinstalled) > 0:
            self.log.info("Installed:")
            for f in filesinstalled:
                self.log.info(os.path.basename(f))
        else:
            self.log.info("Nothing Installed")

    def _findInExtrapackages(self, req, extrapackages):
        ''' Util function to check if a package scheduled
        to be installed already fulfills a given requirement '''
        for extrap in extrapackages:
            if extrap.fulfills(req):
                return extrap
        return None

    def _getPackagesToInstall(self, p,
                              extrapackages=None,
                              extrainfo=None,
                              ignoreInstalled=False):
        '''
        Proper single package installation method
        '''
        # Setting up data if needed
        if extrapackages is None:
            extrapackages = set()

        if extrainfo is None:
            from collections import defaultdict
            extrainfo = defaultdict(list)

        # Checking if the package is already there..
        if self._localDB.isPackagesInstalled(p):
            self.log.warning("%s already installed" % p.rpmName())
            return []

        # We are planning to install p, so its provides are now a granted
        extrapackages.add(p)
        toinstall = [p]
        # Iterating though the reuired packages, first checking
        # what's already on the local filesystem...
        for req in p.requires:
            # First checking that one of the packages already s
            # chedules for install do not already provide the package...
            tmp = self._findInExtrapackages(req, extrapackages)
            if tmp is not None:
                self.log.debug("%s already fulfilled by %s, to be installed"
                               % (str(req), tmp.name))

            elif not ignoreInstalled and self._localDB.provides(req):
                # Now checking whether the package isn't already installed...
                self.log.warning("%s already available on local system"
                                 % str(req))
                extrainfo["alreadyInstalled"].append(req)
            else:
                # Ok lets find in from YUM now...
                match = self._lbYumClient.findLatestMatchingRequire(req)
                if match and match not in extrapackages:
                    toinstall += self._getPackagesToInstall(match,
                                                            extrapackages,
                                                            extrainfo)
        return toinstall

    def _installpackage(self, filename, removeAfterInstall=True,
                        justdb=False, overwrite=False):
        ''' To install a RPM and record the info in the local DB'''
        # The PackageManager responsible for dealing
        # with the local package file
        pm = PackageManager(filename, self._relocateMap)
        # DBManager to update local DB
        db = self._localDB
        # Metadata associated with the RPM
        dbp = pm.getPackage()
        try:
            # Now extract the file to disk
            self.log.warning("Installing %s just-db=%s" % (filename, justdb))
            if not justdb:
                pm.extract(overwrite=overwrite)
            else:
                self.log.warning("--just-db mode, will not install files from %s"
                                 % filename)
            # Update the local DB
            db.addPackage(dbp, pm.getRelocatedFileMetadata())

            # Now checking
            if not justdb:
                pm.checkFileSizesOnDisk()

        except Exception, e:
            print e
            traceback.print_exc()
            # Rollback here
            self.log.error("Error installing files, rolling back")
            pm.removeFiles()
            raise e

        if not justdb:
            try:
                # Running the post install
                self._runPostInstall(pm, dbp)
            except Exception, e:
                print e
                traceback.print_exc()
                self.log.error("Error running post install for %s" % filename)
        else:
            self.log.warning("--just-db mode, will not attempt to run "
                             "post-install for %s"
                             % filename)

        # Now cleanup if install was successfull
        if removeAfterInstall:
            self.log.debug("Install of %s succesful, removing RPM"
                           % filename)
            # Checking the location, do not remove files that are in a
            # local cache...
            willremove = True
            for cachedir in self._localRPMcache:
                if abspath(filename).startswith(abspath(cachedir)):
                    self.log.debug("File %s in local cache, will not remove"
                                   % filename)
                    willremove = False
            if willremove:
                self.log.warning("Removing %s" % filename)
                os.unlink(filename)

    def _runPostInstall(self, packageManager, dbPackage):
        ''' Runs the post install script for a given
        package '''

        # First checking whether we have a script to run
        piscriptcontent = packageManager.getPostInstallScript()
        if not piscriptcontent:
            return

        # Opensing the tempfile and running it
        db = self._localDB
        db.setPostInstallRun(dbPackage, "N")

        # Setting the RPM_INSTALL_PREFIX expected by the scripts
        newenv = dict(os.environ)
        prefix = packageManager.getInstallPrefix()
        if prefix is not None:
            self.log.warning("Setting RPM_INSTALL_PREFIX to %s" % prefix)
            newenv["RPM_INSTALL_PREFIX"] = prefix

        import tempfile
        import subprocess
        self.log.info("Running post-install scripts for %s"
                      % packageManager.getFullName())
        with tempfile.NamedTemporaryFile(prefix="lbpostinst",
                                         delete=False) as piscript:
            piscript.write(piscriptcontent)
            piscript.flush()
            rc = subprocess.check_call(["/bin/sh", piscript.name],
                                       stdout=sys.stdout,
                                       stderr=sys.stderr,
                                       env=newenv)
            if rc == 0:
                db.setPostInstallRun(dbPackage, "Y")
            else:
                db.setPostInstallRun(dbPackage, "E")

    def addDirToRPMCache(self, cachedir):
        ''' Add a directory to the list of dirs that will be scanned
        to look for RPM files before scanning them'''
        self._localRPMcache.append(cachedir)

    def _findFileLocally(self, package):
        ''' Look for RPM  in the local cache directory '''
        for cachedir in self._localRPMcache:
            # Try to look for file on local disk
            self.log.debug("Looking for %s in %s"
                           % (package.rpmFileName(), cachedir))
            localfile = findFileInDir(package.rpmFileName(), cachedir)
            if localfile is not None:
                return localfile
        return None

    def _downloadfiles(self, installlist, location=None):
        """ Downloads a list of files """

        # Default to the TMP directory...
        if location is None:
            location = self._tmpdir

        import urllib
        files = []
        for pack in installlist:
            filename = pack.rpmFileName()
            full_filename = os.path.join(location, filename)
            files.append(full_filename)

            # Checking if file is there and is ok
            needs_download = True
            if os.path.exists(full_filename):
                fileisok = self._checkRpmFile(full_filename)
                if fileisok:
                    needs_download = False

            # Now doing the download
            if not needs_download:
                self.log.debug("%s already exists, will not download"
                               % filename)
            else:
                self.log.info("Downloading %s to %s" % (pack.url(),
                                                        full_filename))
                urllib.urlretrieve(pack.url(), full_filename)
        return files

    def _checkRpmFile(self, full_filename):
        """ Check a specific RPM file """
        self.log.debug("__checkRpmFile NOT YET IMPLEMENTED")
        return True

    # Package removal
    # ############################################################################3
    def remove(self, namere, versionre=None, relre=None, force=False):
        '''
        Remove packages from the system
        '''
        if not namere:
            raise Exception("Please specify the name of packages to remove")

        self.log.warning("Request to remove %s %s %s force=%s"
                         % (namere, versionre, relre, force))
        allpacks = list(self._localDB.getPackages(namere, versionre, relre))

        if len(allpacks) == 0:
            self.log.error("Found no packages to remove - exiting")
        else:
            for p in allpacks:
                self._removeOne(p, force)

    def _removeOne(self, package, force=False):
        '''
        Remove one package from DB and disk
        '''
        self.log.warning("Removing %s" % package.rpmName())
        # Checking whether the package is needed by others...
        reqlist = self._localDB.findPackagesRequiringPackage(package)
        # reqlist is a list of pairs:
        # (requiement. list of package requiring that specific req)
        # Need to convert to a set of packages needed...
        packset = set()
        for _, packlist in reqlist:
            for p in packlist:
                packset.add(p)

        proceedWithRemove = False
        if len(packset) > 0 and not force:
            self.log.error("Cannot remove package %s, needed by %s"
                           % (package.rpmName(),
                              ",".join([r.rpmName() for r in packset])))
        elif len(packset) > 0 and force:
            self.log.warning("Forcing remove of %s needed by %s"
                             % (package.rpmName(),
                                ",".join([r.rpmName() for r in packset])))
            proceedWithRemove = True
        else:
            self.log.info("No dependency found for %s" % package.rpmName())
            proceedWithRemove = True

        if proceedWithRemove:
            filemetadata = self._localDB.loadFMData(package.rpmName())
            # Doing the files first
            for l in filemetadata:
                if not os.path.isdir(l[0]):
                    self.log.debug("Removing file %s" % l[0])
                    try:
                        os.unlink(l[0])
                    except:
                        pass # ignore error
            # Doing the files first
            for l in filemetadata[::-1]:
                if os.path.isdir(l[0]):
                    if len(list(os.listdir(l[0]))):
                        self.log.warning("Cannot remove %s, not empty" %l[0])
                    else:
                        self.log.debug("Removing dir %s" % l[0])
                        os.rmdir(l[0])
            # Now removing the package metadata
            self._localDB.removePackage(package.toDmPackage())
