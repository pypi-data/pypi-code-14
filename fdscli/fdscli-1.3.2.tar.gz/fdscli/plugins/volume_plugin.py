# Copyright (c) 2015, Formation Data Systems, Inc. All Rights Reserved.
#

import collections
import getpass
import math
import json
import time
from services import volume_service
from services import response_writer
from services.subscription.named_credential_client import NamedCredentialClient
from services.subscription.subscription_client import SubscriptionClient
from model.volume.remote_volume import RemoteVolume
from model.volume.volume import Volume
from model.volume.snapshot import Snapshot
from utils.converters.volume.exported_volume_converter import ExportedVolumeConverter
from utils.converters.volume.subscription_converter import SubscriptionConverter
from utils.converters.volume.volume_converter import VolumeConverter
from .abstract_plugin import AbstractPlugin
from utils.volume_validator import VolumeValidator
from utils.converters.volume.snapshot_converter import SnapshotConverter
from services.snapshot_policy_service import SnapshotPolicyService
from utils.converters.volume.snapshot_policy_converter import SnapshotPolicyConverter
from model.volume.settings.block_settings import BlockSettings
from model.common.size import Size
from model.volume.settings.object_settings import ObjectSettings
from model.fds_error import FdsError
from services.fds_auth import FdsAuth
from model.volume.settings.iscsi_settings import ISCSISettings
from model.common.credential import Credential
from model.common.named_credential import NamedCredential
from model.common.s3credentials import S3Credentials
from model.common.repository import Repository
from model.volume.settings.lun_permission import LunPermissions
from model.volume.settings.nfs_settings import NfsSettings
from collections import OrderedDict
from utils.byte_converter import ByteConverter

