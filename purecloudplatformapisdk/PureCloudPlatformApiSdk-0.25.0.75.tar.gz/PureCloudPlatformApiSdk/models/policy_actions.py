# coding: utf-8

"""
Copyright 2016 SmartBear Software

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

    Ref: https://github.com/swagger-api/swagger-codegen
"""

from pprint import pformat
from six import iteritems
import re


class PolicyActions(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        PolicyActions - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'retain_recording': 'bool',
            'delete_recording': 'bool',
            'always_delete': 'bool',
            'assign_evaluations': 'list[EvaluationAssignment]',
            'assign_metered_evaluations': 'list[MeteredEvaluationAssignment]',
            'assign_calibrations': 'list[CalibrationAssignment]',
            'retention_duration': 'RetentionDuration',
            'initiate_screen_recording': 'InitiateScreenRecording'
        }

        self.attribute_map = {
            'retain_recording': 'retainRecording',
            'delete_recording': 'deleteRecording',
            'always_delete': 'alwaysDelete',
            'assign_evaluations': 'assignEvaluations',
            'assign_metered_evaluations': 'assignMeteredEvaluations',
            'assign_calibrations': 'assignCalibrations',
            'retention_duration': 'retentionDuration',
            'initiate_screen_recording': 'initiateScreenRecording'
        }

        self._retain_recording = False
        self._delete_recording = False
        self._always_delete = False
        self._assign_evaluations = None
        self._assign_metered_evaluations = None
        self._assign_calibrations = None
        self._retention_duration = None
        self._initiate_screen_recording = None

    @property
    def retain_recording(self):
        """
        Gets the retain_recording of this PolicyActions.
        true to retain the recording associated with the conversation. Default = true

        :return: The retain_recording of this PolicyActions.
        :rtype: bool
        """
        return self._retain_recording

    @retain_recording.setter
    def retain_recording(self, retain_recording):
        """
        Sets the retain_recording of this PolicyActions.
        true to retain the recording associated with the conversation. Default = true

        :param retain_recording: The retain_recording of this PolicyActions.
        :type: bool
        """
        
        self._retain_recording = retain_recording

    @property
    def delete_recording(self):
        """
        Gets the delete_recording of this PolicyActions.
        true to delete the recording associated with the conversation. If retainRecording = true, this will be ignored. Default = false

        :return: The delete_recording of this PolicyActions.
        :rtype: bool
        """
        return self._delete_recording

    @delete_recording.setter
    def delete_recording(self, delete_recording):
        """
        Sets the delete_recording of this PolicyActions.
        true to delete the recording associated with the conversation. If retainRecording = true, this will be ignored. Default = false

        :param delete_recording: The delete_recording of this PolicyActions.
        :type: bool
        """
        
        self._delete_recording = delete_recording

    @property
    def always_delete(self):
        """
        Gets the always_delete of this PolicyActions.
        true to delete the recording associated with the conversation regardless of the values of retainRecording or deleteRecording. Default = false

        :return: The always_delete of this PolicyActions.
        :rtype: bool
        """
        return self._always_delete

    @always_delete.setter
    def always_delete(self, always_delete):
        """
        Sets the always_delete of this PolicyActions.
        true to delete the recording associated with the conversation regardless of the values of retainRecording or deleteRecording. Default = false

        :param always_delete: The always_delete of this PolicyActions.
        :type: bool
        """
        
        self._always_delete = always_delete

    @property
    def assign_evaluations(self):
        """
        Gets the assign_evaluations of this PolicyActions.


        :return: The assign_evaluations of this PolicyActions.
        :rtype: list[EvaluationAssignment]
        """
        return self._assign_evaluations

    @assign_evaluations.setter
    def assign_evaluations(self, assign_evaluations):
        """
        Sets the assign_evaluations of this PolicyActions.


        :param assign_evaluations: The assign_evaluations of this PolicyActions.
        :type: list[EvaluationAssignment]
        """
        
        self._assign_evaluations = assign_evaluations

    @property
    def assign_metered_evaluations(self):
        """
        Gets the assign_metered_evaluations of this PolicyActions.


        :return: The assign_metered_evaluations of this PolicyActions.
        :rtype: list[MeteredEvaluationAssignment]
        """
        return self._assign_metered_evaluations

    @assign_metered_evaluations.setter
    def assign_metered_evaluations(self, assign_metered_evaluations):
        """
        Sets the assign_metered_evaluations of this PolicyActions.


        :param assign_metered_evaluations: The assign_metered_evaluations of this PolicyActions.
        :type: list[MeteredEvaluationAssignment]
        """
        
        self._assign_metered_evaluations = assign_metered_evaluations

    @property
    def assign_calibrations(self):
        """
        Gets the assign_calibrations of this PolicyActions.


        :return: The assign_calibrations of this PolicyActions.
        :rtype: list[CalibrationAssignment]
        """
        return self._assign_calibrations

    @assign_calibrations.setter
    def assign_calibrations(self, assign_calibrations):
        """
        Sets the assign_calibrations of this PolicyActions.


        :param assign_calibrations: The assign_calibrations of this PolicyActions.
        :type: list[CalibrationAssignment]
        """
        
        self._assign_calibrations = assign_calibrations

    @property
    def retention_duration(self):
        """
        Gets the retention_duration of this PolicyActions.


        :return: The retention_duration of this PolicyActions.
        :rtype: RetentionDuration
        """
        return self._retention_duration

    @retention_duration.setter
    def retention_duration(self, retention_duration):
        """
        Sets the retention_duration of this PolicyActions.


        :param retention_duration: The retention_duration of this PolicyActions.
        :type: RetentionDuration
        """
        
        self._retention_duration = retention_duration

    @property
    def initiate_screen_recording(self):
        """
        Gets the initiate_screen_recording of this PolicyActions.


        :return: The initiate_screen_recording of this PolicyActions.
        :rtype: InitiateScreenRecording
        """
        return self._initiate_screen_recording

    @initiate_screen_recording.setter
    def initiate_screen_recording(self, initiate_screen_recording):
        """
        Sets the initiate_screen_recording of this PolicyActions.


        :param initiate_screen_recording: The initiate_screen_recording of this PolicyActions.
        :type: InitiateScreenRecording
        """
        
        self._initiate_screen_recording = initiate_screen_recording

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

