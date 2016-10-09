# Copyright 2016 Arie Bregman
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
import logging
import re
import yum

import common.constants as const
from result import Result

LOG = logging.getLogger('__main__')


class Yum(object):
    """Represents the local defined repositories."""

    def __init__(self, repos='all', disabled=False, fields=['name']):
        self.name = 'yum'
        self.repos = repos
        self.yum = yum.YumBase()
        self.repos = (self.yum).repos.listEnabled()
        self.ready = self.setup()
        self.disabled = disabled
        self.fields = fields

    def setup(self):
        """Returns bool to indicate whether the source is ready

           or not.
        """
        return len(self.repos)

    def verify_name(self, result, req):
        """Verify the result is indeed the package it searched for.

        The problem with yum search is that it simply searches for the
        string in the name, but not the exact match.

        Also, requirement might be called 'hacking' while the RPM is
        'python-hacking'.
        """
        #rpm_ver = re.search(r'((\d+\.)+\d+(\-\d+))', result)
        #print rpm_ver.group(1)
        m = re.search(r'(^[a-zA-z0-9\-]*)\-\d', result)
        return m.group(1) in [prefix+req for prefix in const.PREFIXES]

    def search(self, req):
        """Returns list of Result object based on the RPMs it found that

        match the requirement name.
        """
        LOG.debug("Looking for %s", req.name)
        found_pkgs = []

        result = (self.yum).searchGenerator(self.fields, [req.name])
        for (full_string, pkg_name) in result:
            if self.verify_name(str(full_string), req.name):
                #LOG.debug("Found: %s", full_string)
                found_pkgs.append(Result(full_string))

        return found_pkgs
