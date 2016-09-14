# coding: utf-8

"""
    Operation Manager API

    Execute operations with the Operation Manager API.

    OpenAPI spec version: 0.1.4
    
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


class User(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self, id=None, username=None, operation_definitions=None, definition=None):
        """
        User - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'id': 'int',
            'username': 'str',
            'operation_definitions': 'list[int]',
            'definition': 'str'
        }

        self.attribute_map = {
            'id': 'id',
            'username': 'username',
            'operation_definitions': 'operation_definitions',
            'definition': 'definition'
        }

        self._id = id
        self._username = username
        self._operation_definitions = operation_definitions
        self._definition = definition

    @property
    def id(self):
        """
        Gets the id of this User.
        Unique identifier representing a specific user

        :return: The id of this User.
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this User.
        Unique identifier representing a specific user

        :param id: The id of this User.
        :type: int
        """

        self._id = id

    @property
    def username(self):
        """
        Gets the username of this User.
        Name given to the user.

        :return: The username of this User.
        :rtype: str
        """
        return self._username

    @username.setter
    def username(self, username):
        """
        Sets the username of this User.
        Name given to the user.

        :param username: The username of this User.
        :type: str
        """

        self._username = username

    @property
    def operation_definitions(self):
        """
        Gets the operation_definitions of this User.
        Array of IDs of all the process descriptions created by the user

        :return: The operation_definitions of this User.
        :rtype: list[int]
        """
        return self._operation_definitions

    @operation_definitions.setter
    def operation_definitions(self, operation_definitions):
        """
        Sets the operation_definitions of this User.
        Array of IDs of all the process descriptions created by the user

        :param operation_definitions: The operation_definitions of this User.
        :type: list[int]
        """

        self._operation_definitions = operation_definitions

    @property
    def definition(self):
        """
        Gets the definition of this User.
        JSON-formatted string containing all the information required to start the process

        :return: The definition of this User.
        :rtype: str
        """
        return self._definition

    @definition.setter
    def definition(self, definition):
        """
        Sets the definition of this User.
        JSON-formatted string containing all the information required to start the process

        :param definition: The definition of this User.
        :type: str
        """

        self._definition = definition

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
