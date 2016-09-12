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


class Appliance(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self, name=None, logo_url=None, description=None, implementations=None):
        """
        Appliance - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'name': 'str',
            'logo_url': 'str',
            'description': 'str',
            'implementations': 'list[str]'
        }

        self.attribute_map = {
            'name': 'name',
            'logo_url': 'logo_url',
            'description': 'description',
            'implementations': 'implementations'
        }

        self._name = name
        self._logo_url = logo_url
        self._description = description
        self._implementations = implementations

    @property
    def name(self):
        """
        Gets the name of this Appliance.
        Name of the appliance

        :return: The name of this Appliance.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this Appliance.
        Name of the appliance

        :param name: The name of this Appliance.
        :type: str
        """

        self._name = name

    @property
    def logo_url(self):
        """
        Gets the logo_url of this Appliance.
        URL to a logo image

        :return: The logo_url of this Appliance.
        :rtype: str
        """
        return self._logo_url

    @logo_url.setter
    def logo_url(self, logo_url):
        """
        Sets the logo_url of this Appliance.
        URL to a logo image

        :param logo_url: The logo_url of this Appliance.
        :type: str
        """

        self._logo_url = logo_url

    @property
    def description(self):
        """
        Gets the description of this Appliance.
        Description of the appliance

        :return: The description of this Appliance.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this Appliance.
        Description of the appliance

        :param description: The description of this Appliance.
        :type: str
        """

        self._description = description

    @property
    def implementations(self):
        """
        Gets the implementations of this Appliance.


        :return: The implementations of this Appliance.
        :rtype: list[str]
        """
        return self._implementations

    @implementations.setter
    def implementations(self, implementations):
        """
        Sets the implementations of this Appliance.


        :param implementations: The implementations of this Appliance.
        :type: list[str]
        """

        self._implementations = implementations

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
