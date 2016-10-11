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

Module that allows to retrieve information about and extract a .rpm file
e.g:

 pm = PackageManager(/path/to/myfile.rpm, relocateMap)

relocateMap being a map between the prefix as mentioned in the
RPM and the final location:

{ "/opt/LHCbSoft":"/opt/siteroot/lhcb" }

 Then it is possible to extract information like:

 pm.getGroup()
 pm.getProvides()
 pm.getRequires()
 [...]

@author: Ben Couturier
'''
import logging
import os
import stat
import lbinstall.rpmfile as rpmfile

from lbinstall.Model import Provides, Requires, Package

#
# Missing features:
# - handle hard links
# - handle modification times


#
# Various utilities to decode RPM
#############################################################
def flagToString(flags):
    ''' Convert numerical flags to strings '''
    if flags is None or (type(flags) == str and len(flags) == 0):
        return None

    flags = flags & 0xf
    if flags == 0:
        return None
    elif flags == 2:
        return 'LT'
    elif flags == 4:
        return 'GT'
    elif flags == 8:
        return 'EQ'
    elif flags == 10:
        return 'LE'
    elif flags == 12:
        return 'GE'
    return flags


def relocate(filename, prefixmap):
    ''' Relocate the filename according to the map'''
    if filename.startswith("./"):
        filename = filename.replace("./", "/")
    for k in prefixmap.keys():
        if filename.startswith(k):
            return filename.replace(k, prefixmap[k])
    return filename


#
# The package manager itself
#############################################################
class PackageManager(object):
    '''
    Class allowing to open a RPM file and extract information
    and files from it.
    '''

    def __init__(self, filename, relocatemap=None):
        '''
        Initialization for the package manager
        '''
        self.log = logging.getLogger(__name__)
        self._filename = filename
        with rpmfile.open(self._filename) as f:
            self._headers = f.headers

        if relocatemap is None:
            # Just remove the "./" prefix in this case
            relocatemap = {"./": "/"}
        self._relocatemap = relocatemap
        self._topdir = None
        self._filenames = None

    def setrelocatemap(self, m):
        self._relocatemap = m

    def getGroup(self):
        return self._headers["group"]

    def _getProvides(self):
        # The flags don't seem to come a a list when only one is specified
        # making sure it's the case before calling zip
        flags = self._headers["provideflags"]

        if not isinstance(flags, (list, tuple)):
            flags = [flags]

        l = [self._headers["providename"],
             self._headers["provideversion"],
             map(flagToString, flags)]
        return zip(*l)

    def getProvides(self):
        l = self._getProvides()
        provs = []
        for n, v, f in l:
            provs.append(Provides(n, v, None, None, f, None))
        return provs

    def _getRequires(self):
        l = [self._headers["requirename"],
             self._headers["requireversion"],
             map(flagToString, self._headers["requireflags"])]
        return zip(*l)

    def getRequires(self):
        l = self._getRequires()
        reqs = []
        for n, v, f in l:
            reqs.append(Requires(n, v, None, None, f, None))
        return reqs

    def getPackage(self):
        ''' Returns the Package metadata in
        lbinstall.DependencyManager format '''
        p = Package(self.getName(),
                    self.getVersion(),
                    self.getRelease(),
                    None, None, self.getGroup(),
                    self.getArch(),
                    self.getTopDir(),
                    self.getProvides(),
                    self.getRequires(),
                    self.relocate(self.getTopDir()))
        return p

    def getPrefixes(self):
        return self._headers["prefixes"]

    def getInstallPrefix(self):
        """ Return the proper relocation
        prefix in case several are specified """
        topDir = self.getTopDir()
        prefixes = [p for p in self.getPrefixes() if p in topDir]
        if len(prefixes) == 0:
            return None
        else:
            return relocate(prefixes[0], self._relocatemap)

    def getName(self):
        return self._headers["name"]

    def getVersion(self):
        return self._headers["version"]

    def getRelease(self):
        return self._headers["release"]

    def getFullName(self):
        return "%s-%s-%s" % (self.getName(), self.getVersion(),
                             self.getRelease())

    def getMD5Checksum(self):
        return self._headers["md5"]

    def getSize(self):
        return self._headers["size"]

    def getArch(self):
        return self._headers["arch"]

    def getRPMVersion(self):
        return self._headers["rpmversion"]

    def getTopDir(self):
        if self._topdir is None:
            with rpmfile.open(self._filename) as rpm:
                self._topdir = os.path.commonprefix([m.name
                                                     for m
                                                     in rpm.getmembers()])
        return self._topdir

    def extract(self, prefixmap=None, overwrite=False):
        ''' Extract the files using the relocation specified
        in the prefix maps'''
        if prefixmap is None:
            prefixmap = self._relocatemap

        with rpmfile.open(self._filename) as rpm:
            for m in rpm.getmembers():
                if prefixmap is None:
                    # Just fix the "./" in that case
                    target = m.name.replace("./", "/")
                else:
                    target = relocate(m.name, prefixmap)
                # Create directories as needed
                attrs = m._attrs
                if not os.path.exists(target) or overwrite:
                    # Only overwite if requested
                    if attrs["isDir"]:
                        self.log.debug("Creating dir %s" % target)
                        os.makedirs(target)
                        os.chmod(target, attrs["mode"])
                    elif attrs["isLink"]:
                        fin = rpm.extractfile(m.name)
                        lnktgt = fin.read()
                        if not os.path.exists(os.path.dirname(target)):
                            os.makedirs(os.path.dirname(target))
                        self.log.debug("We have a link %s to: %s"
                                       % (target, lnktgt))
                        os.symlink(lnktgt, target)
                        # os.lchmod(target, attrs["mode"])
                    else:
                        if not os.path.exists(os.path.dirname(target)):
                            if not os.path.exists(target):
                                os.makedirs(os.path.dirname(target))
                        self.log.debug("Relocating %s to %s"
                                       % (m.name, target))
                        fin = rpm.extractfile(m.name)
                        with open(target, "w+b") as fout:
                            fout.write(fin.read())
                        os.chmod(target, attrs["mode"])

    def getCpioFileSizes(self):
        ''' Get the file sies from the CPIO archive instead of headers '''
        filesizes = []
        with rpmfile.open(self._filename) as rpm:
            for m in rpm.getmembers():
                filesizes.append(m.size)
        return filesizes

    def relocate(self, path):
        ''' Useful util if the PM is initialized with the
        proper relocation map '''
        return relocate(path, self._relocatemap)

    def checkFileSizesOnDisk(self):
        ''' Compare the filesizes on disk with the RPM metadata '''
        mdata = self.getFileMetadata()
        for (fname, isdir, _md5, s) in mdata:
            if isdir:
                continue
            name = self.relocate(fname)
            # lstat as we do not want to check symlinks
            statres = os.lstat(name)
            if s != statres[stat.ST_SIZE]:
                raise Exception("%s: Mismatch in filesize vs metadata:"
                                " %s vs %s" % (name, statres[stat.ST_SIZE], s))
            self.log.debug("File %s metadata:%s real:%s"
                           % (name, s,  statres[stat.ST_SIZE]))

    def removeFiles(self):
        ''' Cleanup the files already installed '''
        mdata = self.getFileMetadata()
        # First removing the files
        for (fname, isdir, _md5, _s) in mdata:
            if isdir:
                continue
            name = self.relocate(fname)
            try:
                os.unlink(name)
                self.log.warning("Removed %s" % name)
            except:
                self.log.warning("Could not remove %s" % name)
        # First removing the files
        for (fname, isdir, _md5, _s) in mdata[::-1]:
            if not isdir:
                continue
            name = self.relocate(fname)
            try:
                os.rmdir(name)
                self.log.warning("Removed %s" % name)
            except:
                self.log.warning("Could not remove %s" % name)

    def getFileNames(self):
        if self._filenames is None:
            ret = []
            with rpmfile.open(self._filename) as rpm:
                for m in rpm.getmembers():
                    ret.append((m.name, m.isdir))
            self._filenames = ret
        return self._filenames

    def getFileMetadata(self):
        ''' Return a list with the needed info about the files in the RPM,
        i.e. a tuple with (filename, bool(isdir), filemd5, filesize '''
        tmp = zip(*self.getFileNames())
        try:
            tmp.append(self._headers['filemd5s'])
        except:
            tmp.append([])
        tmp.append(self.getCpioFileSizes())
        return zip(*tmp)

    def getRelocatedFileMetadata(self):
        ''' Return a list with the needed infor about the files in the RPM,
        i.e. a tuple with (filename, bool(isdir), filemd5, filesize '''
        tmp = []
        for (name, ftype, md5, size) in self.getFileMetadata():
            tmp.append((self.relocate(name), ftype, md5, size))
        return tmp

    def getPostInstallScript(self):
        ''' returns a string with the content of the post install script '''
        return self._headers.get("postin")
