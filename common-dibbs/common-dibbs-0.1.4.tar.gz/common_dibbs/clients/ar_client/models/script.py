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


class Script(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self, id=None, code=None, appliance=None, action=None):
        """
        Script - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'id': 'int',
            'code': 'str',
            'appliance': 'str',
            'action': 'str'
        }

        self.attribute_map = {
            'id': 'id',
            'code': 'code',
            'appliance': 'appliance',
            'action': 'action'
        }

        self._id = id
        self._code = code
        self._appliance = appliance
        self._action = action

    @property
    def id(self):
        """
        Gets the id of this Script.
        Unique identifier representing a specific script

        :return: The id of this Script.
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this Script.
        Unique identifier representing a specific script

        :param id: The id of this Script.
        :type: int
        """

        self._id = id

    @property
    def code(self):
        """
        Gets the code of this Script.
        Actual code of the script

        :return: The code of this Script.
        :rtype: str
        """
        return self._code

    @code.setter
    def code(self, code):
        """
        Sets the code of this Script.
        Actual code of the script

        :param code: The code of this Script.
        :type: str
        """

        self._code = code

    @property
    def appliance(self):
        """
        Gets the appliance of this Script.
        Name of the associated appliance

        :return: The appliance of this Script.
        :rtype: str
        """
        return self._appliance

    @appliance.setter
    def appliance(self, appliance):
        """
        Sets the appliance of this Script.
        Name of the associated appliance

        :param appliance: The appliance of this Script.
        :type: str
        """

        self._appliance = appliance

    @property
    def action(self):
        """
        Gets the action of this Script.
        Name of the associated action

        :return: The action of this Script.
        :rtype: str
        """
        return self._action

    @action.setter
    def action(self, action):
        """
        Sets the action of this Script.
        Name of the associated action

        :param action: The action of this Script.
        :type: str
        """

        self._action = action

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
