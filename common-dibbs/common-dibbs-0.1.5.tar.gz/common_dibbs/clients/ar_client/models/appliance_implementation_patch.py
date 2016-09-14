# coding: utf-8

"""
    Appliance Registry API

    Store appliances with the Appliance Registry API.

    OpenAPI spec version: 0.1.13
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""

from pprint import pformat
from six import iteritems
import re


class ApplianceImplementationPatch(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self, name=None, logo_url=None, image_name=None, site=None, appliance=None):
        """
        ApplianceImplementationPatch - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'name': 'str',
            'logo_url': 'str',
            'image_name': 'str',
            'site': 'str',
            'appliance': 'str'
        }

        self.attribute_map = {
            'name': 'name',
            'logo_url': 'logo_url',
            'image_name': 'image_name',
            'site': 'site',
            'appliance': 'appliance'
        }

        self._name = name
        self._logo_url = logo_url
        self._image_name = image_name
        self._site = site
        self._appliance = appliance

    @property
    def name(self):
        """
        Gets the name of this ApplianceImplementationPatch.
        Name of the appliance implementation

        :return: The name of this ApplianceImplementationPatch.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this ApplianceImplementationPatch.
        Name of the appliance implementation

        :param name: The name of this ApplianceImplementationPatch.
        :type: str
        """

        self._name = name

    @property
    def logo_url(self):
        """
        Gets the logo_url of this ApplianceImplementationPatch.
        URL to a logo image

        :return: The logo_url of this ApplianceImplementationPatch.
        :rtype: str
        """
        return self._logo_url

    @logo_url.setter
    def logo_url(self, logo_url):
        """
        Sets the logo_url of this ApplianceImplementationPatch.
        URL to a logo image

        :param logo_url: The logo_url of this ApplianceImplementationPatch.
        :type: str
        """

        self._logo_url = logo_url

    @property
    def image_name(self):
        """
        Gets the image_name of this ApplianceImplementationPatch.
        Name of the image that will be used by the appliance implementation

        :return: The image_name of this ApplianceImplementationPatch.
        :rtype: str
        """
        return self._image_name

    @image_name.setter
    def image_name(self, image_name):
        """
        Sets the image_name of this ApplianceImplementationPatch.
        Name of the image that will be used by the appliance implementation

        :param image_name: The image_name of this ApplianceImplementationPatch.
        :type: str
        """

        self._image_name = image_name

    @property
    def site(self):
        """
        Gets the site of this ApplianceImplementationPatch.
        Name of the site to use

        :return: The site of this ApplianceImplementationPatch.
        :rtype: str
        """
        return self._site

    @site.setter
    def site(self, site):
        """
        Sets the site of this ApplianceImplementationPatch.
        Name of the site to use

        :param site: The site of this ApplianceImplementationPatch.
        :type: str
        """

        self._site = site

    @property
    def appliance(self):
        """
        Gets the appliance of this ApplianceImplementationPatch.
        Name of the appliance

        :return: The appliance of this ApplianceImplementationPatch.
        :rtype: str
        """
        return self._appliance

    @appliance.setter
    def appliance(self, appliance):
        """
        Sets the appliance of this ApplianceImplementationPatch.
        Name of the appliance

        :param appliance: The appliance of this ApplianceImplementationPatch.
        :type: str
        """

        self._appliance = appliance

    def to_dict(self):
        """
        Returns the model properties as a dict
        """
        result = {}

        for attr, _ in iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """
        Returns the string representation of the model
        """
        return pformat(self.to_dict())

    def __repr__(self):
        """
        For `print` and `pprint`
        """
        return self.to_str()

    def __eq__(self, other):
        """
        Returns true if both objects are equal
        """
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
