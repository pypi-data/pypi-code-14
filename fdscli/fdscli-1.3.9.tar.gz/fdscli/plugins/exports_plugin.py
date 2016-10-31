# Copyright (c) 2016, Formation Data Systems, Inc. All Rights Reserved.
#
import collections
import json
from services import volume_service
from services import response_writer
from services.subscription.named_credential_client import NamedCredentialClient
from model.volume.remote_volume import RemoteVolume
from model.volume.volume import Volume
from utils.converters.volume.exported_volume_converter import ExportedVolumeConverter
from .abstract_plugin import AbstractPlugin
from utils.converters.volume.snapshot_policy_converter import SnapshotPolicyConverter
from model.fds_error import FdsError
from services.fds_auth import FdsAuth
from model.common.named_credential import NamedCredential
from model.common.s3credentials import S3Credentials
from model.common.repository import Repository
from utils.byte_converter import ByteConverter

class ExportsPlugin(AbstractPlugin):
    '''
    Provides management for exported (archive) volumes.

    Currently supports listing only.

    Attributes
    ----------
    :type _ExportsPlugin__volume_service: ``services.VolumeService``
    :attr _ExportsPlugin__volume_service: Low-level API for HTTP volumes API

    :type _ExportsPlugin__named_credential_client: ``services.subscription.NamedCredentialClient``
    :attr _ExportsPlugin__named_credential_client: Low-level API for HTTP named_credentials API

    :type _ExportsPlugin__parser: ``argparse.ArgumentParser``
    :type _ExportsPlugin__subparser: ``argparse._SubParsersAction``
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
        
        if not self.session.is_allowed( FdsAuth.VOL_MGMT ):
            return

        self.__volume_service = volume_service.VolumeService( self.session )
        self.__named_credential_client = NamedCredentialClient( self.session )

        msg = ("Exported (archive) volume management.")
        self.__parser = parentParser.add_parser("exports", description=msg, help=msg)
        self.__subparser = self.__parser.add_subparsers( help="Available sub-commands")

        # Other operations may eventually make sense for exports, like cleaning or deleting.
        self.add_command_list( self.__subparser )

    def detect_shortcut(self, args):
        '''
        @see: AbstractPlugin
        '''        
        return None
        
    def add_command_list(self, subparser):
        '''
        Creates the parser for the ``exports list`` command.

        Parameters
        ----------
        :type subparser: ``argparse._SubParsersAction``
        :param subparser: parsers action
        '''
        msg_for_list = ("List exported volumes in an existing bucket. Specify a named credential "
            "for bucket access, or specify the bucket access arguments individually.")
        __parserForList = subparser.add_parser( "list", description=msg_for_list, help=msg_for_list)

        # Optional args
        __parserForList.add_argument( "-" + AbstractPlugin.format_str, help=(
            "Specify the format that the result is printed as"), choices=["json","tabular"], required=False)
        __parserForList.add_argument("-c", "--credential", help=("A named credential ID or name. "
            "Manage named credentials using the \'credential\' command."))

        __parserForList.add_argument("BUCKET_NAME", nargs='?', help=("An already existing bucket. "
            "The BUCKET_NAME and bucket access arguments are not used if a named credential is specified."))

        groupForS3Access = __parserForList.add_argument_group('bucket access arguments')

        groupForS3Access.add_argument( "-" + AbstractPlugin.s3_access_key_str, help="S3 access key")
        groupForS3Access.add_argument( "-" + AbstractPlugin.s3_secret_key_str, help="S3 secret key")
        groupForS3Access.add_argument( "-" + AbstractPlugin.url_str, help=(
            "The URL where the bucket resides. For Formation, a value like "
            "\'https://us-east.formationds.com'. For AWS, a value like "
            "\'https://s3-us-west-2.amazonaws.com\'."))

        __parserForList.set_defaults( func=self.list_exports, format="tabular")

    def get_volume_service(self):
        return self.__volume_service           

    def get_named_credential_client(self):
        return self.__named_credential_client

    def list_exports(self, args):
        '''
        List all available exports in a given bucket.
        '''
        bucket_name = None
        if "BUCKET_NAME" in args and args["BUCKET_NAME"] is not None:
            bucket_name = args["BUCKET_NAME"]

        credential_key = None
        if "credential" in args and args["credential"] is not None:
            credential_key = args["credential"]

        repository = Repository()
        if credential_key is None:
            repository.bucket_name = bucket_name
            repository.credentials.access_key_id = args[AbstractPlugin.s3_access_key_str]
            repository.credentials.secret_key = args[AbstractPlugin.s3_secret_key_str]
            repository.url = args[AbstractPlugin.url_str]
        else:
            named_credential = self.get_named_credential_client().get_named_credential_by_key(credential_key)
            if isinstance(named_credential, NamedCredential):
                if named_credential.s3credentials is None:
                    print("Not an S3 named credential: \'{}\'.\n".format(credential_key))
                    return
                repository.credentials.access_key_id = named_credential.s3credentials.access_key_id
                repository.credentials.secret_key = named_credential.s3credentials.secret_key
                repository.bucket_name = named_credential.bucketname
                repository.url = named_credential.url
            else:
                print("No named credential found for \'{}\'.\n".format(credential_key))
                return

        if repository.bucket_name is None:
            print("BUCKET_NAME is required.\n")
            return

        response = self.get_volume_service().list_exports_in_bucket(repository)

        if isinstance(response, FdsError):
            return

        if isinstance(response, collections.Iterable):
            if (len(response) == 0):
                print("No exported volumes found for bucket \'{}\'.\n".format(repository.bucket_name))
                return

        #print it all out
        if "format" in args  and args[AbstractPlugin.format_str] == "json":

            j_exports = []

            for export in response:
                j_export = ExportedVolumeConverter.to_json(export)
                j_export = json.loads( j_export )
                j_exports.append( j_export )

            response_writer.ResponseWriter.writeJson( j_exports )
        else:
            resultList = response_writer.ResponseWriter.prep_exports_for_table( self.session, response)
            response_writer.ResponseWriter.writeTabularData( resultList )  
