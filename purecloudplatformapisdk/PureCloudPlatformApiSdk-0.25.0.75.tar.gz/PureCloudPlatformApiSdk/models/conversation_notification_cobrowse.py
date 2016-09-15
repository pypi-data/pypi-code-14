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


class ConversationNotificationCobrowse(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        ConversationNotificationCobrowse - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'state': 'str',
            'disconnect_type': 'str',
            'id': 'str',
            'room_id': 'str',
            'cobrowse_session_id': 'str',
            'cobrowse_role': 'str',
            'controlling': 'list[str]',
            'viewer_url': 'str',
            'provider_event_time': 'int',
            'additional_properties': 'object'
        }

        self.attribute_map = {
            'state': 'state',
            'disconnect_type': 'disconnectType',
            'id': 'id',
            'room_id': 'roomId',
            'cobrowse_session_id': 'cobrowseSessionId',
            'cobrowse_role': 'cobrowseRole',
            'controlling': 'controlling',
            'viewer_url': 'viewerUrl',
            'provider_event_time': 'providerEventTime',
            'additional_properties': 'additionalProperties'
        }

        self._state = None
        self._disconnect_type = None
        self._id = None
        self._room_id = None
        self._cobrowse_session_id = None
        self._cobrowse_role = None
        self._controlling = None
        self._viewer_url = None
        self._provider_event_time = None
        self._additional_properties = None

    @property
    def state(self):
        """
        Gets the state of this ConversationNotificationCobrowse.


        :return: The state of this ConversationNotificationCobrowse.
        :rtype: str
        """
        return self._state

    @state.setter
    def state(self, state):
        """
        Sets the state of this ConversationNotificationCobrowse.


        :param state: The state of this ConversationNotificationCobrowse.
        :type: str
        """
        allowed_values = ["ALERTING", "DIALING", "CONTACTING", "OFFERING", "CONNECTED", "DISCONNECTED", "TERMINATED", "NONE"]
        if state not in allowed_values:
            raise ValueError(
                "Invalid value for `state`, must be one of {0}"
                .format(allowed_values)
            )

        self._state = state

    @property
    def disconnect_type(self):
        """
        Gets the disconnect_type of this ConversationNotificationCobrowse.


        :return: The disconnect_type of this ConversationNotificationCobrowse.
        :rtype: str
        """
        return self._disconnect_type

    @disconnect_type.setter
    def disconnect_type(self, disconnect_type):
        """
        Sets the disconnect_type of this ConversationNotificationCobrowse.


        :param disconnect_type: The disconnect_type of this ConversationNotificationCobrowse.
        :type: str
        """
        allowed_values = ["ENDPOINT", "CLIENT", "SYSTEM", "TIMEOUT", "TRANSFER", "TRANSFER_CONFERENCE", "TRANSFER_CONSULT", "TRANSFER_FORWARD", "TRANSPORT_FAILURE", "ERROR", "PEER", "OTHER", "SPAM"]
        if disconnect_type not in allowed_values:
            raise ValueError(
                "Invalid value for `disconnect_type`, must be one of {0}"
                .format(allowed_values)
            )

        self._disconnect_type = disconnect_type

    @property
    def id(self):
        """
        Gets the id of this ConversationNotificationCobrowse.


        :return: The id of this ConversationNotificationCobrowse.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this ConversationNotificationCobrowse.


        :param id: The id of this ConversationNotificationCobrowse.
        :type: str
        """
        
        self._id = id

    @property
    def room_id(self):
        """
        Gets the room_id of this ConversationNotificationCobrowse.


        :return: The room_id of this ConversationNotificationCobrowse.
        :rtype: str
        """
        return self._room_id

    @room_id.setter
    def room_id(self, room_id):
        """
        Sets the room_id of this ConversationNotificationCobrowse.


        :param room_id: The room_id of this ConversationNotificationCobrowse.
        :type: str
        """
        
        self._room_id = room_id

    @property
    def cobrowse_session_id(self):
        """
        Gets the cobrowse_session_id of this ConversationNotificationCobrowse.


        :return: The cobrowse_session_id of this ConversationNotificationCobrowse.
        :rtype: str
        """
        return self._cobrowse_session_id

    @cobrowse_session_id.setter
    def cobrowse_session_id(self, cobrowse_session_id):
        """
        Sets the cobrowse_session_id of this ConversationNotificationCobrowse.


        :param cobrowse_session_id: The cobrowse_session_id of this ConversationNotificationCobrowse.
        :type: str
        """
        
        self._cobrowse_session_id = cobrowse_session_id

    @property
    def cobrowse_role(self):
        """
        Gets the cobrowse_role of this ConversationNotificationCobrowse.


        :return: The cobrowse_role of this ConversationNotificationCobrowse.
        :rtype: str
        """
        return self._cobrowse_role

    @cobrowse_role.setter
    def cobrowse_role(self, cobrowse_role):
        """
        Sets the cobrowse_role of this ConversationNotificationCobrowse.


        :param cobrowse_role: The cobrowse_role of this ConversationNotificationCobrowse.
        :type: str
        """
        
        self._cobrowse_role = cobrowse_role

    @property
    def controlling(self):
        """
        Gets the controlling of this ConversationNotificationCobrowse.


        :return: The controlling of this ConversationNotificationCobrowse.
        :rtype: list[str]
        """
        return self._controlling

    @controlling.setter
    def controlling(self, controlling):
        """
        Sets the controlling of this ConversationNotificationCobrowse.


        :param controlling: The controlling of this ConversationNotificationCobrowse.
        :type: list[str]
        """
        
        self._controlling = controlling

    @property
    def viewer_url(self):
        """
        Gets the viewer_url of this ConversationNotificationCobrowse.


        :return: The viewer_url of this ConversationNotificationCobrowse.
        :rtype: str
        """
        return self._viewer_url

    @viewer_url.setter
    def viewer_url(self, viewer_url):
        """
        Sets the viewer_url of this ConversationNotificationCobrowse.


        :param viewer_url: The viewer_url of this ConversationNotificationCobrowse.
        :type: str
        """
        
        self._viewer_url = viewer_url

    @property
    def provider_event_time(self):
        """
        Gets the provider_event_time of this ConversationNotificationCobrowse.


        :return: The provider_event_time of this ConversationNotificationCobrowse.
        :rtype: int
        """
        return self._provider_event_time

    @provider_event_time.setter
    def provider_event_time(self, provider_event_time):
        """
        Sets the provider_event_time of this ConversationNotificationCobrowse.


        :param provider_event_time: The provider_event_time of this ConversationNotificationCobrowse.
        :type: int
        """
        
        self._provider_event_time = provider_event_time

    @property
    def additional_properties(self):
        """
        Gets the additional_properties of this ConversationNotificationCobrowse.


        :return: The additional_properties of this ConversationNotificationCobrowse.
        :rtype: object
        """
        return self._additional_properties

    @additional_properties.setter
    def additional_properties(self, additional_properties):
        """
        Sets the additional_properties of this ConversationNotificationCobrowse.


        :param additional_properties: The additional_properties of this ConversationNotificationCobrowse.
        :type: object
        """
        
        self._additional_properties = additional_properties

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

