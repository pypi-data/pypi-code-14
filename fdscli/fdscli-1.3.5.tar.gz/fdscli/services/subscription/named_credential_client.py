# Copyright (c) 2016, Formation Data Systems, Inc. All Rights Reserved.
#
import json
from services.abstract_service import AbstractService
from model.fds_error import FdsError
from model.common.named_credential import NamedCredential
from utils.converters.common.named_credential_converter import NamedCredentialConverter

class NamedCredentialClient(AbstractService):
    '''
    Formation Named Credential
    Formation Named Credential is a web service that enables a user to manage named credentials.
    A named credential encapsulates the endpoint for a SafeGuard data migration task along with
    the authentication parameters required to access the endpoint.

    Client
    This low-level API provides one-to-one mappings to the underlying HTTP API operations.
    '''

    def __init__(self, session):
        '''
        :type session: ``services.FdsAuth``
        :param session: Data about the active session
        '''
        AbstractService.__init__(self, session)

    def create_named_credential(self, named_credential):
        '''
        Adds a persistent named credential for the current user.

        Parameters
        ----------
        :type named_credential: ``model.common.NamedCredential`` object

        Returns
        -------
        :type ``model.FdsError`` or ``model.common.NamedCredential``)
        '''
        url = "{}{}".format(self.get_url_preamble(), "/named_credentials")
        data = NamedCredentialConverter.to_json(named_credential)
        response = self.rest_helper.post(self.session, url, data)

        if isinstance(response, FdsError):
            return response

        deserialized = NamedCredentialConverter.build_from_json(response)
        return deserialized        

    def get_named_credential(self, digest):
        '''
        Parameters
        ----------
        :type digest: string
        :param digest: Unique identifier for a named credential

        Returns
        -------
        :type ``model.FdsError`` or ``model.common.NamedCredential``
        '''
        if digest is None:
            return
        if len(digest) == 0:
            return

        response = self.get_named_credentials()

        if isinstance(response, FdsError):
            return response

        for named_credential in response:
            if (named_credential.digest == digest):
                return named_credential

        return

    def get_named_credentials(self):
        '''
        Returns
        -------
        :type ``model.FdsError`` or list(``model.common.NamedCredential``)
        '''
        url = "{}{}".format(self.get_url_preamble(), "/named_credentials")
        response = self.rest_helper.get(self.session, url)

        if isinstance(response, FdsError):
            return response

        named_credentials = []

        for j_str in response:
            named_credential = NamedCredentialConverter.build_from_json(j_str)
            named_credentials.append(named_credential)

        return named_credentials

    def delete_named_credential(self, digest):
        pass

    def update_named_credential(self, named_credential):
        '''
        Updates existing persistent named credential for the current user.

        Parameters
        ----------
        :type named_credential: ``model.common.NamedCredential`` object

        Returns
        -------
        :type ``model.FdsError`` or ``model.common.NamedCredential``)
        '''
        url = "{}{}{}".format(self.get_url_preamble(), "/named_credentials/",
            named_credential.digest)
        data = NamedCredentialConverter.to_json(named_credential)
        response = self.rest_helper.put(self.session, url, data)

        if isinstance(response, FdsError):
            return response

        deserialized = NamedCredentialConverter.build_from_json(response)
        return deserialized        

