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


class ServicePrincipalCreateParameters(Model):
    """Request parameters for create a new service principal.

    :param app_id: application Id
    :type app_id: str
    :param account_enabled: Specifies if the account is enabled
    :type account_enabled: bool
    :param key_credentials: the list of KeyCredential objects
    :type key_credentials: list of :class:`KeyCredential
     <azure.graphrbac.models.KeyCredential>`
    :param password_credentials: the list of PasswordCredential objects
    :type password_credentials: list of :class:`PasswordCredential
     <azure.graphrbac.models.PasswordCredential>`
    """ 

    _validation = {
        'app_id': {'required': True},
        'account_enabled': {'required': True},
    }

    _attribute_map = {
        'app_id': {'key': 'appId', 'type': 'str'},
        'account_enabled': {'key': 'accountEnabled', 'type': 'bool'},
        'key_credentials': {'key': 'keyCredentials', 'type': '[KeyCredential]'},
        'password_credentials': {'key': 'passwordCredentials', 'type': '[PasswordCredential]'},
    }

    def __init__(self, app_id, account_enabled, key_credentials=None, password_credentials=None):
        self.app_id = app_id
        self.account_enabled = account_enabled
        self.key_credentials = key_credentials
        self.password_credentials = password_credentials
