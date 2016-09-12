# coding: utf-8

"""
    Operation Registry API

    Register operations with the Operation Registry API.

    OpenAPI spec version: 0.1.9
    
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


class OperationVersionPatch(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self, name=None, appliance=None, process_definition=None, cwd=None, script=None, output_type=None, output_parameters=None):
        """
        OperationVersionPatch - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'name': 'str',
            'appliance': 'str',
            'process_definition': 'int',
            'cwd': 'str',
            'script': 'str',
            'output_type': 'str',
            'output_parameters': 'str'
        }

        self.attribute_map = {
            'name': 'name',
            'appliance': 'appliance',
            'process_definition': 'process_definition',
            'cwd': 'cwd',
            'script': 'script',
            'output_type': 'output_type',
            'output_parameters': 'output_parameters'
        }

        self._name = name
        self._appliance = appliance
        self._process_definition = process_definition
        self._cwd = cwd
        self._script = script
        self._output_type = output_type
        self._output_parameters = output_parameters

    @property
    def name(self):
        """
        Gets the name of this OperationVersionPatch.
        Name given to the process implementation

        :return: The name of this OperationVersionPatch.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this OperationVersionPatch.
        Name given to the process implementation

        :param name: The name of this OperationVersionPatch.
        :type: str
        """

        self._name = name

    @property
    def appliance(self):
        """
        Gets the appliance of this OperationVersionPatch.
        Name of the appliance on which the process implementation must be run

        :return: The appliance of this OperationVersionPatch.
        :rtype: str
        """
        return self._appliance

    @appliance.setter
    def appliance(self, appliance):
        """
        Sets the appliance of this OperationVersionPatch.
        Name of the appliance on which the process implementation must be run

        :param appliance: The appliance of this OperationVersionPatch.
        :type: str
        """

        self._appliance = appliance

    @property
    def process_definition(self):
        """
        Gets the process_definition of this OperationVersionPatch.
        Id of the process definition linked with this new implementation

        :return: The process_definition of this OperationVersionPatch.
        :rtype: int
        """
        return self._process_definition

    @process_definition.setter
    def process_definition(self, process_definition):
        """
        Sets the process_definition of this OperationVersionPatch.
        Id of the process definition linked with this new implementation

        :param process_definition: The process_definition of this OperationVersionPatch.
        :type: int
        """

        self._process_definition = process_definition

    @property
    def cwd(self):
        """
        Gets the cwd of this OperationVersionPatch.
        Working directory to be in when ruing the process implementation

        :return: The cwd of this OperationVersionPatch.
        :rtype: str
        """
        return self._cwd

    @cwd.setter
    def cwd(self, cwd):
        """
        Sets the cwd of this OperationVersionPatch.
        Working directory to be in when ruing the process implementation

        :param cwd: The cwd of this OperationVersionPatch.
        :type: str
        """

        self._cwd = cwd

    @property
    def script(self):
        """
        Gets the script of this OperationVersionPatch.
        Script to execute to run the process on the cluster

        :return: The script of this OperationVersionPatch.
        :rtype: str
        """
        return self._script

    @script.setter
    def script(self, script):
        """
        Sets the script of this OperationVersionPatch.
        Script to execute to run the process on the cluster

        :param script: The script of this OperationVersionPatch.
        :type: str
        """

        self._script = script

    @property
    def output_type(self):
        """
        Gets the output_type of this OperationVersionPatch.
        type of output (e.g. file, stream)

        :return: The output_type of this OperationVersionPatch.
        :rtype: str
        """
        return self._output_type

    @output_type.setter
    def output_type(self, output_type):
        """
        Sets the output_type of this OperationVersionPatch.
        type of output (e.g. file, stream)

        :param output_type: The output_type of this OperationVersionPatch.
        :type: str
        """

        self._output_type = output_type

    @property
    def output_parameters(self):
        """
        Gets the output_parameters of this OperationVersionPatch.
        JSON-formatted dictionary containing parameters regarding the output (depending on the output type)

        :return: The output_parameters of this OperationVersionPatch.
        :rtype: str
        """
        return self._output_parameters

    @output_parameters.setter
    def output_parameters(self, output_parameters):
        """
        Sets the output_parameters of this OperationVersionPatch.
        JSON-formatted dictionary containing parameters regarding the output (depending on the output type)

        :param output_parameters: The output_parameters of this OperationVersionPatch.
        :type: str
        """

        self._output_parameters = output_parameters

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
