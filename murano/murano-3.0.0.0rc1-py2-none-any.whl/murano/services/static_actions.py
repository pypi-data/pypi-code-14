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

import uuid

from murano.common import rpc


class StaticActionServices(object):

    @staticmethod
    def execute(method_name, class_name, pkg_name, class_version, args,
                credentials):
        action = {
            'method': method_name,
            'args': args or {},
            'class_name': class_name,
            'pkg_name': pkg_name,
            'class_version': class_version
        }
        task = {
            'action': action,
            'token': credentials['token'],
            'tenant_id': credentials['tenant_id'],
            'id': str(uuid.uuid4())
        }
        return rpc.engine().call_static_action(task)
