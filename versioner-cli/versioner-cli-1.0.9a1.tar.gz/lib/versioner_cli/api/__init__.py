from __future__ import (absolute_import, division, print_function)

from enum import Enum
from urllib.parse import urljoin
from future.utils import raise_with_traceback
import sys

import requests
import logging

from .enums import BumpType

logger = logging.getLogger(__name__)
ch = logging.StreamHandler()
logger.setLevel(logging.DEBUG)
logger.addHandler(ch)


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
        response = requests.post(self.makeurl(VersionerApiRoutes.release),
                             json={'project_name': project_name,
                                     'version': version,
                                     'type': type,
                                     'text': text},
                             headers=self.token,
                             verify=False)
        print('Jenkins Release Response Status: {}'.format(response.status_code))
        logger.debug('Jenkins Release Response Status: {}'.format(response.status_code))
        if response.status_code == 200:
            return response.text
        else:
            return None

    def bump_version(self, bump_type, project_name, branch_from=None, merge_to=None, build_number=None):
        logger.info('bump version')
        if bump_type == BumpType.branch:
            logger.info('bumping branch')
            return requests.post(self.makeurl(VersionerApiRoutes.version),
                                 data={'project_name': project_name,
                                         'bump_type': bump_type,
                                         'branch_from': branch_from,
                                         'build_number': int(build_number)},
                                 headers=self.token, verify=False).json()
        logger.info('bummping not branch')
        result = requests.post(self.makeurl(VersionerApiRoutes.version), data={'project_name': project_name,
                                                                               'bump_type': bump_type},
                             verify=False)
        logger.info(result.text)
        return result.json().get('id'), result.json().get('version').get('formatted')

    def get_auth_token(self):
        print(self.username, self.password)
        response = requests.post(self.makeurl(VersionerApiRoutes.login), json={'username': self.username,
                                                                             'password': self.password},
                             verify=False)
        if response.status_code == 200:
            return response.json().get('token')
        else:
            raise_with_traceback(ValueError('Bad Username Password for Versioner'))

    def __init__(self, endpoint, username=None, password=None):
        self.endpoint = endpoint
        if username and password:
            self.username = username
            self.password = password
            try:
                self.token = {'X-Auth-Token': self.get_auth_token()}
            except ValueError as msg:
                logger.critical(msg)
                sys.exit(0)
