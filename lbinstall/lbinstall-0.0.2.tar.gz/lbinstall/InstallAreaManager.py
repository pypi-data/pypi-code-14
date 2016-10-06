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
"""

Classes that setup and allow interaction with the files on disk in the
InstallArea.


"""
import logging
import os
import subprocess
import sys
import time

# Constants for the dir names
SVAR = "var"
SLIB = "lib"
SDB = "db"
SETC = "etc"
STMP = "tmp"
SUSR = "usr"
SBIN = "bin"

__RCSID__ = "$Id$"


# Checking whether the MYSITEROOT is set correctly
###############################################################################
class InstallAreaConfig(object):  # IGNORE:R0903
    """ Configuration object for the installer. All options and defaults
    should be kept in an instance of this class """

    def __init__(self, siteroot=None, configType="LHCbConfig"):
        """ Constructor for the config object """
        # Get the default siteroot
        if siteroot is None:
            envsiteroot = os.environ.get("MYSITEROOT", None)
            if envsiteroot is None:
                raise Exception("Please specify the Install root (MYSITEROOT)")
            else:
                siteroot = envsiteroot
        self.siteroot = siteroot
        # And the default repository URL
        self.repourl = None
        # Debug mode defaults to false
        self.debug = False
        # Use install by default
        self.rpmupdate = False
        # Version of the scripts
        self.script_version = "080812"
        # Default log width
        self.line_size = 120
        # Checking python versions
        self.python_version = sys.version_info[:3]
        self.txt_python_version = ".".join([str(k)
                                            for k in self.python_version])
        # Simple logger by default
        self.log = logging.getLogger()
        # Keeping the config type
        self.configType = configType
        # Now importing the config module
        self.configInst = None
        try:
            self.configMod = __import__(self.configType)
            self.configInst = self.configMod.Config()
        except ImportError, ie:
            self.log.error(ie)

# Utility to run a command
###############################################################################
def call(command):
    """ Wraps up subprocess call and return caches and returns rc, stderr, stdout """
    pc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    out, err = pc.communicate()
    rc = pc.returncode
    return (rc, out, err)

# Utility to run a command
###############################################################################
def callSimple(command):
    """ Simpler wrapper for subprocess """
    rc = subprocess.call(command, shell=True)
    return rc

# Check for binary in path
###############################################################################
def checkForCommand(command):
    """ Check whether a command is in the path using which """
    whichcmd = "which %s" % command
    rc, out, err = call(whichcmd)  # @UnusedVariable IGNORE:W0612
    return rc, out

# Utilities for log printout
###############################################################################
def printHeader(config):
    """ Prints the standard header as in install_project """
    # Start banner
    thelog = config.log
    start_time = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
    thelog.info('=' * config.line_size)
    thelog.info(('<<< %s - Start of lb-install.py %s with python %s >>>' \
                 % (start_time, config.script_version, config.txt_python_version)).center(config.line_size))
    thelog.info('=' * config.line_size)
    thelog.debug("Command line arguments: %s" % " ".join(sys.argv))

def printTrailer(config):
    """ Prints the standard trailer as in install_project """
    # Trailer
    thelog = config.log
    end_time = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
    thelog.info('=' * config.line_size)
    thelog.info(('<<< %s - End of lb-install.py %s >>>' % (end_time, config.script_version)).center(config.line_size))
    thelog.info('=' * config.line_size)

# Class representing the repository
###############################################################################
class InstallArea(object):  # IGNORE:R0902
    """ Class representing the software InstallArea,
    with all related actions"""

    # Initialization of the area
    ##########################################################################
    def __init__(self, config=None):
        """ Init of the InstallArea, check that all directories and config files
        are present.
        """
        self.config = config
        self.log = logging.getLogger(__name__)

        # Setting the siteroot
        self.siteroot = config.siteroot
        self.log.info("Siteroot is: %s" % self.siteroot)
        if self.siteroot is None:
            self.log.error("Please specify a site root with the --root option or via the MYSITEROOT env variable")
            sys.exit(1)

        # Setting the main repository URL
        self.repourl = config.repourl

        # Making sure the directory containing the DB is initialized
        self.dbdir = os.path.join(self.siteroot, SVAR, SLIB, SDB)
        if not os.path.exists(self.dbdir):
            os.makedirs(self.dbdir)
        self.dbpath = os.path.join(self.dbdir, "packages.db")

        # Initializing yum config
        self.etc = os.path.join(self.siteroot, SETC)
        if not os.path.exists(self.etc):
            os.makedirs(self.etc)
        
        # tmp directory
        self.tmpdir = os.path.join(self.siteroot, STMP)
        if not os.path.exists(self.tmpdir):
            os.makedirs(self.tmpdir)

        # Local bin directory
        self.usrbin = os.path.join(self.siteroot, SUSR, SBIN)
        if not os.path.exists(self.usrbin):
            os.makedirs(self.usrbin)
        # Add the local bin to the path
        os.environ['PATH'] = os.pathsep.join([os.environ['PATH'], self.usrbin])

        # Local lib directory
        self.lib = os.path.join(self.siteroot, SLIB)
        if not os.path.exists(self.lib):
            os.makedirs(self.lib)
        # Add the local bin to the path
        sys.path.append(self.lib)


        # Now calling the configuration method from the specific config module...
        self.yumConfig = self.config.configInst.getRepoConfig(None)

        # Defining structures and
        # Checking if all needed tools are available
        self.externalStatus = {}
        self.requiredExternals = [  ]
        self.externalFix = {}
        self._checkPrerequisites()

        # And if all the software is there
        self.initfile = None
        self._checkRepository()

    def createYumClient(self, checkForUpdates=True):
        from DependencyManager import LbYumClient
        conf = dict([(k,v["url"]) for k, v in self.yumConfig.iteritems()])
        return LbYumClient(self.siteroot, conf, checkForUpdates=checkForUpdates)

    def createDBManager(self):
        # Setting up our own local software DB
        from db.DBManager import DBManager
        return DBManager(self.dbpath)

    def getTmpDir(self):
        return self.tmpdir

    def _checkPrerequisites(self):
        """ Checks that external tools required by this tool to perform
        the installation """
        # Flag indicating whether a crucial external is missing and we cannot run
        externalMissing = False

        for e in self.requiredExternals:
            rc, out = checkForCommand(e)
            self.externalStatus[e] = (rc, out)

        for key, val in self.externalStatus.iteritems():
            rc, exefile = val
            if rc == 0:
                self.log.info("%s: Found %s", key, exefile.strip())
            else:
                self.log.info("%s: Missing - trying compensatory measure", key)
                fix = self.externalFix[key]
                if fix is not None:
                    fix()
                    rc2, out2 = checkForCommand(key)
                    self.externalStatus[key] = (rc2, out2)
                    if rc2 == 0:
                        self.log.info("%s: Found %s", key, out2)
                    else:
                        self.log.error("%s: missing", key)
                        externalMissing = True
                else:
                    externalMissing = True
        return externalMissing

    def _checkRepository(self):
        """ Checks whether the repository was initialized """
        self.initfile = os.path.join(self.etc, "repoinit")
        if not os.path.exists(self.initfile):
            # self.installRpm("LBSCRIPTS")
            with open(self.initfile, "w") as fini:
                fini.write(time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime()))
        # BC: Remove auto update and add specific command instead
        # else:
        #    self._checkUpdates()

    def getRelocateMap(self):
        """ Returns the mapping between siteroot and extract location """
        # XXX Need to clean up config system
        return self.config.configInst.getRelocateMap(self.siteroot)
