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


class OutboundRoute(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        OutboundRoute - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'id': 'str',
            'name': 'str',
            'description': 'str',
            'version': 'int',
            'date_created': 'datetime',
            'date_modified': 'datetime',
            'modified_by': 'str',
            'created_by': 'str',
            'state': 'str',
            'modified_by_app': 'str',
            'created_by_app': 'str',
            'site': 'Site',
            'classification_types': 'list[str]',
            'enabled': 'bool',
            'distribution': 'str',
            'managed': 'bool',
            'external_trunk_bases': 'list[UriReference]',
            'self_uri': 'str'
        }

        self.attribute_map = {
            'id': 'id',
            'name': 'name',
            'description': 'description',
            'version': 'version',
            'date_created': 'dateCreated',
            'date_modified': 'dateModified',
            'modified_by': 'modifiedBy',
            'created_by': 'createdBy',
            'state': 'state',
            'modified_by_app': 'modifiedByApp',
            'created_by_app': 'createdByApp',
            'site': 'site',
            'classification_types': 'classificationTypes',
            'enabled': 'enabled',
            'distribution': 'distribution',
            'managed': 'managed',
            'external_trunk_bases': 'externalTrunkBases',
            'self_uri': 'selfUri'
        }

        self._id = None
        self._name = None
        self._description = None
        self._version = None
        self._date_created = None
        self._date_modified = None
        self._modified_by = None
        self._created_by = None
        self._state = None
        self._modified_by_app = None
        self._created_by_app = None
        self._site = None
        self._classification_types = None
        self._enabled = False
        self._distribution = None
        self._managed = False
        self._external_trunk_bases = None
        self._self_uri = None

    @property
    def id(self):
        """
        Gets the id of this OutboundRoute.
        The globally unique identifier for the object.

        :return: The id of this OutboundRoute.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this OutboundRoute.
        The globally unique identifier for the object.

        :param id: The id of this OutboundRoute.
        :type: str
        """
        
        self._id = id

    @property
    def name(self):
        """
        Gets the name of this OutboundRoute.
        The name of the entity.

        :return: The name of this OutboundRoute.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this OutboundRoute.
        The name of the entity.

        :param name: The name of this OutboundRoute.
        :type: str
        """
        
        self._name = name

    @property
    def description(self):
        """
        Gets the description of this OutboundRoute.


        :return: The description of this OutboundRoute.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this OutboundRoute.


        :param description: The description of this OutboundRoute.
        :type: str
        """
        
        self._description = description

    @property
    def version(self):
        """
        Gets the version of this OutboundRoute.


        :return: The version of this OutboundRoute.
        :rtype: int
        """
        return self._version

    @version.setter
    def version(self, version):
        """
        Sets the version of this OutboundRoute.


        :param version: The version of this OutboundRoute.
        :type: int
        """
        
        self._version = version

    @property
    def date_created(self):
        """
        Gets the date_created of this OutboundRoute.
        Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss.SSSZ

        :return: The date_created of this OutboundRoute.
        :rtype: datetime
        """
        return self._date_created

    @date_created.setter
    def date_created(self, date_created):
        """
        Sets the date_created of this OutboundRoute.
        Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss.SSSZ

        :param date_created: The date_created of this OutboundRoute.
        :type: datetime
        """
        
        self._date_created = date_created

    @property
    def date_modified(self):
        """
        Gets the date_modified of this OutboundRoute.
        Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss.SSSZ

        :return: The date_modified of this OutboundRoute.
        :rtype: datetime
        """
        return self._date_modified

    @date_modified.setter
    def date_modified(self, date_modified):
        """
        Sets the date_modified of this OutboundRoute.
        Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss.SSSZ

        :param date_modified: The date_modified of this OutboundRoute.
        :type: datetime
        """
        
        self._date_modified = date_modified

    @property
    def modified_by(self):
        """
        Gets the modified_by of this OutboundRoute.


        :return: The modified_by of this OutboundRoute.
        :rtype: str
        """
        return self._modified_by

    @modified_by.setter
    def modified_by(self, modified_by):
        """
        Sets the modified_by of this OutboundRoute.


        :param modified_by: The modified_by of this OutboundRoute.
        :type: str
        """
        
        self._modified_by = modified_by

    @property
    def created_by(self):
        """
        Gets the created_by of this OutboundRoute.


        :return: The created_by of this OutboundRoute.
        :rtype: str
        """
        return self._created_by

    @created_by.setter
    def created_by(self, created_by):
        """
        Sets the created_by of this OutboundRoute.


        :param created_by: The created_by of this OutboundRoute.
        :type: str
        """
        
        self._created_by = created_by

    @property
    def state(self):
        """
        Gets the state of this OutboundRoute.


        :return: The state of this OutboundRoute.
        :rtype: str
        """
        return self._state

    @state.setter
    def state(self, state):
        """
        Sets the state of this OutboundRoute.


        :param state: The state of this OutboundRoute.
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
    def modified_by_app(self):
        """
        Gets the modified_by_app of this OutboundRoute.


        :return: The modified_by_app of this OutboundRoute.
        :rtype: str
        """
        return self._modified_by_app

    @modified_by_app.setter
    def modified_by_app(self, modified_by_app):
        """
        Sets the modified_by_app of this OutboundRoute.


        :param modified_by_app: The modified_by_app of this OutboundRoute.
        :type: str
        """
        
        self._modified_by_app = modified_by_app

    @property
    def created_by_app(self):
        """
        Gets the created_by_app of this OutboundRoute.


        :return: The created_by_app of this OutboundRoute.
        :rtype: str
        """
        return self._created_by_app

    @created_by_app.setter
    def created_by_app(self, created_by_app):
        """
        Sets the created_by_app of this OutboundRoute.


        :param created_by_app: The created_by_app of this OutboundRoute.
        :type: str
        """
        
        self._created_by_app = created_by_app

    @property
    def site(self):
        """
        Gets the site of this OutboundRoute.
        The site associated to the outbound route.

        :return: The site of this OutboundRoute.
        :rtype: Site
        """
        return self._site

    @site.setter
    def site(self, site):
        """
        Sets the site of this OutboundRoute.
        The site associated to the outbound route.

        :param site: The site of this OutboundRoute.
        :type: Site
        """
        
        self._site = site

    @property
    def classification_types(self):
        """
        Gets the classification_types of this OutboundRoute.


        :return: The classification_types of this OutboundRoute.
        :rtype: list[str]
        """
        return self._classification_types

    @classification_types.setter
    def classification_types(self, classification_types):
        """
        Sets the classification_types of this OutboundRoute.


        :param classification_types: The classification_types of this OutboundRoute.
        :type: list[str]
        """
        
        self._classification_types = classification_types

    @property
    def enabled(self):
        """
        Gets the enabled of this OutboundRoute.


        :return: The enabled of this OutboundRoute.
        :rtype: bool
        """
        return self._enabled

    @enabled.setter
    def enabled(self, enabled):
        """
        Sets the enabled of this OutboundRoute.


        :param enabled: The enabled of this OutboundRoute.
        :type: bool
        """
        
        self._enabled = enabled

    @property
    def distribution(self):
        """
        Gets the distribution of this OutboundRoute.


        :return: The distribution of this OutboundRoute.
        :rtype: str
        """
        return self._distribution

    @distribution.setter
    def distribution(self, distribution):
        """
        Sets the distribution of this OutboundRoute.


        :param distribution: The distribution of this OutboundRoute.
        :type: str
        """
        allowed_values = ["SEQUENTIAL", "RANDOM"]
        if distribution not in allowed_values:
            raise ValueError(
                "Invalid value for `distribution`, must be one of {0}"
                .format(allowed_values)
            )

        self._distribution = distribution

    @property
    def managed(self):
        """
        Gets the managed of this OutboundRoute.


        :return: The managed of this OutboundRoute.
        :rtype: bool
        """
        return self._managed

    @managed.setter
    def managed(self, managed):
        """
        Sets the managed of this OutboundRoute.


        :param managed: The managed of this OutboundRoute.
        :type: bool
        """
        
        self._managed = managed

    @property
    def external_trunk_bases(self):
        """
        Gets the external_trunk_bases of this OutboundRoute.
        Trunk base settings of trunkType \"EXTERNAL\".  This base must also be set on an edge logical interface for correct routing.

        :return: The external_trunk_bases of this OutboundRoute.
        :rtype: list[UriReference]
        """
        return self._external_trunk_bases

    @external_trunk_bases.setter
    def external_trunk_bases(self, external_trunk_bases):
        """
        Sets the external_trunk_bases of this OutboundRoute.
        Trunk base settings of trunkType \"EXTERNAL\".  This base must also be set on an edge logical interface for correct routing.

        :param external_trunk_bases: The external_trunk_bases of this OutboundRoute.
        :type: list[UriReference]
        """
        
        self._external_trunk_bases = external_trunk_bases

    @property
    def self_uri(self):
        """
        Gets the self_uri of this OutboundRoute.
        The URI for this object

        :return: The self_uri of this OutboundRoute.
        :rtype: str
        """
        return self._self_uri

    @self_uri.setter
    def self_uri(self, self_uri):
        """
        Sets the self_uri of this OutboundRoute.
        The URI for this object

        :param self_uri: The self_uri of this OutboundRoute.
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

