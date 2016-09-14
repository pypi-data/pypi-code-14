# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
#
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class RoleAssignment(Model):
    """Role Assignments.

    :param id: Gets or sets role assignment id.
    :type id: str
    :param name: Gets or sets role assignment name.
    :type name: str
    :param type: Gets or sets role assignment type.
    :type type: str
    :param properties: Gets or sets role assignment properties.
    :type properties: :class:`RoleAssignmentPropertiesWithScope
     <azure.mgmt.authorization.models.RoleAssignmentPropertiesWithScope>`
    """ 

    _attribute_map = {
        'id': {'key': 'id', 'type': 'str'},
        'name': {'key': 'name', 'type': 'str'},
        'type': {'key': 'type', 'type': 'str'},
        'properties': {'key': 'properties', 'type': 'RoleAssignmentPropertiesWithScope'},
    }

    def __init__(self, id=None, name=None, type=None, properties=None):
        self.id = id
        self.name = name
        self.type = type
        self.properties = properties
