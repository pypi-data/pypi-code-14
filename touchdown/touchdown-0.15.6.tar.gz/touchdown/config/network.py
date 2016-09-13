# Copyright 2016 Isotoma Limited
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import netaddr

from touchdown.core import argument

from . import variable


class IPNetwork(variable.Variable):

    resource_name = 'ip_network'

    default = argument.String()
    min = argument.Integer()
    max = argument.Integer()


class Set(variable.Set):
    resource = IPNetwork

    def to_lines(self, value):
        return [str(value)]


class Get(variable.Get):
    resource = IPNetwork

    def from_lines(self, value):
        return netaddr.IPNetwork(value[0])


argument.IPNetwork.register_adapter(IPNetwork, variable.VariableAsString)
