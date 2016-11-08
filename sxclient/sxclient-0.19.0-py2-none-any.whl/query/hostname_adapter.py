'''
Copyright (C) 2015-2016 Skylable Ltd. <info-copyright@skylable.com>
License: Apache 2.0, see LICENSE for more details.
'''

from __future__ import unicode_literals

import requests
from requests.packages.urllib3.poolmanager import PoolManager


class SXHostnameAdapter(requests.adapters.HTTPAdapter):
    def __init__(self, assert_hostname=None, **kwargs):  # type: ignore
        self.assert_hostname = assert_hostname
        super(SXHostnameAdapter, self).__init__(**kwargs)

    def init_poolmanager(self, connections, maxsize, block=False):  # type: ignore  # noqa
        self.poolmanager = PoolManager(
            num_pools=connections,
            maxsize=maxsize,
            block=block,
            assert_hostname=self.assert_hostname
        )
