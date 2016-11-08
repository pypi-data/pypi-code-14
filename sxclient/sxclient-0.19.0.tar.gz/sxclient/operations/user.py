'''
Copyright (C) 2015-2016 Skylable Ltd. <info-copyright@skylable.com>
License: Apache 2.0, see LICENSE for more details.
'''

from __future__ import unicode_literals

from typing import Optional  # noqa

from sxclient.operations.base import BaseOperation
from sxclient.models.query_parameters import QueryParameters


__all__ = [
    'ListUsers', 'GetUser', 'CreateUser', 'ModifyUser', 'RemoveUser', 'WhoAmI'
]


class ListUsers(BaseOperation):
    '''
    List all users in the cluster, along with additional information.

    Required access: admin.

    Query-specific parameters:
      - clones -- if not None, list only the clones of the user named by the
        parameter value
    '''

    def _generate_query_params(self, clones=None):
        # type: (Optional[bool]) -> QueryParameters
        dict_params = {}
        if clones is not None:
            dict_params['clones'] = clones
        return QueryParameters(
            sx_verb='GET',
            path_items=['.users'],
            bool_params={'desc', 'quota'},
            dict_params=dict_params
        )


class GetUser(BaseOperation):
    '''
    Get key components, name and role of the user.

    Required access: admin.

    Query-specific parameters:
      - userName -- name of the user for whom the data will be obtained
    '''
    def _generate_query_params(self, userName):
        # type: (str) -> QueryParameters
        return QueryParameters(
            sx_verb='GET',
            path_items=['.users', userName]
        )


class CreateUser(BaseOperation):
    '''
    Create a new cluster user.

    Required access: admin.

    Query-specific parameters:
      - userName -- name of the user to be created
      - userType -- role of the user (either "normal" or "admin")
      - userKey -- lowercase hex encoded 20 byte user key
      - quota -- quota for all volume sized owned by the user; if 0 or
        None, quota is unlimited
      - desc -- description of the user; if None, it is set to an empty
        string
      - existingName -- name of an existing user to create a clone of; if None,
        a new user will be created
    '''

    def _generate_body(
        self, userName, userType, userKey, quota=None, desc=None,
        existingName=None
    ):
        # type: (str, str, str, Optional[int], Optional[str], Optional[str]) -> dict  # noqa
        body = {
            'userName': userName,
            'userType': userType,
            'userKey': userKey
        }  # type: dict
        if quota is not None:
            body['userQuota'] = quota
        if desc is not None:
            body['userDesc'] = desc
        if existingName is not None:
            body['existingName'] = existingName
        return body

    def _generate_query_params(
        self, userName, userType, userKey, quota=None, desc=None,
        existingName=None
    ):
        # type: (str, str, str, Optional[int], Optional[str], Optional[str]) -> QueryParameters  # noqa
        return QueryParameters(
            sx_verb='JOB_PUT',
            path_items=['.users']
        )


class ModifyUser(BaseOperation):
    '''
    Update properties of an existing user.

    Required access: normal (own key) / admin (any property)

    Query-specific parameters:
      - userName -- name of the user whose key is to be changed
      - userKey -- new lowercase hex encoded 20 byte user key; if None, user
        key will not be changed
      - quota -- new user quota; if set to 0, the quota will be unlimited; if
        None, quota will not be changed
      - desc -- new user description; if None, description will not be changed

    Note: at least one of userKey, quota, desc has to be provided and not be
    None for the query to succeed.
    '''

    def _generate_body(self, userName, userKey=None, quota=None, desc=None):
        # type: (str, Optional[str], Optional[int], Optional[str]) -> dict  # noqa
        body = {}  # type: dict

        if userKey is not None:
            body['userKey'] = userKey
        if quota is not None:
            body['quota'] = int(quota)
        if desc is not None:
            body['desc'] = desc
        if not body:
            raise ValueError('One of userKey, quota, desc has to be not None')

        return body

    def _generate_query_params(
        self, userName, userKey=None, quota=None, desc=None
    ):
        # type: (str, Optional[str], Optional[int], Optional[str]) -> QueryParameters  # noqa
        return QueryParameters(
            sx_verb='JOB_PUT',
            path_items=['.users', userName]
        )


class RemoveUser(BaseOperation):
    '''
    Remove an existing cluster user.

    Required access: admin.

    Query-specific parameters:
      - userName -- name of the user to be deleted
      - all -- if set to True, additionally remove all user's clones
    '''

    def _generate_query_params(self, userName, all=False):
        # type: (str, Optional[bool]) -> QueryParameters  # noqa
        bool_params = set()
        if all:
            bool_params.add('all')
        return QueryParameters(
            sx_verb='JOB_DELETE',
            path_items=['.users', userName],
            bool_params=bool_params
        )


class WhoAmI(BaseOperation):
    '''
    Returns details of the authenticated SX cluster user.

    Required access: ordinary user
    '''

    def _generate_query_params(self):
        # type: () -> QueryParameters  # noqa
        return QueryParameters(
            sx_verb='GET',
            path_items=['.self']
        )
