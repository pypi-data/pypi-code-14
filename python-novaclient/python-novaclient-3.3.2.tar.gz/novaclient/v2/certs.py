# Copyright 2010 Jacob Kaplan-Moss

# Copyright 2011 OpenStack Foundation
# All Rights Reserved.
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

"""
Certificate interface.
"""

from novaclient import base


class Certificate(base.Resource):
    def __repr__(self):
        return ("<Certificate: private_key=[%s bytes] data=[%s bytes]>" %
                (len(self.private_key) if self.private_key else 0,
                 len(self.data)))


class CertificateManager(base.Manager):
    """Manage :class:`Certificate` resources."""
    resource_class = Certificate

    def create(self):
        """Create a x509 certificate for a user in tenant."""
        return self._create('/os-certificates', {}, 'certificate')

    def get(self):
        """Get root certificate."""
        return self._get("/os-certificates/root", 'certificate')
