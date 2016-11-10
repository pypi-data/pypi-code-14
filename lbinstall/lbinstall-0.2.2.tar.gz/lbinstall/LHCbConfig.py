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
LbInstall specific config for LHCb

"""
import os


class Config:

    def __init__(self):
        self.CONFIG_VERSION = 1

    @staticmethod
    def getRepoConfig(defaultRepoURL=None):
        """ Specify the repository config """

        repourl = "http://lhcbproject.web.cern.ch/lhcbproject/dist/rpm"
        if defaultRepoURL != None:
            repourl = defaultRepoURL

        repos = {}
        repos["lhcb"] = { "url": repourl + "/lhcb" }
        repos["lcg"] = { "url": "http://service-spi.web.cern.ch/service-spi/external/rpms/lcg" }
        repos["lhcbext"] = { "url": repourl + "/lcg" }
        repos["lhcbincubator"] = { "url": repourl + "/incubator" }
        return repos

    @staticmethod
    def getRelocateMap(siteroot):
        """ Returns relocate command to be passed to RPM for the repositories """
        ret = { '/opt/lcg/external' : os.path.join(siteroot, 'lcg', 'external'),
                '/opt/lcg' : os.path.join(siteroot, 'lcg', 'releases'),
                '/opt/LHCbSoft': siteroot }
        return ret
