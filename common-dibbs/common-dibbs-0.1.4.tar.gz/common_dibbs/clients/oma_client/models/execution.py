# coding: utf-8

"""
    Operation Manager Agent API

    Interact with deployed Cloud Computing resources via API.

    OpenAPI spec version: 0.1.1
    
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


class Execution(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self, op_id=None, execution_id=None, progress=None, info=None):
        """
        Execution - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'op_id': 'int',
            'execution_id': 'str',
            'progress': 'float',
            'info': 'str'
        }

        self.attribute_map = {
            'op_id': 'op_id',
            'execution_id': 'execution_id',
            'progress': 'progress',
            'info': 'info'
        }

        self._op_id = op_id
        self._execution_id = execution_id
        self._progress = progress
        self._info = info

    @property
    def op_id(self):
        """
        Gets the op_id of this Execution.
        Unique identifier representing a specific op

        :return: The op_id of this Execution.
        :rtype: int
        """
        return self._op_id

    @op_id.setter
    def op_id(self, op_id):
        """
        Sets the op_id of this Execution.
        Unique identifier representing a specific op

        :param op_id: The op_id of this Execution.
        :type: int
        """

        self._op_id = op_id

    @property
    def execution_id(self):
        """
        Gets the execution_id of this Execution.
        Id of the execution (application specific)

        :return: The execution_id of this Execution.
        :rtype: str
        """
        return self._execution_id

    @execution_id.setter
    def execution_id(self, execution_id):
        """
        Sets the execution_id of this Execution.
        Id of the execution (application specific)

        :param execution_id: The execution_id of this Execution.
        :type: str
        """

        self._execution_id = execution_id

    @property
    def progress(self):
        """
        Gets the progress of this Execution.
        percentage representing the progress of the execution

        :return: The progress of this Execution.
        :rtype: float
        """
        return self._progress

    @progress.setter
    def progress(self, progress):
        """
        Sets the progress of this Execution.
        percentage representing the progress of the execution

        :param progress: The progress of this Execution.
        :type: float
        """

        self._progress = progress

    @property
    def info(self):
        """
        Gets the info of this Execution.
        Formatted JSON information about the progress of the op

        :return: The info of this Execution.
        :rtype: str
        """
        return self._info

    @info.setter
    def info(self, info):
        """
        Sets the info of this Execution.
        Formatted JSON information about the progress of the op

        :param info: The info of this Execution.
        :type: str
        """

        self._info = info

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
