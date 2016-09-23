from googleapiclient import discovery
from oauth2client.service_account import ServiceAccountCredentials

from .Compute import Compute
from .DeploymentManager import DeploymentManager
from .Iam import Iam

CLOUD_PLATFORM_SCOPE = 'https://www.googleapis.com/auth/cloud-platform'


class Cloud:
    def __init__(self, credentials_file: str, scopes=CLOUD_PLATFORM_SCOPE):
        credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials_file, scopes)
        self._compute = Compute(discovery.build(serviceName='compute', version='v1', credentials=credentials))
        self._iam = Iam(discovery.build(serviceName='iam', version='v1', credentials=credentials))
        self._deploymentmanager = DeploymentManager(discovery.build(serviceName='deploymentmanager',
                                                                    version='v2',
                                                                    credentials=credentials))

    def compute(self) -> Compute:
        return self._compute

    def iam(self) -> Iam:
        return self._iam

    def deployment_manager(self) -> DeploymentManager:
        return self._deploymentmanager
