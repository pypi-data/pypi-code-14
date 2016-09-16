# -*- encoding: utf-8 -*-
# Copyright (c) 2015 b<>com
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import enum

from watcher.common import exception


class ResourceType(enum.Enum):
    cpu_cores = 'num_cores'
    memory = 'memory'
    disk = 'disk'
    disk_capacity = 'disk_capacity'


class Resource(object):
    def __init__(self, name, capacity=None):
        """Resource

        :param name: ResourceType
        :param capacity: max
        :return:
        """
        self._name = name
        self.capacity = capacity
        self.mapping = {}

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, n):
        self._name = n

    def set_capacity(self, element, value):
        self.mapping[element.uuid] = value

    def unset_capacity(self, element):
        del self.mapping[element.uuid]

    def get_capacity_by_uuid(self, uuid):
        try:
            return self.mapping[str(uuid)]
        except KeyError:
            raise exception.CapacityNotDefined(
                capacity=self.name.value, resource=str(uuid))

    def get_capacity(self, element):
        return self.get_capacity_by_uuid(element.uuid)
