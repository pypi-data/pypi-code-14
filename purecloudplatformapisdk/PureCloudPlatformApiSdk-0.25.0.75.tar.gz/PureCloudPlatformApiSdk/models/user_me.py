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


class UserMe(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        UserMe - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'id': 'str',
            'name': 'str',
            'chat': 'Chat',
            'department': 'str',
            'email': 'str',
            'primary_contact_info': 'list[Contact]',
            'addresses': 'list[Contact]',
            'state': 'str',
            'title': 'str',
            'username': 'str',
            'images': 'list[UserImage]',
            'version': 'int',
            'routing_status': 'RoutingStatus',
            'presence': 'UserPresence',
            'conversation_summary': 'UserConversationSummary',
            'out_of_office': 'OutOfOffice',
            'geolocation': 'Geolocation',
            'station': 'UserStations',
            'authorization': 'UserAuthorization',
            'profile_skills': 'list[str]',
            'date': 'ServerDate',
            'geolocation_settings': 'GeolocationSettings',
            'organization': 'Organization',
            'presence_definitions': 'list[OrganizationPresence]',
            'locations': 'list[Location]',
            'self_uri': 'str'
        }

        self.attribute_map = {
            'id': 'id',
            'name': 'name',
            'chat': 'chat',
            'department': 'department',
            'email': 'email',
            'primary_contact_info': 'primaryContactInfo',
            'addresses': 'addresses',
            'state': 'state',
            'title': 'title',
            'username': 'username',
            'images': 'images',
            'version': 'version',
            'routing_status': 'routingStatus',
            'presence': 'presence',
            'conversation_summary': 'conversationSummary',
            'out_of_office': 'outOfOffice',
            'geolocation': 'geolocation',
            'station': 'station',
            'authorization': 'authorization',
            'profile_skills': 'profileSkills',
            'date': 'date',
            'geolocation_settings': 'geolocationSettings',
            'organization': 'organization',
            'presence_definitions': 'presenceDefinitions',
            'locations': 'locations',
            'self_uri': 'selfUri'
        }

        self._id = None
        self._name = None
        self._chat = None
        self._department = None
        self._email = None
        self._primary_contact_info = None
        self._addresses = None
        self._state = None
        self._title = None
        self._username = None
        self._images = None
        self._version = None
        self._routing_status = None
        self._presence = None
        self._conversation_summary = None
        self._out_of_office = None
        self._geolocation = None
        self._station = None
        self._authorization = None
        self._profile_skills = None
        self._date = None
        self._geolocation_settings = None
        self._organization = None
        self._presence_definitions = None
        self._locations = None
        self._self_uri = None

    @property
    def id(self):
        """
        Gets the id of this UserMe.
        The globally unique identifier for the object.

        :return: The id of this UserMe.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this UserMe.
        The globally unique identifier for the object.

        :param id: The id of this UserMe.
        :type: str
        """
        
        self._id = id

    @property
    def name(self):
        """
        Gets the name of this UserMe.


        :return: The name of this UserMe.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this UserMe.


        :param name: The name of this UserMe.
        :type: str
        """
        
        self._name = name

    @property
    def chat(self):
        """
        Gets the chat of this UserMe.


        :return: The chat of this UserMe.
        :rtype: Chat
        """
        return self._chat

    @chat.setter
    def chat(self, chat):
        """
        Sets the chat of this UserMe.


        :param chat: The chat of this UserMe.
        :type: Chat
        """
        
        self._chat = chat

    @property
    def department(self):
        """
        Gets the department of this UserMe.


        :return: The department of this UserMe.
        :rtype: str
        """
        return self._department

    @department.setter
    def department(self, department):
        """
        Sets the department of this UserMe.


        :param department: The department of this UserMe.
        :type: str
        """
        
        self._department = department

    @property
    def email(self):
        """
        Gets the email of this UserMe.


        :return: The email of this UserMe.
        :rtype: str
        """
        return self._email

    @email.setter
    def email(self, email):
        """
        Sets the email of this UserMe.


        :param email: The email of this UserMe.
        :type: str
        """
        
        self._email = email

    @property
    def primary_contact_info(self):
        """
        Gets the primary_contact_info of this UserMe.
        Auto populated from addresses.

        :return: The primary_contact_info of this UserMe.
        :rtype: list[Contact]
        """
        return self._primary_contact_info

    @primary_contact_info.setter
    def primary_contact_info(self, primary_contact_info):
        """
        Sets the primary_contact_info of this UserMe.
        Auto populated from addresses.

        :param primary_contact_info: The primary_contact_info of this UserMe.
        :type: list[Contact]
        """
        
        self._primary_contact_info = primary_contact_info

    @property
    def addresses(self):
        """
        Gets the addresses of this UserMe.
        Email addresses and phone numbers for this user

        :return: The addresses of this UserMe.
        :rtype: list[Contact]
        """
        return self._addresses

    @addresses.setter
    def addresses(self, addresses):
        """
        Sets the addresses of this UserMe.
        Email addresses and phone numbers for this user

        :param addresses: The addresses of this UserMe.
        :type: list[Contact]
        """
        
        self._addresses = addresses

    @property
    def state(self):
        """
        Gets the state of this UserMe.
        The current state for this user.

        :return: The state of this UserMe.
        :rtype: str
        """
        return self._state

    @state.setter
    def state(self, state):
        """
        Sets the state of this UserMe.
        The current state for this user.

        :param state: The state of this UserMe.
        :type: str
        """
        allowed_values = ["active", "inactive", "deleted"]
        if state not in allowed_values:
            raise ValueError(
                "Invalid value for `state`, must be one of {0}"
                .format(allowed_values)
            )

        self._state = state

    @property
    def title(self):
        """
        Gets the title of this UserMe.


        :return: The title of this UserMe.
        :rtype: str
        """
        return self._title

    @title.setter
    def title(self, title):
        """
        Sets the title of this UserMe.


        :param title: The title of this UserMe.
        :type: str
        """
        
        self._title = title

    @property
    def username(self):
        """
        Gets the username of this UserMe.


        :return: The username of this UserMe.
        :rtype: str
        """
        return self._username

    @username.setter
    def username(self, username):
        """
        Sets the username of this UserMe.


        :param username: The username of this UserMe.
        :type: str
        """
        
        self._username = username

    @property
    def images(self):
        """
        Gets the images of this UserMe.


        :return: The images of this UserMe.
        :rtype: list[UserImage]
        """
        return self._images

    @images.setter
    def images(self, images):
        """
        Sets the images of this UserMe.


        :param images: The images of this UserMe.
        :type: list[UserImage]
        """
        
        self._images = images

    @property
    def version(self):
        """
        Gets the version of this UserMe.
        Required when updating a user, this value should be the current version of the user.  The current version can be obtained with a GET on the user before doing a PATCH.

        :return: The version of this UserMe.
        :rtype: int
        """
        return self._version

    @version.setter
    def version(self, version):
        """
        Sets the version of this UserMe.
        Required when updating a user, this value should be the current version of the user.  The current version can be obtained with a GET on the user before doing a PATCH.

        :param version: The version of this UserMe.
        :type: int
        """
        
        self._version = version

    @property
    def routing_status(self):
        """
        Gets the routing_status of this UserMe.
        ACD routing status

        :return: The routing_status of this UserMe.
        :rtype: RoutingStatus
        """
        return self._routing_status

    @routing_status.setter
    def routing_status(self, routing_status):
        """
        Sets the routing_status of this UserMe.
        ACD routing status

        :param routing_status: The routing_status of this UserMe.
        :type: RoutingStatus
        """
        
        self._routing_status = routing_status

    @property
    def presence(self):
        """
        Gets the presence of this UserMe.
        Active presence

        :return: The presence of this UserMe.
        :rtype: UserPresence
        """
        return self._presence

    @presence.setter
    def presence(self, presence):
        """
        Sets the presence of this UserMe.
        Active presence

        :param presence: The presence of this UserMe.
        :type: UserPresence
        """
        
        self._presence = presence

    @property
    def conversation_summary(self):
        """
        Gets the conversation_summary of this UserMe.
        Summary of conversion statistics for conversation types.

        :return: The conversation_summary of this UserMe.
        :rtype: UserConversationSummary
        """
        return self._conversation_summary

    @conversation_summary.setter
    def conversation_summary(self, conversation_summary):
        """
        Sets the conversation_summary of this UserMe.
        Summary of conversion statistics for conversation types.

        :param conversation_summary: The conversation_summary of this UserMe.
        :type: UserConversationSummary
        """
        
        self._conversation_summary = conversation_summary

    @property
    def out_of_office(self):
        """
        Gets the out_of_office of this UserMe.
        Determine if out of office is enabled

        :return: The out_of_office of this UserMe.
        :rtype: OutOfOffice
        """
        return self._out_of_office

    @out_of_office.setter
    def out_of_office(self, out_of_office):
        """
        Sets the out_of_office of this UserMe.
        Determine if out of office is enabled

        :param out_of_office: The out_of_office of this UserMe.
        :type: OutOfOffice
        """
        
        self._out_of_office = out_of_office

    @property
    def geolocation(self):
        """
        Gets the geolocation of this UserMe.
        Current geolocation position

        :return: The geolocation of this UserMe.
        :rtype: Geolocation
        """
        return self._geolocation

    @geolocation.setter
    def geolocation(self, geolocation):
        """
        Sets the geolocation of this UserMe.
        Current geolocation position

        :param geolocation: The geolocation of this UserMe.
        :type: Geolocation
        """
        
        self._geolocation = geolocation

    @property
    def station(self):
        """
        Gets the station of this UserMe.
        Effective, default, and last station information

        :return: The station of this UserMe.
        :rtype: UserStations
        """
        return self._station

    @station.setter
    def station(self, station):
        """
        Sets the station of this UserMe.
        Effective, default, and last station information

        :param station: The station of this UserMe.
        :type: UserStations
        """
        
        self._station = station

    @property
    def authorization(self):
        """
        Gets the authorization of this UserMe.
        Roles and permissions assigned to the user

        :return: The authorization of this UserMe.
        :rtype: UserAuthorization
        """
        return self._authorization

    @authorization.setter
    def authorization(self, authorization):
        """
        Sets the authorization of this UserMe.
        Roles and permissions assigned to the user

        :param authorization: The authorization of this UserMe.
        :type: UserAuthorization
        """
        
        self._authorization = authorization

    @property
    def profile_skills(self):
        """
        Gets the profile_skills of this UserMe.
        Skills possessed by the user

        :return: The profile_skills of this UserMe.
        :rtype: list[str]
        """
        return self._profile_skills

    @profile_skills.setter
    def profile_skills(self, profile_skills):
        """
        Sets the profile_skills of this UserMe.
        Skills possessed by the user

        :param profile_skills: The profile_skills of this UserMe.
        :type: list[str]
        """
        
        self._profile_skills = profile_skills

    @property
    def date(self):
        """
        Gets the date of this UserMe.
        The PureCloud system date time.

        :return: The date of this UserMe.
        :rtype: ServerDate
        """
        return self._date

    @date.setter
    def date(self, date):
        """
        Sets the date of this UserMe.
        The PureCloud system date time.

        :param date: The date of this UserMe.
        :type: ServerDate
        """
        
        self._date = date

    @property
    def geolocation_settings(self):
        """
        Gets the geolocation_settings of this UserMe.
        Geolocation settings for user's organization.

        :return: The geolocation_settings of this UserMe.
        :rtype: GeolocationSettings
        """
        return self._geolocation_settings

    @geolocation_settings.setter
    def geolocation_settings(self, geolocation_settings):
        """
        Sets the geolocation_settings of this UserMe.
        Geolocation settings for user's organization.

        :param geolocation_settings: The geolocation_settings of this UserMe.
        :type: GeolocationSettings
        """
        
        self._geolocation_settings = geolocation_settings

    @property
    def organization(self):
        """
        Gets the organization of this UserMe.
        Organization details for this user.

        :return: The organization of this UserMe.
        :rtype: Organization
        """
        return self._organization

    @organization.setter
    def organization(self, organization):
        """
        Sets the organization of this UserMe.
        Organization details for this user.

        :param organization: The organization of this UserMe.
        :type: Organization
        """
        
        self._organization = organization

    @property
    def presence_definitions(self):
        """
        Gets the presence_definitions of this UserMe.
        The first 100 presence definitions for user's organization.

        :return: The presence_definitions of this UserMe.
        :rtype: list[OrganizationPresence]
        """
        return self._presence_definitions

    @presence_definitions.setter
    def presence_definitions(self, presence_definitions):
        """
        Sets the presence_definitions of this UserMe.
        The first 100 presence definitions for user's organization.

        :param presence_definitions: The presence_definitions of this UserMe.
        :type: list[OrganizationPresence]
        """
        
        self._presence_definitions = presence_definitions

    @property
    def locations(self):
        """
        Gets the locations of this UserMe.
        The first 100 locations for user's organization

        :return: The locations of this UserMe.
        :rtype: list[Location]
        """
        return self._locations

    @locations.setter
    def locations(self, locations):
        """
        Sets the locations of this UserMe.
        The first 100 locations for user's organization

        :param locations: The locations of this UserMe.
        :type: list[Location]
        """
        
        self._locations = locations

    @property
    def self_uri(self):
        """
        Gets the self_uri of this UserMe.
        The URI for this object

        :return: The self_uri of this UserMe.
        :rtype: str
        """
        return self._self_uri

    @self_uri.setter
    def self_uri(self, self_uri):
        """
        Sets the self_uri of this UserMe.
        The URI for this object

        :param self_uri: The self_uri of this UserMe.
        :type: str
        """
        
        self._self_uri = self_uri

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