class VolumePlugin(AbstractPlugin):
    '''
    Created on Apr 3, 2015
    
    This plugin will handle all call that deal with volumes.  Create, list, edit, attach snapshot policy etc.
    
    In order to run, it utilizes the volume service class and acts as a parsing pass through to acheive
    the various tasks
    
    @author: nate

    Attributes
    ----------
    :type _VolumePlugin__volume_service: ``services.VolumeService``
    :attr _VolumePlugin__volume_service: Low-level API for HTTP volumes API

    :type _VolumePlugin__named_credential_client: ``services.subscription.NamedCredentialClient``
    :attr _VolumePlugin__named_credential_client: Low-level API for HTTP named_credentials API

    :type _VolumePlugin__subscription_client: ``services.subscription.SubscriptionClient``
    :attr _VolumePlugin__subscription_client: Low-level API for HTTP subscriptions API

    :type _VolumePlugin__parser: ``argparse.ArgumentParser``

    :type _VolumePlugin__subparser: ``argparse._SubParsersAction``
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
        self.__subscription_client = SubscriptionClient( self.session )
        self.__named_credential_client = NamedCredentialClient( self.session )

        self.__parser = parentParser.add_parser( "volume", help="All volume management operations" )
        self.__subparser = self.__parser.add_subparsers( help="The sub-commands that are available")

        self.create_list_command( self.__subparser )
        self.create_list_snapshot_policies_command( self.__subparser )
        self.create_create_command( self.__subparser )
        self.create_delete_command( self.__subparser )
        self.create_list_snapshots_command(self.__subparser)
        self.create_edit_command( self.__subparser )
        self.create_snapshot_command( self.__subparser )
        self.create_clone_command( self.__subparser )
        self.create_list_exports_command( self.__subparser )
        self.create_export_command( self.__subparser )
        self.create_import_command( self.__subparser )
        self.create_safeguard_command( self.__subparser )
        self.create_check_command( self.__subparser )
        self.create_fix_command( self.__subparser )

    def detect_shortcut(self, args):
        '''
        @see: AbstractPlugin
        '''        

        # is it the listVolumes shortcut
        if ( args[0].endswith( "listVolumes" ) ):
            args.pop(0)
            args.insert( 0, "volume" )
            args.insert( 1, "list" )
            return args
        
        return None
        
    #parser creation        
    def create_list_command(self, subparser ):
        '''
        Configure the parser for the volume list command
        '''           
        __listParser = subparser.add_parser( "list", help="List all the volumes in the system" )
        __listParser.add_argument( "-" + AbstractPlugin.format_str, help="Specify the format that the result is printed as", choices=["json","tabular"], required=False )
        
#         indGroup = __listParser.add_argument_group( "Individual volume queries", "Indicate how to identify the volume that you are looking for." )
#         __listParserGroup = indGroup.add_mutually_exclusive_group()
        __listParser.add_argument( "-" + AbstractPlugin.volume_id_str, help="Specify a particular volume to list by UUID", default=None )
#         __listParserGroup.add_argument( "-" + AbstractPlugin.volume_name_str, help="Specify a particular volume to list by name" )
        __listParser.set_defaults( func=self.list_volumes, format="tabular" )
        

    def create_list_snapshot_policies_command(self, subparser):
        '''
        List all of the snapshot policies for a specified volume
        '''
        
        __listSp_parser = subparser.add_parser( "list_snapshot_policies", help="List the snapshot policies for a specific volume.")
        self.add_format_arg(__listSp_parser)
        __listSp_parser.add_argument( self.arg_str + AbstractPlugin.volume_id_str, help="The ID of the volume you'd like to list the policies for.", required=True)
        
        __listSp_parser.set_defaults( func=self.list_snapshot_policies, format="tabular")

    def create_create_command(self, subparser):
        """
        Create the parser for the volume creation command
        """
        # Exponent math is easier than straight math here.
        # 2^32 is the addressable size, 2^17 is the smallest block size, 2^30 is 1 GiB.  
        # so multiple the size and small block size to get the bytes we can handle, subract 30 to convert to GiB
        vol_size_in_gb = int(math.pow( 2, (32 + 17) - 30))
        __createParser = subparser.add_parser("create", help="All volume create management operations")
        volumeTypeParser = __createParser.add_subparsers(help="The sub-commands that are available")
                 
        __createObjectParser = volumeTypeParser.add_parser("object", help="Create a new object volume")
        __createNfsParser = volumeTypeParser.add_parser("nfs", help="Create a new NFS volume" )
        __createIscsiParser = volumeTypeParser.add_parser("iscsi", help="Create a new iscsi volume" )
        __createBlockParser = volumeTypeParser.add_parser("block", help="Create a new block volume" )

        __createObjectParser = self.add_common_defaults(__createObjectParser)
        __createNfsParser = self.add_common_defaults(__createNfsParser)
        __createIscsiParser = self.add_common_defaults(__createIscsiParser)
        __createBlockParser = self.add_common_defaults(__createBlockParser)

        # Object volume options
        __createObjectParser.add_argument( self.arg_str + AbstractPlugin.max_obj_size_str, help="The internal maximum size for one blob.  This is only applicable to OBJECT volumes and must be within 4KB and 8MB.  If it is not, the system default will be applied.", type=int, default=None)
        __createObjectParser.add_argument( self.arg_str + AbstractPlugin.max_obj_size_unit_str, help="The units that you with the max object size to be in.  The default is MB.", choices=["B", "KB", "MB", "GB", "TB"], default="MB")

        # iSCSI volume options
        __createIscsiParser.add_argument( self.arg_str + AbstractPlugin.block_size_str, help="The block size you would like to use for block type volumes.  This value must be between 4KB and 8MB.  If it is not, the system default will be applied.", type=int, default=None)
        __createIscsiParser.add_argument( self.arg_str + AbstractPlugin.block_size_unit_str, help="The units that you wish the block size to be in.  The default is KB.", choices=["KB","MB"], default="KB")

        __createIscsiParser.add_argument(self.arg_str + AbstractPlugin.incoming_creds_str,
                                         help="Credentials for users allowed to use this volume.  You can provide this in the format <username>:<password>, or supply just the username and you will be prompted for the passwords.",
                                         nargs="+", default=None, metavar="")
        __createIscsiParser.add_argument(self.arg_str + AbstractPlugin.outgoing_creds_str,
                                         help="Credentials for this volume to use for outgoing authentication.  You can provide this in the format <username>:<password>, or supply just the username and you will be prompted for the passwords.",
                                         nargs="+", default=None, metavar="")
        __createIscsiParser.add_argument(self.arg_str + AbstractPlugin.lun_permissions_str,
                                         help="Set the LUN permissions in the form of <LUN name>:[rw|ro].", nargs="+",
                                         default=None, metavar="")
        __createIscsiParser.add_argument(self.arg_str + AbstractPlugin.initiators_str, help="Set a list of initiators.",
                                         nargs="+", default=None, metavar="")
        __createIscsiParser.add_argument(self.arg_str + AbstractPlugin.size_str,
                                       help="How large you would like the volume to appear as a numerical value.  "
                                            "It will assume the value is in GB unless you specify the size_units.  "
                                            "NOTE: This is only applicable to iSCSI and NFS volumes and is set to " +
                                            str(vol_size_in_gb) + " GB if not specified.",
                                       type=VolumeValidator.size, default=vol_size_in_gb, metavar="")
        __createIscsiParser.add_argument( self.arg_str + AbstractPlugin.size_unit_str, help="The units that should be applied to the size parameter.  The default is GB if not specified.", choices=["MB","GB","TB", "PB"], default="GB")

        # NFS Volume options
        __createNfsParser.add_argument( self.arg_str + AbstractPlugin.max_obj_size_str, help="The internal maximum size for one blob.  This is only applicable to OBJECT volumes and must be within 4KB and 8MB.  If it is not, the system default will be applied.", type=int, default=None)
        __createNfsParser.add_argument( self.arg_str + AbstractPlugin.max_obj_size_unit_str, help="The units that you with the max object size to be in.  The default is MB.", choices=["B", "KB", "MB", "GB", "TB"], default="MB")

        __createNfsParser.add_argument(self.arg_str + AbstractPlugin.use_acls_str,
                                       help="Whether or not ACLs should be used with this volume.",
                                       choices=["true", "false"], default="false", metavar="")
        __createNfsParser.add_argument(self.arg_str + AbstractPlugin.use_root_squash_str,
                                       help="Whether or not root squash is to be used with this volume.",
                                       choices=["true", "false"], default="false", metavar="")
        __createNfsParser.add_argument(self.arg_str + AbstractPlugin.synchronous_str,
                                       help="Whether or not this volume is to be used synchronously.",
                                       choices=["true", "false"], default="false", metavar="")
        __createNfsParser.add_argument(self.arg_str + AbstractPlugin.clients,
                                       help="An IP filter that defines which clients can access this share.",
                                       default="*", metavar="")
        __createNfsParser.add_argument( self.arg_str + AbstractPlugin.size_str,
                                        help="How large you would like the volume to appear as a numerical value."
                                             "It will assume the value is in GB unless you specify the size_units.  "
                                          "NOTE: This is only applicable to iSCSI and NFS volumes and is set to " +
                                          str(vol_size_in_gb) + " GB if not specified.",
                                        type=VolumeValidator.size, default=vol_size_in_gb, metavar="" )
        __createNfsParser.add_argument( self.arg_str + AbstractPlugin.size_unit_str, help="The units that should be applied to the size parameter.  The default is GB if not specified.", choices=["MB","GB","TB", "PB"], default="GB")
        # block volume options
        __createBlockParser.add_argument( self.arg_str + AbstractPlugin.block_size_str,
                                          help="The block size you would like to use for block type volumes.  "
                                               "This value must be between 4KB and 8MB.  If it is not, the system "
                                               "default will be applied.", type=int, default=None)
        __createBlockParser.add_argument( self.arg_str + AbstractPlugin.block_size_unit_str,
                                          help="The units that you wish the block size to be in.  "
                                               "The default is KB.", choices=["KB","MB"], default="KB")
        __createBlockParser.add_argument(self.arg_str + AbstractPlugin.size_str,
                                       help="How large you would like the volume to appear as a numerical value."
                                            "It will assume the value is in GB unless you specify the size_units.  "
                                            "NOTE: This is only applicable to iSCSI and NFS volumes and is set to " +
                                            str(vol_size_in_gb) + " GB if not specified.",
                                       type=VolumeValidator.size, default=vol_size_in_gb, metavar="")
        __createBlockParser.add_argument(self.arg_str + AbstractPlugin.size_unit_str,
                                   help="The units that should be applied to the size parameter. The default is GB if not specified.",
                                   choices=["MB", "GB", "TB", "PB"], default="GB")

        __createIscsiParser.set_defaults(func=self.create_iscsi_volume, format="tabular")
        __createNfsParser.set_defaults(func=self.create_nfs_volume, format="tabular")
        __createObjectParser.set_defaults(func=self.create_object_volume, format="tabular")
        __createBlockParser.set_defaults(func=self.create_block_volume, format="tabular")

    def add_common_defaults(self, __createParser):
        __createParser.add_argument( self.arg_str + AbstractPlugin.format_str, help="Specify the format that the result is printed as", choices=["json","tabular"], required=False )
        __createParser.add_argument( self.arg_str + AbstractPlugin.data_str, help="JSON string representing the volume parameters desired for the new volume.  This argument will take precedence over all individual arguments.", default=None)
        __createParser.add_argument( self.arg_str + AbstractPlugin.name_str, help="The name of the volume", default=None )
        __createParser.add_argument( self.arg_str + AbstractPlugin.qos_preset_str, help=("The ID of the quality of service preset you would like applied. Takes precedence over individually set items. See \'presets list\' command for ID values."), default=None)
        __createParser.add_argument( self.arg_str + AbstractPlugin.timeline_preset_str, help=("The ID of the data protection preset you would like applied. This will cause snapshot policies to be created and attached to this volume. See \'presets list\' command for ID values."), default=None)
        __createParser.add_argument( self.arg_str + AbstractPlugin.iops_limit_str, help="The IOPs limit for the volume.  0 = unlimited and is the default if not specified.", type=VolumeValidator.iops_limit, default=0, metavar="" )
        __createParser.add_argument( self.arg_str + AbstractPlugin.iops_guarantee_str, help="The IOPs guarantee for this volume.  0 = no guarantee and is the default if not specified.", type=VolumeValidator.iops_guarantee, default=0, metavar="" )
        __createParser.add_argument( self.arg_str + AbstractPlugin.priority_str, help="A value that indicates how to prioritize performance for this volume.  1 = highest priority, 10 = lowest.  Default value is 7.", type=VolumeValidator.priority, default=7, metavar="")
        __createParser.add_argument( self.arg_str + AbstractPlugin.media_policy_str, help="The policy that will determine where the data will live over time.", choices=["HYBRID", "SSD", "HDD"], default="HYBRID")
        __createParser.add_argument( self.arg_str + AbstractPlugin.continuous_protection_str, help="A value (in seconds) for how long you want continuous rollback for this volume.  The default is 24 hours (86400 seconds) so if you do NOT want this please provide a value.  Valid values are from 0 to 1209600 (1 year)", type=VolumeValidator.continuous_protection, default=86400, metavar="" )
        return __createParser

    def create_edit_command(self, subparser):
        '''
        Create the parser for the edit command
        '''
        
        __editParser = subparser.add_parser( "edit", help="Edit the quality of service settings on your volume")
        __editParser.add_argument( self.arg_str + AbstractPlugin.format_str, help="Specify the format that the result is printed as", choices=["json","tabular"], required=False )
        __editGroup = __editParser.add_mutually_exclusive_group( required=True )
        __editGroup.add_argument( self.arg_str + AbstractPlugin.data_str, help="A JSON string representing the volume and parameters to change.  This argument will take precedence over all individual arguments.", default=None)
        __editGroup.add_argument( self.arg_str + AbstractPlugin.volume_id_str, help="The UUID of the volume you would like to edit.", default=None)
        __editParser.add_argument( self.arg_str + AbstractPlugin.qos_preset_str, help=(
            "The ID of the quality of service preset you would like applied. Takes precedence over "
            "individually set items. See \'presets list\' command for ID values."), default=None)
        __editParser.add_argument( self.arg_str + AbstractPlugin.timeline_preset_str, help=(
            "The ID of the timeline preset you would like applied .This will cause snapshot policies "
            "to be created and attached to this volume. See \'presets list\' command for ID values."), default=None)
        __editParser.add_argument( self.arg_str + AbstractPlugin.iops_limit_str, help="The IOPs limit for the volume.  0 = unlimited.", type=VolumeValidator.iops_limit, default=None, metavar="" )
        __editParser.add_argument( self.arg_str + AbstractPlugin.iops_guarantee_str, help="The IOPs guarantee for this volume.  0 = no guarantee.", type=VolumeValidator.iops_guarantee, default=None, metavar="" )
        __editParser.add_argument( self.arg_str + AbstractPlugin.priority_str, help="A value that indicates how to prioritize performance for this volume.  1 = highest priority, 10 = lowest.", type=VolumeValidator.priority, default=None, metavar="")
#         __editParser.add_argument( "-media_policy", help="The policy that will determine where the data will live over time.", choices=["HYBRID_ONLY", "SSD_ONLY", "HDD_ONLY"], default=None)
        __editParser.add_argument( self.arg_str + AbstractPlugin.continuous_protection_str, help="A value (in seconds) for how long you want continuous rollback for this volume.  Valid values are from 0 to 1209600 (1 year)", type=VolumeValidator.continuous_protection, default=None, metavar="" )
        
        '''
        iSCSI arguments
        '''    
        __editParser.add_argument( self.arg_str + AbstractPlugin.incoming_creds_str, help="Credentials for users allowed to use this volume.  You can provide this in the format <username>:<password>, or supply just the username and you will be prompted for the passwords.", nargs="+", default=None, metavar="")
        __editParser.add_argument( self.arg_str + AbstractPlugin.outgoing_creds_str, help="Credentials for this volume to use for outgoing authentication.  You can provide this in the format <username>:<password>, or supply just the username and you will be prompted for the passwords.", nargs="+", default=None, metavar="")
        __editParser.add_argument( self.arg_str + AbstractPlugin.lun_permissions_str, help="Set the LUN permissions in the form of <LUN name>:[rw|ro].", nargs="+", default=None, metavar="" )
        __editParser.add_argument( self.arg_str + AbstractPlugin.initiators_str, help="Set a list of initiators.", nargs="+", default=None, metavar="")
        
        '''
        NFS options
        '''
        __editParser.add_argument( self.arg_str + AbstractPlugin.use_acls_str, help="Whether or not ACLs should be used with this volume.", choices=["true", "false"], default="false", metavar="")
        __editParser.add_argument( self.arg_str + AbstractPlugin.use_root_squash_str, help="Whether or not root squash is to be used with this volume.", choices=["true", "false"], default="false", metavar="")
        __editParser.add_argument( self.arg_str + AbstractPlugin.synchronous_str, help="Whether or not this volume is to be used synchronously.", choices=["true", "false"], default="false", metavar="")
        __editParser.add_argument( self.arg_str + AbstractPlugin.clients, help="An IP filter that defines which clients can access this share.", default="*", metavar="")
            
        
        __editParser.set_defaults( func=self.edit_volume, format="tabular")
        
    def create_clone_command(self, subparser):
        '''
        Create the parser for the clone command

        Parameters
        ----------
        subparser (argparse._SubParsersAction) : parsers action
        '''
        __cloneParser = subparser.add_parser( "clone", help=("Create a clone of a volume from "
            "the current volume or a snapshot from the past. The clone can be created in the "
            "local domain or a remote domain."))

        # Optional arguments
        __cloneParser.add_argument( "-" + AbstractPlugin.format_str, help="Specify the format that the result is printed as", choices=["json","tabular"], required=False )
        __cloneParser.add_argument(self.arg_str + AbstractPlugin.media_policy_str, help="The policy that will determine where the data will live over time.", choices=["HYBRID", "SSD", "HDD"], default=None)

        __fromGroup = __cloneParser.add_mutually_exclusive_group( required=False )
        __fromGroup.add_argument( "-" + AbstractPlugin.time_str, help="The time (in seconds from the epoch) that you wish the clone to be made from.  The system will select the snapshot of the volume chosen which is nearest to this value.  If not specified, the default is to use the current time.", default=0, type=int)
        __fromGroup.add_argument( "-" + AbstractPlugin.snapshot_id_str, help="The UUID of the snapshot you would like to create the clone from.")

        __cloneParser.add_argument( self.arg_str + AbstractPlugin.qos_preset_str, help=(
            "The ID of the quality of service preset you would like to use. This will take "
            "precedence over any other QoS settings. See \'presets list\' command for ID values."), default=None)
        __cloneParser.add_argument( self.arg_str + AbstractPlugin.timeline_preset_str, help=(
            "The ID of the data protection preset that you would like to be applied. This will create "
            "and attach snapshot policies to the created volume. See \'presets list\' command for "
            "ID values."), default=None)
        __cloneParser.add_argument( "-" + AbstractPlugin.iops_limit_str, help="The IOPs maximum for the volume.  If not specified, the default will be the same as the parent volume.  0 = unlimited.", type=VolumeValidator.iops_limit, default=None, metavar="" )
        __cloneParser.add_argument( "-" + AbstractPlugin.iops_guarantee_str, help="The IOPs minimum for this volume.  If not specified, the default will be the same as the parent volume.  0 = no guarantee.", type=VolumeValidator.iops_guarantee, default=None, metavar="" )
        __cloneParser.add_argument( "-" + AbstractPlugin.priority_str, help="A value that indicates how to prioritize performance for this volume.  If not specified, the default will be the same as the parent volume.  1 = highest priority, 10 = lowest.", type=VolumeValidator.priority, default=None, metavar="")
        __cloneParser.add_argument( "-" + AbstractPlugin.continuous_protection_str, help="A value (in seconds) for how long you want continuous rollback for this volume.  If not specified, the default will be the same as the parent volume.  All values less than 24 hours will be set to 24 hours.", type=VolumeValidator.continuous_protection, default=None, metavar="" )
        __cloneParser.add_argument( "-" + AbstractPlugin.data_str, help="A JSON string containing the IOPs minimum, IOPs maximum, priority and continuous protection settings.", default=None )

        # SafeGuard arguments
        safeguard_group = __cloneParser.add_argument_group("SafeGuard arguments")
        safeguard_group.add_argument( self.arg_str + AbstractPlugin.remote_om_str, help=(
            "A string like \'https://remoteOmUser:remoteOmPasswd@remoteOmHost:remoteOmPort\'. "
            "Creates the clone in the domain given by this OM service locator. Use of secure http "
            "is recommended."), default=None)
        safeguard_group.add_argument( "-" + AbstractPlugin.incremental_str, help="If volume has "
            "been previously cloned to the remote domain, directs the system to continue exporting "
            "from the previous point. Errors if no previous full migration has completed.", default=False,
            action='store_true', required=False)
        safeguard_group.add_argument("-" + AbstractPlugin.safeguard_preset_str, help=("ID for a SafeGuard preset. "
            "Creates a recurring remote clone subscription. See \'presets list\' command for ID values."), default=None, required=False)

        # Required arguments
        group = __cloneParser.add_argument_group("required arguments")
        group.add_argument( "-" + AbstractPlugin.name_str, help="The name of the resulting new volume.", required=True )
        group.add_argument( "-" + AbstractPlugin.volume_id_str, help="The UUID of the volume from which the clone will be made.", required=True)

        __cloneParser.set_defaults( func=self.clone_volume, format="tabular" )

    def create_delete_command(self, subparser):
        '''
        create a parser for the delete command
        '''
        
        __deleteParser = subparser.add_parser( "delete", help="Delete a specified volume." )
        __deleteParser.add_argument( "-" + AbstractPlugin.format_str, help="Specify the format that the result is printed as", choices=["json","tabular"], required=False )
        __deleteGroup = __deleteParser.add_mutually_exclusive_group( required=True)
        __deleteGroup.add_argument( "-" + AbstractPlugin.volume_id_str, help="The UUID of the volume to delete.")
        __deleteGroup.add_argument( "-" + AbstractPlugin.volume_name_str, help="The name of the volume to delete.  If the name is not unique, this call will fail.")
        
        __deleteParser.set_defaults( func=self.delete_volume, format="tabular")

    def create_list_exports_command(self, subparser):
        '''
        Create the parser for the list_exports command

        TODO: other operations may eventually make sense for exports, like cleaning them.
        Consider adding a new subparser for exports, and support this functionality using exports list.

        Parameters
        ----------
        subparser : parsers action
        '''
        __listExportsParser = subparser.add_parser( "list_exports", help=("List exported volumes "
            "contained by an existing bucket."))

        group = __listExportsParser.add_argument_group('required arguments')

        group.add_argument( "-" + AbstractPlugin.s3_bucket_name_str, help="An already existing bucket", required=True)
        group.add_argument( "-" + AbstractPlugin.s3_access_key_str, help="S3 access key", required=True)
        group.add_argument( "-" + AbstractPlugin.s3_secret_key_str, help="S3 secret key", required=True)
        group.add_argument( "-" + AbstractPlugin.url_str, help=(
            "The URL where the bucket resides. For Formation, a value like "
            "\'https://us-east.formationds.com'. For AWS, a value like "
            "\'https://s3-us-west-2.amazonaws.com\'."), required=True)

        __listExportsParser.set_defaults( func=self.list_exports, format="tabular")

    def create_export_command(self, subparser):
        '''
        Create the parser for the export command

        Parameters
        ----------
        subparser (argparse._SubParsersAction) : parsers action
        '''
        __exportParser = subparser.add_parser( "export", help="Export a volume to an existing bucket.")

        # Optional args
        __exportParser.add_argument( "-" + AbstractPlugin.incremental_str, help="If volume has "
            "been previously exported to the existing bucket, directs the system to continue exporting "
            "from the previous point. Errors if no previous full export has completed.", default=False,
            action='store_true', required=False)
        __exportParser.add_argument("-" + AbstractPlugin.safeguard_preset_str, help=("ID for a SafeGuard preset. "
            "Creates a recurring export. See \'presets list\' command for ID values."), default=None, required=False)

        # Required arguments
        group = __exportParser.add_argument_group('required arguments')

        group.add_argument( "-" + AbstractPlugin.volume_id_str, help=("The UUID of the volume from which "
            "the export will be made."), required=True, type=long)
        group.add_argument( "-" + AbstractPlugin.s3_bucket_name_str, help=(
            "An already existing bucket"), required=True)
        group.add_argument( "-" + AbstractPlugin.s3_access_key_str, help="S3 access key", required=True)
        group.add_argument( "-" + AbstractPlugin.s3_secret_key_str, help="S3 secret key", required=True)
        group.add_argument( "-" + AbstractPlugin.url_str, help=(
            "The URL where the bucket resides. For Formation, a value like "
            "\'https://us-east.formationds.com'. For AWS, a value like "
            "\'https://s3-us-west-2.amazonaws.com\'."), required=True)

        __exportParser.set_defaults( func=self.export_volume, format="tabular")

    def create_import_command(self, subparser):
        '''
        Create the parser for the import command

        Parameters
        ----------
        subparser : parsers action
        '''
        __importParser = subparser.add_parser( "import", help=("Import a volume from an "
            "exported volume in an existing bucket."))
        __importParser.add_argument( "-" + AbstractPlugin.name_str, help="The name of the resulting new volume. When not supplied, the system derives a unique name from the exported volume.", required=False )

        group = __importParser.add_argument_group('required arguments')

        group.add_argument( "-" + AbstractPlugin.s3_object_prefix_str, help=(
            "Object prefix key that identifies the exported volume, obtained using "
            "list_exports command for a bucket."), required=True)
        group.add_argument( "-" + AbstractPlugin.s3_bucket_name_str, help=(
            "Bucket that contains the exported volume."), required=True)
        group.add_argument( "-" + AbstractPlugin.s3_access_key_str, help="S3 access key", required=True)
        group.add_argument( "-" + AbstractPlugin.s3_secret_key_str, help="S3 secret key", required=True)
        group.add_argument( "-" + AbstractPlugin.url_str, help=(
            "The URL where the bucket resides. For Formation, a value like "
            "\'https://us-east.formationds.com'. For AWS, a value like "
            "\'https://s3-us-west-2.amazonaws.com\'."), required=True)

        __importParser.set_defaults( func=self.import_volume, format="tabular")

    def create_snapshot_command(self, subparser):
        '''
        Create the parser for the create snapshot command
        '''
        __snapshotParser = subparser.add_parser( "create_snapshot", help="Create a snapshot from a specific volume.")
        __snapshotParser.add_argument( "-" + AbstractPlugin.format_str, help="Specify the format that the result is printed as", choices=["json","tabular"], required=False )
        __snapshotParser.add_argument( "-" + AbstractPlugin.name_str, help="The name to give this snapshot.", required=True)
        __snapshotParser.add_argument( "-" + AbstractPlugin.volume_id_str, help="The UUID of the volume that you'd like to take a snapshot of.", required=True)
        __snapshotParser.add_argument( "-" + AbstractPlugin.retention_str, help="The time (in seconds) that this snapshot will be retained.  0 = forever.", default=0, type=int )
        
        __snapshotParser.set_defaults( func=self.create_snapshot, format="tabular" )
        
    def create_list_snapshots_command(self, subparser):
        '''
        create the list snapshot command
        '''
        
        __listSnapsParser = subparser.add_parser( "list_snapshots", help="List all of the snapshots that exist for a specific volume.")
        __listSnapsParser.add_argument( "-" + AbstractPlugin.format_str, help="Specify the format that the result is printed as", choices=["json","tabular"], required=False )
        __listSnapsParser.add_argument( "-" + AbstractPlugin.volume_id_str, help="The UUID of the volume to list snapshots for.", required=True)
        
        __listSnapsParser.set_defaults( func=self.list_snapshots, format="tabular")
    
    def create_check_command(self, subparser):
        '''
        Create the parser for the volume check command
        '''
        __checkParser = subparser.add_parser( "check", help="Check a specified volume." )
        __checkGroup = __checkParser.add_mutually_exclusive_group( required=True)
        __checkGroup.add_argument( "-" + AbstractPlugin.volume_id_str, help="The UUID of the volume to check.")
        __checkGroup.add_argument( "-" + AbstractPlugin.volume_name_str, help="The name of the volume to check.  If the name is not unique, this call will fail.")
        __checkParser.set_defaults( func=self.check_volume, format="tabular" )

    def create_fix_command(self, subparser):
        '''
        Create the parser for the volume fix command
        '''
        __fixParser = subparser.add_parser( "fix", help="Fix a specified volume." )
        __fixGroup = __fixParser.add_mutually_exclusive_group( required=True)
        __fixGroup.add_argument( "-" + AbstractPlugin.volume_id_str, help="The UUID of the volume to fix.")
        __fixGroup.add_argument( "-" + AbstractPlugin.volume_name_str, help="The name of the volume to fix.  If the name is not unique, this call will fail.")
        __fixParser.set_defaults( func=self.fix_volume, format="tabular" )


    def create_safeguard_command(self, subparser):
        '''
        Creates the parser for the safeguard sub-command.

        Parameters
        ----------
        :type subparser: ``argparse._SubParsersAction)``
        :param subparser: parsers action
        '''
        __safeguardParser = subparser.add_parser("safeguard", help=("Volumes can optionally "
            "subscribe to one or many SafeGuard policies. SafeGuard policies can reference "
            "durable storage endpoints and enable management of data migration tasks. Available "
            "sub-commands are add, list, and remove."))

        safeguardSubParser = __safeguardParser.add_subparsers(help="Available sub-commands.")

        # Add subscription
        __parserForAdd = safeguardSubParser.add_parser("add", help=("Add SafeGuard subscription "
            "for a volume. Creates a recurring data migration task."));
        __parserForAdd.set_defaults(func=self.add_subscription, format="tabular")

        # Optional args
        __parserForAdd.add_argument(self.arg_str + AbstractPlugin.remote_volume_name_str, help=("For a "
            "recurring volume clone remote, gives the name of the remote volume."), required=False)

        # Required arguments
        groupForAdd = __parserForAdd.add_argument_group('required arguments')
        groupForAdd.add_argument(self.arg_str + AbstractPlugin.name_str, help="The subscription name.", default=None, required=True )
        groupForAdd.add_argument(self.arg_str + AbstractPlugin.safeguard_preset_str, help=("ID for a SafeGuard preset. "
            "See \'presets list\' command for ID values."), default=None, required=True)
        groupForAdd.add_argument(self.arg_str + AbstractPlugin.credential_str, help=("A credential name "
            "or unique identifier. See \'credentials list\' command for values."), default=None, required=True)
        groupForAdd.add_argument(self.arg_str + AbstractPlugin.volume_id_str, help=("Volume UUID."), required=True, type=long)

        # List subscriptions
        __parserForList = safeguardSubParser.add_parser("list", help="List all SafeGuard subscriptions for a volume.");

        # Required arguments
        groupForList = __parserForList.add_argument_group('required arguments')
        groupForList.add_argument(self.arg_str + AbstractPlugin.volume_id_str, help=("Volume UUID."), required=True, type=long)

        __parserForList.set_defaults(func=self.list_subscriptions, format="tabular")

        # Remove subscriptions
        __parserForRemove = safeguardSubParser.add_parser("remove", help="Remove SafeGuard subscription(s) for a volume.");

        #Optional args
        __parserForRemove.add_argument(self.arg_str + AbstractPlugin.name_str, help=("A subscription name "
            "or unique identifier. When not supplied, \'remove\' command will remove all subscriptions "
            "for the given volume."), required=False)

        # Required arguments
        groupForRemove = __parserForRemove.add_argument_group('required arguments')
        groupForRemove.add_argument(self.arg_str + AbstractPlugin.volume_id_str, help=("Volume UUID."), required=True, type=long)

        __parserForRemove.set_defaults(func=self.remove_subscription, format="tabular")

    #other class utilities
    def get_volume_service(self):
        '''
        Creates one instance of the volume service and it's accessed by this getter
        '''        
        return self.__volume_service           

    def get_named_credential_client(self):
        return self.__named_credential_client

    def get_subscription_client(self):
        return self.__subscription_client

    def pretty_print_volume(self, volume):
        '''
        Does a pretty version of printing out the volume details
        '''
        
        print( "Volume Name: {}\n".format( volume.name ) )
        
        basic_ov = OrderedDict()
        
        if ( hasattr( volume.settings, "max_object_size" ) ):
            basic_ov["Max Object Size"] = ByteConverter.convertBytesToString( volume.settings.max_object_size.size, 2 )

        if ( hasattr( volume.settings, "block_size" ) ):
            basic_ov["Block Size"] = ByteConverter.convertBytesToString( volume.settings.block_size.size, 2 )
                        
        basic_ov["Logical Bytes Used"] = ByteConverter.convertBytesToString( volume.status.current_usage.size )
        
        lastCapFirebreak = int( volume.status.last_capacity_firebreak )
        lastPerfFirebreak = int( volume.status.last_performance_firebreak )
            
        if ( lastCapFirebreak == 0 ):
            lastCapFirebreak = "Never"
        else:
            lastCapFirebreak = time.localtime( lastCapFirebreak )
            lastCapFirebreak = time.strftime( "%c", lastCapFirebreak )
            
        if ( lastPerfFirebreak == 0 ):
            lastPerfFirebreak = "Never"
        else:
            lastPerfFirebreak = time.localtime( lastPerfFirebreak )
            lastPerfFirebreak = time.strftime( "%c", lastPerfFirebreak )
        
        basic_ov["Last Capacity Firebreak"] = lastCapFirebreak
        basic_ov["Last Performance Firebreak"] = lastPerfFirebreak
        
        response_writer.ResponseWriter.writeTabularData( [basic_ov] )
        
        
        # DC section
        dc_ov = OrderedDict()
        print( "\nData Connector" )
        dc_ov["Type"] = volume.settings.type
        
        if ( hasattr( volume.settings, "capacity" ) ):
            dc_ov["Size to Report"] = ByteConverter.convertSizeToString( volume.settings.capacity.size, volume.settings.capacity.unit ) 
            
        if ( hasattr( volume.settings, "clients" ) ):
            dc_ov["Clients"] = volume.settings.clients
            
        if ( hasattr( volume.settings, "use_acls" ) ):
            dc_ov["Use ACLs"] = str( volume.settings.use_acls )
            
        if ( hasattr( volume.settings, "synchronous" ) ):
            dc_ov["Synchronous"] = str( volume.settings.synchronous )
            
        if ( hasattr( volume.settings, "use_root_squash" ) ):
            dc_ov["Use Root Squash"] = str( volume.settings.use_root_squash )
            
        if ( hasattr( volume.settings, "initiators" ) ):
            
            initStr = "";
            
            for initiator in volume.settings.initiators:
                initStr += initiator + ", "
                
            initStr = initStr[:-2]
            
            dc_ov["Initiators"] = initStr
                
        if ( hasattr( volume.settings, "lun_permissions" ) ):
            lunStr = ""
            
            for lun_permission in volume.settings.lun_permissions:
                lunStr += lun_permission.lun_name + ":" + lun_permission.permissions + ", "
                
            lunStr = lunStr[:-2]
            
            dc_ov["Lun Permissions"] = lunStr
            
        response_writer.ResponseWriter.writeTabularData( [dc_ov] )
            
        #Now that we did the metadata let's do the rest of the garabage
        print( "\nQuality of Service")
        qosData = response_writer.ResponseWriter.prep_qos_for_table( volume.qos_policy )
        response_writer.ResponseWriter.writeTabularData( qosData )
        
# Area for actual calls and JSON manipulation        
         
    def list_volumes(self, args):
        '''
        Retrieve a list of volumes in accordance with the passed in arguments
        '''
        response = []
        just_one_volume = False
        
        if AbstractPlugin.volume_id_str in args and args[AbstractPlugin.volume_id_str] is not None:
            response = self.get_volume_service().get_volume(args[AbstractPlugin.volume_id_str])
            response = [response]
            just_one_volume = True
        else:
            response = self.get_volume_service().list_volumes()
            
        #this means that we got a single thing... it's probably an error but 
        # we'll make it into an array here and deal with that below.
        if not isinstance( response, collections.Iterable):
            response = [response]
            
        #it really is an error object... instance just isn't matching
        if len(response) > 0 and (isinstance( response[0], FdsError ) or (hasattr( response[0], "error" ) and hasattr( response[0], "message" ))):
            return 1     
        
        if len( response ) == 0:
            print("No volumes found.")
            return  
        
        #write the volumes out
        if "format" in args  and args[AbstractPlugin.format_str] == "json":
            
            j_volumes = []
            
            for volume in response:
                j_volume = VolumeConverter.to_json(volume)
                j_volume = json.loads(j_volume)
                j_volumes.append( j_volume )
                
            response_writer.ResponseWriter.writeJson( j_volumes )
        else:
            
            if not just_one_volume:
                #The tabular format is very poor for a volume object, so we need to remove some keys before display
                response = response_writer.ResponseWriter.prep_volume_for_table( self.session, response )
                response_writer.ResponseWriter.writeTabularData( response )
            else:
                # since there is only one and they did not want json format... we'll do a special 
                # volume presentation
                self.pretty_print_volume( response[0] ) 
        

    def list_snapshot_policies(self, args):
        '''
        List out the policies attached to this volume
        '''
        snapshot_policy_service = SnapshotPolicyService(self.session)
        
        j_list = snapshot_policy_service.list_snapshot_policies( args[AbstractPlugin.volume_id_str])
        
        if isinstance( j_list, FdsError ):
            return
        
        if ( args[AbstractPlugin.format_str] == "json" ):
            j_policies = []
            
            for policy in j_list:
                j_policy = SnapshotPolicyConverter.to_json(policy)
                j_policy = json.loads( j_policy )
                j_policies.append( j_policy )
                
            response_writer.ResponseWriter.writeJson( j_policies )
        else:
            cleaned = response_writer.ResponseWriter.prep_snapshot_policy_for_table( self.session, j_list )
            response_writer.ResponseWriter.writeTabularData( cleaned )

    def create_iscsi_volume(self, args):
        volume = Volume()
        volume.type = "iscsi"
        self.add_iscsi_settings(volume, args)
        if args[AbstractPlugin.block_size_str] is not None:
            block_size = self.validate_block_size(args[AbstractPlugin.block_size_str],
                                                 args[AbstractPlugin.block_size_unit_str])
            volume.settings.block_size = block_size
        self.create_volume(args, volume)

    def create_block_volume(self, args):
        volume = Volume()
        volume.type = "block"
        self.add_block_settings(volume, args)
        if args[AbstractPlugin.block_size_str] is not None:
            block_size = self.validate_block_size(args[AbstractPlugin.block_size_str],
                                                 args[AbstractPlugin.block_size_unit_str])
            volume.settings.block_size = block_size
        self.create_volume(args, volume)

    def create_nfs_volume(self, args):
        volume = Volume()
        volume.type = "nfs"
        self.add_nfs_settings(volume, args)
        if args[AbstractPlugin.max_obj_size_str] is not None:
            obj_size = self.validate_object_size(args[AbstractPlugin.max_obj_size_str],
                                                 args[AbstractPlugin.max_obj_size_unit_str])
            volume.settings.max_object_size = obj_size
        self.add_nfs_settings(volume, args)
        self.create_volume(args, volume)

    def create_object_volume(self, args):
        volume = Volume()
        volume.type = "object"
        volume.settings = ObjectSettings()
        if args[AbstractPlugin.max_obj_size_str] is not None:
            obj_size = self.validate_object_size(args[AbstractPlugin.max_obj_size_str],
                                                 args[AbstractPlugin.max_obj_size_unit_str])
            volume.settings.max_object_size = obj_size
        self.create_volume(args, volume)

    def create_volume(self, args, volume):
        """
        Create a new volume.  The arguments are not all necessary (@see: Volume __init__) but the user
        must specify a name either in the -data construct or the -name argument
        """
        if args[AbstractPlugin.data_str] is None and args[AbstractPlugin.name_str] is None:
            print("Either -data or -name must be present")
            return
        # if -data exists all other arguments will be ignored!
        if args[AbstractPlugin.data_str] is not None:
            print( "WARN: Because a data argument exists, all other arguments will be ignored!")
            jsonData = json.loads( args[AbstractPlugin.data_str])
            volume = VolumeConverter.build_volume_from_json( jsonData )
        # build the volume object from the arguments
        else:
            volume.name = args[AbstractPlugin.name_str]
            volume.media_policy = args[AbstractPlugin.media_policy_str]
            # deal with the QOS preset selection if there was one
            if args[AbstractPlugin.qos_preset_str] is not None:
                qos_preset = self.get_volume_service().get_qos_presets(preset_id=args[AbstractPlugin.qos_preset_str])
                
                if len(qos_preset) >= 1:
                    qos_preset = qos_preset[0]
                    
                    volume.qos_policy.preset_id = qos_preset.id
                    volume.qos_policy.iops_max = qos_preset.iops_limit
                    volume.qos_policy.iops_min = qos_preset.iops_guarantee
                    volume.qos_policy.priority = qos_preset.priority
            else:                
                volume.qos_policy.iops_min = args[AbstractPlugin.iops_guarantee_str]
                volume.qos_policy.iops_max = args[AbstractPlugin.iops_limit_str]
                volume.qos_policy.priority = args[AbstractPlugin.priority_str]
                
            # deal with the continuous protection arg in the timeline preset if specified
            t_preset = None
            if args[AbstractPlugin.timeline_preset_str] is not None:
                t_preset = self.get_volume_service().get_data_protection_presets(preset_id=args[AbstractPlugin.timeline_preset_str])[0]
                
                volume.data_protection_policy = t_preset
                volume.data_protection_policy.preset_id = t_preset.id
            else:
                volume.data_protection_policy.commit_log_retention = args[AbstractPlugin.continuous_protection_str]

        response = self.get_volume_service().create_volume(volume)
        if isinstance(response, Volume):
            self.list_volumes(args)
        else:
            return 1
        return
    
    def get_credentials(self, cred_list ):
        '''
        helps parse the credential list and give back an object-ized version
        '''
        credentials = []
        
        for cred in cred_list:
            cred_args = cred.split(":")
               
            if cred_args is None:
                break
                
            credential = Credential(cred_args[0])
            
            if len( cred_args ) > 1:
                credential.password = cred_args[1]
            else:   
                credential.password = getpass.getpass( 'Password for ' + credential.username + ': ' )
            #fi
            
            credentials.append( credential )
        #end for
        
        return credentials
    
    def add_block_settings(self, volume, args ):
        '''
        Method to add all the block settings from the command line
        '''
        volume.settings = BlockSettings()
        size = None
        size_unit = None
        volume.settings.capacity = Size( size=args[AbstractPlugin.size_str], unit=args[AbstractPlugin.size_unit_str] )
        if AbstractPlugin.size_str in args:
            size = args[AbstractPlugin.size_str]
        if AbstractPlugin.size_unit_str in args:
            size_unit = args[AbstractPlugin.size_unit_str]
        if size is not None and size_unit is not None:
            volume.settings.capacity = Size(size=size, unit=size_unit)


    def add_nfs_settings(self, volume, args ):
        '''
        method to add the NFS specific settings
        '''
        volume.settings = NfsSettings()
        acls = args[AbstractPlugin.use_acls_str]
        squash = args[AbstractPlugin.use_root_squash_str]
        sync = args[AbstractPlugin.synchronous_str]
        size = None
        size_unit = None
        
        if ( AbstractPlugin.size_str in args ):
            size = args[AbstractPlugin.size_str]
        
        if ( AbstractPlugin.size_unit_str in args ):
            size_unit = args[AbstractPlugin.size_unit_str]
        
        if ( acls != None ):
            volume.settings.use_acls = acls
            
        if ( squash != None ):
            volume.settings.use_root_squash = squash
            
        if ( sync != None ):
            volume.settings.synchronous = sync
            
        if ( size != None and size_unit != None ):
            volume.settings.capacity = Size( size=size, unit=size_unit )
            
        clients = args[AbstractPlugin.clients]
        
        volume.settings.clients = clients
        
    def add_iscsi_settings(self, volume, args ):
        '''
        Method to handle putting the iscsi settings into the volume
        '''
        volume.settings = ISCSISettings()
        size = None
        size_unit = None

        if ( args[AbstractPlugin.incoming_creds_str] != None ):
            
            credentials = self.get_credentials( args[AbstractPlugin.incoming_creds_str] )
            volume.settings.incoming_credentials = credentials
            
        if ( args[AbstractPlugin.outgoing_creds_str] != None ):
            
            credentials = self.get_credentials( args[AbstractPlugin.outgoing_creds_str] )
            volume.settings.outgoing_credentials = credentials
            
        if ( args[AbstractPlugin.initiators_str] != None ):
            volume.settings.initiators = args[AbstractPlugin.initiators_str]
            
        if ( args[AbstractPlugin.lun_permissions_str] != None ):
            
            lun_permissions = []
            
            for lun in args[AbstractPlugin.lun_permissions_str]:
                lun_args = lun.split( ':' )
                lun_permission = LunPermissions( lun_name=lun_args[0] )
                
                if ( len( lun_args ) > 1 ):
                    lun_permission.permissions = lun_args[1]
                #fi
                lun_permissions.append( lun_permission )
            #for
            volume.settings.lun_permissions = lun_permissions

        if AbstractPlugin.size_str in args:
            size = args[AbstractPlugin.size_str]
        if AbstractPlugin.size_unit_str in args:
            size_unit = args[AbstractPlugin.size_unit_str]
        if size is not None and size_unit is not None:
            volume.settings.capacity = Size(size=size, unit=size_unit)

    def edit_volume(self, args):
        '''
        Edit an existing volume.  The arguments are not all necessary but the user must specify
        something to uniquely identify the volume
        '''
        
        volume = None
        isFromData = False
        
        if ( args[AbstractPlugin.data_str] is not None):
            isFromData = True
            jsonData = json.loads( args[AbstractPlugin.data_str] )
            volume =  VolumeConverter.build_volume_from_json( jsonData )  
        elif ( args[AbstractPlugin.volume_id_str] is not None ):
            volume = self.get_volume_service().get_volume( args[AbstractPlugin.volume_id_str] )
               
        if ( isinstance( volume, FdsError ) or volume is None or volume.id is None ):
            print("Could not find a volume that matched your entry.\n")
            return       
           
        if ( args[AbstractPlugin.iops_guarantee_str] is not None and isFromData is False ):
            volume.qos_policy.iops_min = args[AbstractPlugin.iops_guarantee_str]
            
        if ( args[AbstractPlugin.iops_limit_str] is not None and isFromData is False):
            volume.qos_policy.iops_max = args[AbstractPlugin.iops_limit_str]
            
        if ( args[AbstractPlugin.priority_str] is not None and isFromData is False):
            volume.qos_policy.priority = args[AbstractPlugin.priority_str]
            
        if ( args[AbstractPlugin.continuous_protection_str] is not None and isFromData is False):
            volume.data_protection_policy.commit_log_retention = args[AbstractPlugin.continuous_protection_str]      
            
        if ( volume.settings.type == "ISCSI" ):
            self.add_iscsi_settings( volume, args )
            
        if ( volume.settings.type == "NFS" ):
            self.add_nfs_settings( volume, args )
            
        #use the qos preset if it was provided
        if args[AbstractPlugin.qos_preset_str] != None:
            qos_preset = self.get_volume_service().get_qos_presets( args[AbstractPlugin.qos_preset_str] )
            
            if len(qos_preset) >= 1:
                qos_preset = qos_preset[0]
                volume.qos_policy.preset_id = qos_preset.id
                volume.qos_policy.iops_min = qos_preset.iops_guarantee
                volume.qos_policy.iops_max = qos_preset.iops_limit
                volume.qos_policy.priority = qos_preset.priority
            
        #if a timeline preset is provided we need to do the following
        # 1.  get a list of all attached policies
        # 2.  If the policy has the volume id_TIMELINE in the name we need to delete the policy
        # 3.  Create the policies like we do in the create method and attach them
        if args[AbstractPlugin.timeline_preset_str] != None:
            t_preset = self.get_volume_service().get_data_protection_presets(args[AbstractPlugin.timeline_preset_str])
            
            if len( t_preset ) >= 1:
                t_preset = t_preset[0]
                
                volume.data_protection_policy.commit_log_retention = t_preset.commit_log_retention
                
                #get attached policies
                policies = volume.data_protection_policy.snapshot_policies
                n_policies = []
                
                #clean up the current policy assignments
                for policy in policies:
                    
                    if not policy.type.startswith( volume.id + "SYSTEM_TIMELINE" ):
                        n_policies.append( policy )
                        
                volume.data_protection_policy.snapshot_policies = t_preset.snapshot_policies
                
                for policy in n_policies:
                    volume.data_protection_policy.snapshot_policies.append( policy ) 
                        
            
        response = self.get_volume_service().edit_volume( volume );
        
        if isinstance(response, Volume):
            args = [ args[AbstractPlugin.format_str]]
            self.list_volumes( args )   
        else:
            return 1              
            
    def clone_volume(self, args):
        '''
        Clone a volume from the argument list
        '''
        if ( args[AbstractPlugin.time_str] is not None ):
            fromTime = args[AbstractPlugin.time_str]
        
        volume = self.get_volume_service().get_volume( args[AbstractPlugin.volume_id_str] )
        
        if ( volume is None ):
            print("Could not find a volume associated with the input parameters.")
            return

        iops_guarantee = volume.qos_policy.iops_min
        iops_limit = volume.qos_policy.iops_max
        priority = volume.qos_policy.priority
        continuous_protection = volume.data_protection_policy.commit_log_retention
        media_policy = volume.media_policy

        
        if ( args[AbstractPlugin.iops_guarantee_str] is not None ):
            iops_guarantee = args[AbstractPlugin.iops_guarantee_str]
        
        if ( args[AbstractPlugin.iops_limit_str] is not None):
            iops_limit = args[AbstractPlugin.iops_limit_str]
            
        if ( args[AbstractPlugin.priority_str] is not None):
            priority = args[AbstractPlugin.priority_str]
            
        if ( args[AbstractPlugin.continuous_protection_str] is not None):
            continuous_protection = args[AbstractPlugin.continuous_protection_str]

        if ( args[AbstractPlugin.media_policy_str] is not None):
            media_policy = args[AbstractPlugin.media_policy_str]
        
        if ( args[AbstractPlugin.data_str] is not None ):
            jsonData = json.loads( args[AbstractPlugin.data_str] )
            
            qosData = jsonData["qosPolicy"]
            dataProtection = jsonData["dataProtectionPolicy"]
            
            if ( qosData["priority"] is not None ):
                priority = qosData["priority"]
                
            if ( qosData["iopsMin"] is not None ):
                iops_guarantee = qosData["iopsMin"]
                
            if ( qosData["iopsMax"] is not None ):
                iops_limit = qosData["iopsMax"]
                
            if ( dataProtection["commitLogRetention"] is not None ):
                continuous_protection = dataProtection["commitLogRetention"]
                
        if args[AbstractPlugin.qos_preset_str] != None:
            qos_preset = self.get_volume_service().get_qos_presets(args[AbstractPlugin.qos_preset_str])
            
            if len( qos_preset ) >= 1:
                qos_preset = qos_preset[0]
                iops_guarantee = qos_preset.iops_min
                iops_limit = qos_preset.iops_max
                priority = qos_preset.priority     
                volume.qos_policy.preset_id = qos_preset.id   
        
        #have to get continuous from a potential timeline preset
        t_preset = None
        if args[AbstractPlugin.timeline_preset_str] != None:
            t_preset = self.get_volume_service().get_data_protection_presets(args[AbstractPlugin.timeline_preset_str])
            
            if len( t_preset ) >= 1:
                t_preset = t_preset[0]
                
                continuous_protection = t_preset.commit_log_retention
        
        volume.qos_policy.iops_min = iops_guarantee
        volume.qos_policy.iops_max = iops_limit
        volume.qos_policy.priority = priority
        volume.data_protection_policy.commit_log_retention = continuous_protection
        volume.media_policy = media_policy
        
        if ( args[AbstractPlugin.remote_om_str] is not None ):
            # This is a volume clone remote request
            remote_volume = RemoteVolume()
            # A remote volume carries the remote OM, which is like
            # 'https://remoteOmUser:remoteOmPasswd@remoteOmHost:remoteOmPort'.
            remote_volume.remote_om_url = args[AbstractPlugin.remote_om_str]
            remote_volume.source_volume_name = volume.name
            # Replace volume name with new volume name
            volume.name = args[AbstractPlugin.name_str]
            remote_volume.volume = volume

            from_last_clone_remote = False
            if AbstractPlugin.incremental_str in args:
                from_last_clone_remote = args[AbstractPlugin.incremental_str]

            # capture recurrence data
            safeguard_preset = None
            if args[AbstractPlugin.safeguard_preset_str] != None:
                presets = self.get_volume_service().get_safeguard_presets(preset_id=args[AbstractPlugin.safeguard_preset_str])
                if isinstance(presets, FdsError):
                    return 1
                if (len(presets) == 0):
                    print("Missing SafeGuard preset identifier.")
                    return
                safeguard_preset = presets[0]

            # The remote domain is responsible for creating and attaching timeline preset
            # policies.
            response = self.get_volume_service().clone_remote( remote_volume, safeguard_preset, from_last_clone_remote )
            if not isinstance( response, FdsError ):
                print('Remote volume clone initiated.')
                return
            else:
                return 1

        volume.name = args[AbstractPlugin.name_str]

        # one URL when snapshot was chosen, a different one if the time / volume was chosen
        new_volume = None
        if ( args[AbstractPlugin.snapshot_id_str] is not None ):
            new_volume = self.get_volume_service().clone_from_snapshot_id( volume, args[AbstractPlugin.snapshot_id_str] )
        else:
            new_volume = self.get_volume_service().clone_from_timeline( volume, fromTime )
            
        if isinstance(new_volume, Volume):
            
            #if there was a timeline preset included, create and attach those policies now
            if t_preset is not None:
                
                for policy in t_preset.policies:
                    volume.data_protection_policy.snapshot_policies.append( policy ) 
                    
                volume.data_protection_policy.preset_id = t_preset.id               
            
            print("Volume cloned successfully.")
            args = [args[AbstractPlugin.format_str]]
            self.list_volumes( args );
        else:
            return 1
    
    def delete_volume(self, args):
        '''
        Delete the indicated volume
        '''
        vol_id = args[AbstractPlugin.volume_id_str]
        
        if AbstractPlugin.volume_name_str in args and args[AbstractPlugin.volume_name_str] is not None:
            volume = self.get_volume_service().find_volume_by_name( args[AbstractPlugin.volume_name_str])
            vol_id = volume.id
        
        response = self.get_volume_service().delete_volume( vol_id )
        
        if not isinstance( response, FdsError ):
            print('Deletion request completed successfully.')
            args = [args[AbstractPlugin.format_str]]
            self.list_volumes(args)
        else:
            return 1

    def check_volume(self, args):
        '''
        Checks a particular volume
        '''
        vol_id = args[AbstractPlugin.volume_id_str]

        if AbstractPlugin.volume_name_str in args and args[AbstractPlugin.volume_name_str] is not None:
            volume = self.get_volume_service().find_volume_by_name( args[AbstractPlugin.volume_name_str])
            vol_id = volume.id
        
        print('Issuing volume check operation. This may take a while...')
        response = self.get_volume_service().check_volume( vol_id )

        if not isinstance( response, FdsError ):
            print('Volume check request completed successfully. No error was found')
        else:
            # TODO - be more specific w.r.t. FdsError
            print('Volume check request completed successfully. Some error was found')
            return 1

    def fix_volume(self, args):
        '''
        Fix a particular volume
        '''
        vol_id = args[AbstractPlugin.volume_id_str]

        if AbstractPlugin.volume_name_str in args and args[AbstractPlugin.volume_name_str] is not None:
            volume = self.get_volume_service().find_volume_by_name( args[AbstractPlugin.volume_name_str])
            vol_id = volume.id
        
        print('Issuing volume rescue operation. This may take a while...')
        response = self.get_volume_service().fix_volume( vol_id )

        if not isinstance( response, FdsError ):
            print('Volume rescue request completed successfully. No error was found')
        else:
            # TODO - be more specific w.r.t. FdsError
            print('Volume rescue request completed successfully. Some error was found')
            return 1


    def import_volume(self, args):
        '''
        Import volume from exported volume in existing S3 bucket.
        '''
        new_volume_name = None
        if AbstractPlugin.name_str in args and args[AbstractPlugin.name_str] is not None:
            new_volume_name = args[AbstractPlugin.name_str]
        else:
            print "New volume name required"
            return 1

        repository = Repository()
        repository.credentials.access_key_id = args[AbstractPlugin.s3_access_key_str]
        repository.credentials.secret_key = args[AbstractPlugin.s3_secret_key_str]
        repository.bucket_name = args[AbstractPlugin.s3_bucket_name_str]
        repository.url = args[AbstractPlugin.url_str]
        repository.obj_prefix_key = args[AbstractPlugin.s3_object_prefix_str]
        repository.new_volume_name = new_volume_name

        response = self.get_volume_service().import_volume(new_volume_name, repository)

        if not isinstance( response, FdsError ):
            print('Import initiated.')
            return
        else:
            return 1

    def export_volume(self, args):
        '''
        Export volume to existing S3 bucket.
        '''
        volume = self.get_volume_service().get_volume( args[AbstractPlugin.volume_id_str] )

        if isinstance(volume, FdsError):
            return 1

        if ( volume is None ):
            print("Could not find a volume associated with the input parameters.")
            return

        repository = Repository()
        repository.credentials.access_key_id = args[AbstractPlugin.s3_access_key_str]
        repository.credentials.secret_key = args[AbstractPlugin.s3_secret_key_str]
        repository.bucket_name = args[AbstractPlugin.s3_bucket_name_str]
        repository.url = args[AbstractPlugin.url_str]
        repository.volume_id = volume.id

        from_last_export = False
        if AbstractPlugin.incremental_str in args:
            from_last_export = args[AbstractPlugin.incremental_str]

        # capture recurrence data
        safeguard_preset = None
        if args[AbstractPlugin.safeguard_preset_str] != None:
            presets = self.get_volume_service().get_safeguard_presets(preset_id=args[AbstractPlugin.safeguard_preset_str])
            if isinstance(presets, FdsError):
                return 1
            if (len(presets) == 0):
                print("Missing SafeGuard preset identifier.")
                return
            safeguard_preset = presets[0]

        response = self.get_volume_service().export_volume( volume, repository, safeguard_preset, from_last_export )
        if not isinstance( response, FdsError ):
            print('Export initiated.')
            self.list_volumes(args)
        else:
            return 1

    def create_snapshot(self, args):
        '''
        Create a snapshot for a volume
        '''
        
        volume = self.get_volume_service().get_volume( args[AbstractPlugin.volume_id_str] )
            
        if ( volume is None ):
            print("No volume found with the specified identification.\n")
            return
        
        snapshot = Snapshot()
        
        snapshot.name = args[AbstractPlugin.name_str]
        snapshot.retention = args[AbstractPlugin.retention_str]
        snapshot.volume_id = volume.id
        
        response = self.get_volume_service().create_snapshot( snapshot )
        
        if isinstance(response, Snapshot):
            self.list_snapshots(args)
        else:
            return 1
         
    def list_exports(self, args):
        '''
        List all available exports in a given bucket.
        '''
        repository = Repository()
        repository.credentials.access_key_id = args[AbstractPlugin.s3_access_key_str]
        repository.credentials.secret_key = args[AbstractPlugin.s3_secret_key_str]
        repository.bucket_name = args[AbstractPlugin.s3_bucket_name_str]
        repository.url = args[AbstractPlugin.url_str]

        response = self.get_volume_service().list_exports_in_bucket(repository)

        if isinstance( response, FdsError ):
            return 1
        
        if ( len( response ) == 0 ):
            print("No exported volumes found for bucket {}".format(repository.bucket_name))
        
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

    def list_snapshots(self, args):
        '''
        List snapshots for this volume
        '''
        volId = args[AbstractPlugin.volume_id_str]
            
        response = self.get_volume_service().list_snapshots(volId)
        
        if isinstance( response, FdsError ):
            return 1
        
        if ( len( response ) == 0 ):
            print("No snapshots found for volume with ID " + volId)
        
        #print it all out
        if "format" in args  and args[AbstractPlugin.format_str] == "json":
            
            j_snapshots = []
            
            for snapshot in response:
                j_snapshot = SnapshotConverter.to_json(snapshot)
                j_snapshot = json.loads( j_snapshot )
                j_snapshots.append( j_snapshot )
                
            response_writer.ResponseWriter.writeJson( j_snapshots )
        else:
            resultList = response_writer.ResponseWriter.prep_snapshot_for_table( self.session, response)
            response_writer.ResponseWriter.writeTabularData( resultList )

    def add_subscription(self, args):
        '''
        Parameters
        ----------
        :type args: dict
        '''
        # Get named credential
        credential_key = args[AbstractPlugin.credential_str]
        if (credential_key is None or len(credential_key) == 0):
            print("Missing named credential name or unique identifier. See \'cred\' command.")
            return

        named_credential = self.get_named_credential_client().get_named_credential(credential_key)
        if not isinstance(named_credential, NamedCredential):
            if named_credential is None:
                print("Named credential \'{}\' not found. See \'cred\' command for saving "
                    "named credentials.".format(credential_key))
            return

        # Get recurrence rule
        preset_id = args[AbstractPlugin.safeguard_preset_id_str]
        presets = self.get_safeguard_presets(preset_id)
        if isinstance(presets, FdsError):
            return 1
        if (len(presets) == 0):
            print("Missing SafeGuard preset identifier.")
            return
        safeguard_preset = presets[0]

        subscription = Subscription()

        # Required args
        subscription.volume_id = args[AbstractPlugin.volume_id_str]
        subscription.name = args[AbstractPlugin.name_str]

        # Optional args
        if args[AbstractPlugin.remote_volume_str] is not None:
            subscription.remote_volume = args[AbstractPlugin.remote_volume_str]

        # Named credential and recurrence rule
        subscription.named_credential = named_credential
        subscription.recurrence_rule = safeguard_preset.recurrence_rule

        # TODO: Check for existence
        response = self.get_subscription_client().create_subscription(subscription)
        if isinstance(response, FdsError):
            return 1
        

    def list_subscriptions(self, args):
        '''
        Parameters
        ----------
        :type args: dict
        '''
        volume_id = args[AbstractPlugin.volume_id_str]
        response = self.get_subscription_client().list_subscriptions(volume_id)

        if isinstance( response, FdsError ):
            return 1

        if len(response) == 0:
            print("\nNo subscriptions for volume {0}".format(volume_id))
            return

        if args[AbstractPlugin.format_str] == "json":
            j_subscriptions = []

            for subscription in response:
                j_subscription = SubscriptionConverter.to_json(subscription)
                j_subscription = json.loads(j_subscription)
                j_subscriptions.append(j_subscription)

            ResponseWriter.writeJson(j_subscriptions)
        else:
            p_subscriptions = response_writer.ResponseWriter.prep_subscriptions_for_table(response)
            response_writer.ResponseWriter.writeTabularData(p_subscriptions)

    def remove_subscription(self, args):
        '''
        '''
        digest = None
        if (AbstractPlugin.id_str in args and
            args[AbstractPlugin.id_str] is not None):

           digest = args[AbstractPlugin.id_str]

        elif (AbstractPlugin.name_str in args and
            args[AbstractPlugin.name_str] is not None):

            # Look up by name
            subscription = self.get_subscription_client().get_subscription_by_name(args[AbstractPlugin.name_str])
            digest = subscription.digest

        if digest is None:
            print('Subscription not found')
            return

        response = self.get_subscription_client().remove_subscription(digest)
        
        if not isinstance(response, FdsError):
            print('Deletion request completed successfully.')
        else:
            return 1

        return

    @staticmethod
    def validate_object_size(max_obj_size_str, max_obj_size_unit_str):
        if max_obj_size_str is not None:
            obj_size = Size(size=max_obj_size_str, unit=max_obj_size_unit_str)
            if obj_size.get_bytes() < (4 * 1024) or obj_size.get_bytes() > (8 * pow(1024, 2)):
                print("Warning: The maximum object size you entered is outside the bounds of 4KB and 8MB.  "
                      "The actual value will be the system default (typically 2MB)")
            return obj_size

    @staticmethod
    def validate_block_size(block_size_str, block_size_unit_str):
        if block_size_str is not None:
            block_size = Size(size=block_size_str, unit=block_size_unit_str)
            if block_size.get_bytes() < (4 * 1024) or block_size.get_bytes() > (8 * pow(1024, 2)):
                print("Warning: The block size you entered is outside the bounds of 4KB and 8MB. The actual value will "
                      "be the system default (typically 128KB)")
            return block_size

