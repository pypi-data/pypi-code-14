# Licensed to the Brocade, Inc. ('Brocade') under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import abc
import httplib
import traceback

import six
from cliff import command


@six.add_metaclass(abc.ABCMeta)
class ResourceCommand(command.Command):
    pk_argument_name = None

    def __init__(self, resource, app, *args, **kwargs):
        super(ResourceCommand, self).__init__(app, *args, **kwargs)
        self.resource = resource
        self.app = app

    @property
    def manager(self):
        return self.app.client.managers[self.resource.__name__]

    @property
    def arg_name_for_resource_id(self):
        resource_name = self.resource.get_display_name().lower()
        return '%s-id' % resource_name.replace(' ', '-')

    def print_not_found(self, name):
        print ('%s "%s" is not found.\n' %
               (self.resource.get_display_name(), name))

    def get_resource(self, name_or_id, **kwargs):
        pk_argument_name = self.pk_argument_name

        if pk_argument_name == 'name_or_id':
            instance = self.get_resource_by_name_or_id(name_or_id=name_or_id, **kwargs)
        elif pk_argument_name == 'ref_or_id':
            instance = self.get_resource_by_ref_or_id(ref_or_id=name_or_id, **kwargs)
        else:
            instance = self.get_resource_by_pk(pk=name_or_id, **kwargs)

        return instance

    def get_resource_by_pk(self, pk, **kwargs):
        """
        Retrieve resource by a primary key.
        """
        try:
            instance = self.manager.get_by_id(pk, **kwargs)
        except Exception as e:
            traceback.print_exc()
            # Hack for "Unauthorized" exceptions, we do want to propagate those
            response = getattr(e, 'response', None)
            status_code = getattr(response, 'status_code', None)
            if status_code and status_code == httplib.UNAUTHORIZED:
                raise e

            instance = None

        return instance

    def get_resource_by_id(self, id, **kwargs):
        instance = self.get_resource_by_pk(pk=id, **kwargs)

        if not instance:
            message = ('Resource with id "%s" doesn\'t exist.' % (id))
            raise ResourceNotFoundError(message)
        return instance

    def get_resource_by_name(self, name, **kwargs):
        """
        Retrieve resource by name.
        """
        instance = self.manager.get_by_name(name, **kwargs)
        return instance

    def get_resource_by_name_or_id(self, name_or_id, **kwargs):
        instance = self.get_resource_by_name(name=name_or_id, **kwargs)
        if not instance:
            instance = self.get_resource_by_pk(pk=name_or_id, **kwargs)

        if not instance:
            message = ('Resource with id or name "%s" doesn\'t exist.' %
                       (name_or_id))
            raise ResourceNotFoundError(message)
        return instance

    def get_resource_by_ref_or_id(self, ref_or_id, **kwargs):
        instance = self.manager.get_by_ref_or_id(ref_or_id=ref_or_id, **kwargs)
        if not instance:
            message = ('Resource with id or reference "%s" doesn\'t exist.' %
                       (ref_or_id))
            raise ResourceNotFoundError(message)
        return instance

    def _get_metavar_for_argument(self, argument):
        return argument.replace('_', '-')

    def _get_help_for_argument(self, resource, argument):
        argument_display_name = argument.title()
        resource_display_name = resource.get_display_name().lower()

        if 'ref' in argument:
            result = ('Reference or ID of the %s.' % (resource_display_name))
        elif 'name_or_id' in argument:
            result = ('Name or ID of the %s.' % (resource_display_name))
        else:
            result = ('%s of the %s.' % (argument_display_name, resource_display_name))

        return result


class ResourceNotFoundError(Exception):
    pass
