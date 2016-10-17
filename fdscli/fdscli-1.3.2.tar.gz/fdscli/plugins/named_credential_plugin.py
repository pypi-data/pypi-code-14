# Copyright (c) 2016, Formation Data Systems, Inc. All Rights Reserved.
#

import collections
import json
import time
from services import response_writer
from services.subscription.named_credential_client import NamedCredentialClient
from utils.converters.common.named_credential_converter import NamedCredentialConverter
from .abstract_plugin import AbstractPlugin
from model.common.size import Size
from model.fds_error import FdsError
from services.fds_auth import FdsAuth
from model.common.named_credential import NamedCredential
from model.common.s3credentials import S3Credentials
from model.common.repository import Repository
from collections import OrderedDict

class NamedCredentialPlugin(AbstractPlugin):
    '''Provides named credential management.

    Creates command line parsers and uses Formation Named Credential service client to
    dispatch requests.

    Attributes
    ----------
    :type _NamedCredentialPlugin__credential_client: ``services.subscription.NamedCredentialClient``
    :attr _NamedCredentialPlugin__credential_client: Low-level API for HTTP named credential API

    :type _NamedCredentialPlugin__parser: ``argparse.ArgumentParser``

    :type _NamedCredentialPlugin__subparser: ``argparse._SubParsersAction``
    '''
    
    def __init__(self):
        AbstractPlugin.__init__(self)
    
    def build_parser(self, parentParser, session):
        '''
        @see: AbstractPlugin

        Parameters
        ----------
        parentParser (argparse.Action)
        session (services.FdsAuth)
        '''
        
        self.session = session
        
        self.__credential_client = NamedCredentialClient( self.session )
        
        self.__parser = parentParser.add_parser( "cred", help=("Named credential management. "
            "Stores credentials securely for use by SafeGuard recurring data migration tasks. "
            "A named credential specifies the URL of a data storage endpoint and the authentication "
            "arguments required to access the data."))
        self.__subparser = self.__parser.add_subparsers( help="Available sub-commands")

        # Add parsers for sub-commands
        self.add_command_delete(self.__subparser)
        self.add_command_get(self.__subparser)
        self.add_command_list(self.__subparser)
        self.add_command_save(self.__subparser)

    def add_command_delete(self, subparser):
        '''
        Creates the parser for the 'cred delete' sub-command.

        Parameters
        ----------
        :type subparser: ``argparse._SubParsersAction``
        :param subparser: parsers action
        '''
        __parserForDelete = subparser.add_parser("delete", help=("Delete a named credential "
            "for the current user."))

        # Optional args
        __parserForDelete.add_argument(self.arg_str + AbstractPlugin.name_str, help=("The user "
            "defined credential name."), required=False)
        __parserForDelete.add_argument(self.arg_str + AbstractPlugin.id_str, help=("The unique "
            "identifier for the named credential."), required=False)

        __parserForDelete.set_defaults(func=self.delete_named_credential, format="tabular")

    def add_command_get(self, subparser):
        '''
        Creates the parser for the 'cred get' sub-command.

        Parameters
        ----------
        :type subparser: ``argparse._SubParsersAction``
        :param subparser: parsers action
        '''
        __parserForGet = subparser.add_parser("get", help=("Get a (previously saved) named "
            "credential for the current user."))

        # Optional args
        __parserForGet.add_argument(self.arg_str + AbstractPlugin.name_str, help=("The user "
            "defined credential name."), required=False)
        __parserForGet.add_argument(self.arg_str + AbstractPlugin.id_str, help=("The unique "
            "identifier for the named credential."), required=False)

        __parserForGet.set_defaults(func=self.get_named_credential, format="tabular")

    def add_command_list(self, subparser ):
        '''
        Creates the parser for the 'cred list' sub-command.

        Parameters
        ----------
        :type subparser: ``argparse._SubParsersAction``
        :param subparser: parsers action
        '''
        __parserForList = subparser.add_parser( "list", help="List all named credentials for the current user.")

        # Optional args
        __parserForList.add_argument(self.arg_str + AbstractPlugin.format_str, help=("Specify the "
            "format that the result is printed as"), choices=["json","tabular"], required=False )
        
        __parserForList.set_defaults( func=self.list_named_credentials, format="tabular" )

    def add_command_save(self, subparser):
        '''
        Creates the parser for the 'cred save' sub-command.

        Parameters
        ----------
        :type subparser: ``argparse._SubParsersAction``
        :param subparser: parsers action
        '''
        __parserForSave = subparser.add_parser("save", help=("Create a named credential "
            "for the current user."))

        parserForSaveSubParser = __parserForSave.add_subparsers(help="Available sub-commands.")

        # 'cred save s3' sub-command
        __parserForSaveS3 = parserForSaveSubParser.add_parser("s3", help=("Save S3 named "
            "credential. Used for data migration to an existing S3 bucket."))

        # Required arguments
        groupForSaveS3 = __parserForSaveS3.add_argument_group('required arguments')
        groupForSaveS3.add_argument(self.arg_str + AbstractPlugin.name_str, help=("The credential "
            "name. Must be unique for the user. Spaces are invalid in the name."),
            default=None, required=True)
        groupForSaveS3.add_argument(self.arg_str + AbstractPlugin.url_str, help=("S3 endpoint "
            "like \'https://s3-us-west2.amazonaws.com\'."), required=True)
        groupForSaveS3.add_argument(self.arg_str + AbstractPlugin.s3_bucket_name_str,
            help=("For a S3 endpoint, specifies the bucket name. The bucket must exist prior to "
            "data access."), required=True)
        groupForSaveS3.add_argument(self.arg_str + AbstractPlugin.s3_access_key_str,
            help=("For a S3 endpoint, specifies the AWS Credentials access key."), required=True)
        groupForSaveS3.add_argument(self.arg_str + AbstractPlugin.s3_secret_key_str,
            help=("For a S3 endpoint, specifies the AWS Credentials secret key."), required=True)

        __parserForSaveS3.set_defaults(func=self.save_named_credential_s3, format="tabular")

        # 'cred save f1' sub-command
        __parserForSaveF1 = parserForSaveSubParser.add_parser("f1", help=("Save FormationOne "
            "named credential. Used for data migration to a remote OM node."))

        # Required arguments
        groupForSaveF1 = __parserForSaveF1.add_argument_group('required arguments')
        groupForSaveF1.add_argument(self.arg_str + AbstractPlugin.name_str, help=("The credential "
            "name. Must be unique for the user. Spaces are invalid in the name."),
            default=None, required=True)
        groupForSaveF1.add_argument(self.arg_str + AbstractPlugin.protocol_str,
            help=("For a FormationOne endpoint, the protocol. Recommended value is \'https\'."),
            default=None, required=True)
        groupForSaveF1.add_argument(self.arg_str + AbstractPlugin.username_str,
            help=("Name of a FormationOne user for the remote OM."),
            default=None, required=True)
        groupForSaveF1.add_argument(self.arg_str + AbstractPlugin.password_str,
            help=("Password for the FormationOne user on the remote OM."),
            default=None, required=True)
        groupForSaveF1.add_argument(self.arg_str + AbstractPlugin.hostname_str,
            help=("Hostname for the remote OM."),
            default=None, required=True)
        groupForSaveF1.add_argument(self.arg_str + AbstractPlugin.port_str,
            help=("Port number for the remote OM."),
            default=None, required=True)

        __parserForSaveF1.set_defaults(func=self.save_named_credential_f1, format="tabular")

    def get_named_credential_client(self):
        return self.__credential_client

    def delete_named_credential(self, args):
        '''
        Parameters
        ----------
        :type args: dict
        '''
        digest = None
        name = None
        if AbstractPlugin.id_str in args and args[AbstractPlugin.id_str] is not None:
            digest = args[AbstractPlugin.id_str]
        elif AbstractPlugin.name_str in args and args[AbstractPlugin.name_str] is not None:
            name = args[AbstractPlugin.name_str]

        if digest is None and name is None:
            print("Missing identifier or name")
            return

        response = None
        if digest is not None:
            response = self.get_named_credential_client().delete_named_credential(digest)
        elif name is not None:
            pass

        if isinstance(response, FdsError):
            return 1

        print("Named credential \'{}\' deleted.".format(digest))
        return

    def get_named_credential(self, args):
        '''
        Parameters
        ----------
        :type args: dict
        '''
        response = self.get_named_credential_client().get_named_credentials()

        if isinstance(response, FdsError):
            return 1

        digest = None
        name = None
        if AbstractPlugin.id_str in args and args[AbstractPlugin.id_str] is not None:
            digest = args[AbstractPlugin.id_str]
        elif AbstractPlugin.name_str in args and args[AbstractPlugin.name_str] is not None:
            name = args[AbstractPlugin.name_str]

        for named_credential in response:
            if digest != None and named_credential.digest == digest:
                return named_credential
            if name != None and named_credential.name == name:
                return named_credential
        return

    def get_named_credential_by_name(self, name):
        '''
        Parameters
        ----------
        :type name: string
        :param name: The name of the named credential, which is unique per user

        Returns
        -------
        :type ``model.common.NamedCredential``
        '''
        if name is None:
            return 1
        if len(name) == 0:
            return 1

        response = self.get_named_credential_client().get_named_credentials()

        if isinstance(response, FdsError):
            return 1

        for named_credential in response:
            if named_credential.name == name:
                return named_credential

        return

    def list_named_credentials(self, args):
        '''
        Parameters
        ----------
        :type args: dict
        '''
        response = self.get_named_credential_client().get_named_credentials()

        if isinstance(response, FdsError):
            return 1

        if (len(response) == 0):
            print("No named credentials for this user.")
            return

        if "format" in args and args[AbstractPlugin.format_str] == "json":

            j_named_credentials = []

            for named_credential in response:
                j_named_cred = NamedCredentialConverter.to_json(named_credential)
                j_named_cred = json.loads(j_named_cred)
                j_named_credentials.append(j_named_cred)

            response_writer.ResponseWriter.writeJson(j_named_credentials)
        else:
            resultList = response_writer.ResponseWriter.prep_named_credentials_for_table(self.session, response)
            response_writer.ResponseWriter.writeTabularData(resultList)

    def save_named_credential_f1(self, args):
        '''
        Parameters
        ----------
        :type args: dict
        '''
        credential = NamedCredential()

        # Required args
        credential.protocol = args[AbstractPlugin.protocol_str]
        credential.username = args[AbstractPlugin.username_str]
        credential.password = args[AbstractPlugin.password_str]
        credential.hostname = args[AbstractPlugin.hostname_str]
        credential.port = args[AbstractPlugin.port_str]

        credential.name = args[AbstractPlugin.name_str]
        credential.user_id = self.session.get_user_id()

        credential.url = credential.protocol;
        if credential.url.find("://") == -1:
            if credential.url.find(":/") == -1:
                credential.url += "://"
            else:
                credential.url += "/"

        credential.url += credential.username
        credential.url += ":"
        credential.url += credential.password
        credential.url += "@"
        credential.url += credential.hostname
        credential.url += ":"
        credential.url += str(credential.port)

        # Check for existence
        existing = self.get_named_credential_by_name(credential.name)
        if (isinstance(existing, NamedCredential)):
            credential.digest = existing.digest
            response = self.get_named_credential_client().update_named_credential(credential)
        else:
            response = self.get_named_credential_client().create_named_credential(credential)

        if (isinstance(response, NamedCredential)):
            # TODO: format
            pass
        else:
            return 1
        return

    def save_named_credential_s3(self, args):
        '''
        Parameters
        ----------
        :type args: dict
        '''
        credential = NamedCredential()

        # Required args
        credential.url = args[AbstractPlugin.url_str]
        credential.name = args[AbstractPlugin.name_str]
        credential.user_id = self.session.get_user_id()
        credential.bucketname = args[AbstractPlugin.s3_bucket_name_str]
        s3credentials = S3Credentials()
        s3credentials.access_key_id = args[AbstractPlugin.s3_access_key_str]
        s3credentials.secret_key = args[AbstractPlugin.s3_secret_key_str]
        credential.s3credentials = s3credentials

        # Check for existence
        existing = self.get_named_credential_by_name(credential.name)
        if (isinstance(existing, NamedCredential)):
            credential.digest = existing.digest
            response = self.get_named_credential_client().update_named_credential(credential)
        else:
            response = self.get_named_credential_client().create_named_credential(credential)

        if (isinstance(response, NamedCredential)):
            # TODO: format
            pass
        else:
            return 1
        return
