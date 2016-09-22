from __future__ import (absolute_import, division, print_function)

from enum import Enum
from urllib.parse import urljoin

import requests
import logging

from .enums import BumpType

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class VersionerApiRoutes(Enum):
    login = '/api/token/'
    version = '/api/bump/'
    release = '/api/make-release/'


class VersionerVersion(Enum):
    major = 'major'
    minor = 'minor'
    patch = 'patch'
    build = 'build'
    feature = 'feature'


class VersionerApi(object):
    def makeurl(self, api):
        return urljoin(self.endpoint, api.value)

    def make_release(self, project_name, version, type, text):
        logger.info('make release')
        return requests.post(self.makeurl(VersionerApiRoutes.version),
                             data={'project_name': project_name,
                                     'version': version,
                                     'type': type,
                                     'text': text},
                             headers=self.token,
                             verify=False).json()

    def bump_version(self, bump_type, project_name, branch_name=None, build_number=None):
        logger.info('bump version')
        if bump_type == BumpType.branch:
            logger.info('bumping branch')
            return requests.post(self.makeurl(VersionerApiRoutes.version),
                                 data={'project_name': project_name,
                                         'bump_type': bump_type,
                                         'branch_name': branch_name,
                                         'build_number': int(build_number)},
                                 headers=self.token, verify=False).json()
        logger.info('bummping not branch')
        result = requests.post(self.makeurl(VersionerApiRoutes.version), data={'project_name': project_name,
                                                                               'bump_type': bump_type},
                             verify=False)
        logger.info(result.text)
        return result.json().get('formatted')

    def get_auth_token(self):
        return requests.post(self.makeurl(VersionerApiRoutes.login), data={'username': self.username,
                                                                             'password': self.password},
                             verify=False).json()

    def __init__(self, endpoint, username=None, password=None):
        self.endpoint = endpoint
        if username and password:
            self.username = username
            self.password = password
            self.token = {'X-Auth-Token': self.get_auth_token()}
