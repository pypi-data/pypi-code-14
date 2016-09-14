from enum import Enum
from urllib.parse import urljoin

import requests

from versioner_cli.api.enums import BumpType


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
        return requests.post(self.makeurl(VersionerApiRoutes.version),
                             params={'project_name': project_name,
                                     'version': version,
                                     'type': type,
                                     'text': text},
                             headers=self.token).json()

    def bump_version(self, bump_type, project_name, branch_name=None, build_number=None):
        if bump_type == BumpType.branch:
            return requests.post(self.makeurl(VersionerApiRoutes.version),
                                 params={'project_name': project_name,
                                         'bump_type': bump_type,
                                         'branch_name': branch_name,
                                         'build_number': int(build_number)},
                                 headers=self.token).json()
        return requests.post(self.makeurl(VersionerApiRoutes.version), params={'project_name': project_name,
                                                                               'bump_type': bump_type}).json()

    def get_auth_token(self):
        return requests.post(self.makeurl(VersionerApiRoutes.login), params={'username': self.username,
                                                                             'password': self.password}).json()

    def __init__(self, endpoint, username=None, password=None):
        self.endpoint = endpoint
        if username and password:
            self.username = username
            self.password = password
            self.token = {'X-Auth-Token': self.get_auth_token()}
