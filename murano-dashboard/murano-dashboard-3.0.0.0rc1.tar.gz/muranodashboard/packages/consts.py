#    Copyright (c) 2015 Mirantis, Inc.
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

from django.conf import settings
from oslo_log import log as logging

LOG = logging.getLogger(__name__)


MURANO_REPO_URL = getattr(
    settings, 'MURANO_REPO_URL',
    "http://apps.openstack.org/api/v1/murano_repo/liberty/")

DISPLAY_MURANO_REPO_URL = getattr(
    settings, 'DISPLAY_MURANO_REPO_URL',
    "http://apps.openstack.org/#tab=murano-apps")

try:
    MAX_FILE_SIZE_MB = int(getattr(settings, 'MAX_FILE_SIZE_MB', 5))
except ValueError:
    LOG.warning("MAX_FILE_SIZE_MB parameter has the incorrect value.")
    MAX_FILE_SIZE_MB = 5
