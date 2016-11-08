#    Copyright (c) 2016 Shanghai EISOO Information Technology Corp.
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
from abclient.http import HTTPClient
from abclient.backup_manager import BackupManager


class ABClient(object):
    """AnyBackup Client

    If set both app_id and app_secret, abclient will request
    AnyBackup with a athentication token.
    If either of app_id and app_secret is None, abclient will
    request AnyBackup without ahentication token.

    Usage:

        from abclient.client import ABClient

        client = ABClient('https://<ip addr>:<port>',
                          <app_id>, <app_secret>)
        data_source = client.backup_manager.get_data_source_list(...)
    """
    def __init__(self, endpoint, app_id=None, app_secret=None, **kwargs):
        """
        :param endpoint: EISOO AnyBackup console server endpoint.
        :param app_id: Application ID for EISOO AnyBackup open API
                       authentication.
        :param app_secret: Application secret key for EISOO AnyBackup
                           open API authentication.
        """
        self._http_client = HTTPClient(endpoint, app_id=app_id,
                                       app_secret=app_secret)
        self._app_id = app_id
        self._app_secret = app_secret

        self.backup_manager = BackupManager(self._http_client)
