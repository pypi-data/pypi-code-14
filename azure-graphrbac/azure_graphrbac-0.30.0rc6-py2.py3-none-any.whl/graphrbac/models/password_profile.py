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


class PasswordProfile(Model):
    """Contains the password profile associated with a user.

    :param password: Password
    :type password: str
    :param force_change_password_next_login: Force change password on next
     login
    :type force_change_password_next_login: bool
    """ 

    _validation = {
        'password': {'required': True},
    }

    _attribute_map = {
        'password': {'key': 'password', 'type': 'str'},
        'force_change_password_next_login': {'key': 'forceChangePasswordNextLogin', 'type': 'bool'},
    }

    def __init__(self, password, force_change_password_next_login=None):
        self.password = password
        self.force_change_password_next_login = force_change_password_next_login
