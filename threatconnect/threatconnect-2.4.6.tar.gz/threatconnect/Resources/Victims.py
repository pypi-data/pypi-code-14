""" standard """
import re
import types

""" custom """
from threatconnect import ApiProperties
from threatconnect import VictimFilterMethods
from threatconnect.VictimObject import VictimObjectAdvanced
from threatconnect.Config.ResourceType import ResourceType
from threatconnect.RequestObject import RequestObject
from threatconnect.Resource import Resource
from threatconnect.FilterObject import FilterObject


class Victims(Resource):
    """ """
    def __init__(self, tc_obj):
        """ """
        super(Victims, self).__init__(tc_obj)
        self._filter_class = VictimFilterObject
        self._resource_type = ResourceType.VICTIMS

    @ property
    def default_request_object(self):
        """ default request when no filters are provided """
        resource_properties = ApiProperties.api_properties[self._resource_type.name]['properties']
        # create default request object for non-filtered requests
        request_object = RequestObject()
        request_object.set_http_method(resource_properties['base']['http_method'])
        request_object.set_owner_allowed(resource_properties['base']['owner_allowed'])
        request_object.set_request_uri(resource_properties['base']['uri'])
        request_object.set_resource_pagination(resource_properties['base']['pagination'])
        request_object.set_resource_type(self._resource_type)
        return request_object

    def _method_wrapper(self, resource_object):
        """ """
        return VictimObjectAdvanced(self.tc, self, resource_object)
        # return resource_object


class VictimFilterObject(FilterObject):
    """ """
    def __init__(self, tc_obj):
        """ """
        super(VictimFilterObject, self).__init__(tc_obj)
        self._owners = []

        # define properties for resource type
        self._resource_type = ResourceType.VICTIMS
        self._resource_properties = ApiProperties.api_properties[self._resource_type.name]['properties']

        #
        # add_obj filter methods
        #
        for method_name in self._resource_properties['filters']:
            if re.findall('add_pf_', method_name):
                self.add_post_filter_names(method_name)
            else:
                self.add_api_filter_name(method_name)
            method = getattr(VictimFilterMethods, method_name)
            setattr(self, method_name, types.MethodType(method, self))

    @ property
    def default_request_object(self):
        """ default request when only a owner filter is provided """
        request_object = RequestObject()
        request_object.set_description('filter by owner')
        request_object.set_http_method(self._resource_properties['base']['http_method'])
        request_object.set_owner_allowed(self._resource_properties['base']['owner_allowed'])
        request_object.set_request_uri(self._resource_properties['base']['uri'])
        request_object.set_resource_pagination(self._resource_properties['base']['pagination'])
        request_object.set_resource_type(self._resource_type)

        return request_object
