# ----------------------------------------------------------
#  Copyright (c) Microsoft Corporation. All rights reserved. 
#  Licensed under the MIT License. See License.txt in the 
#  project root for license information.  If License.txt is 
#  missing, see https://opensource.org/licenses/MIT
# ----------------------------------------------------------

"""File for all argument parsing"""
import sys
import os
import os.path
import argparse
from collections import namedtuple

class ArgsOutput(object):
    """Class that contains all arguments passed to app"""
    def __init__(self):
        """Constructor"""

        self.args_file = ""
        self.subscription_key = ""
        self.command = ""
        self.workflow_id = ""
        self.process_name = ""
        self.process_args = ""

        self.input_storage_account_type = ""
        self.input_storage_account_name = ""
        self.input_storage_account_key = ""
        self.input_storage_account_container = ""
        self.input_storage_account_vdir = ""
        #self.input_storage_account_container_sas = ""
        self.input_blob_name_1 = ""
        self.input_blob_name_2 = ""


        self.output_storage_account_type = ""
        self.output_storage_account_name = ""
        self.output_storage_account_key = ""
        self.output_storage_account_container = ""
        self.output_storage_account_vdir = ""
        #self.output_storage_account_container_sas = ""
        self.output_overwrite = False
        self.output_filename_base = ""
        self.output_include_logfiles = True

        self.local_input_1 = ""
        self.local_input_2 = ""
        self.local_output_path = ""
        self.blobxfer_path = ""
        self.azure_as_cache_mode = False

        self.api_url_base = ""
        self.no_poll = False
        self.debug_mode = False

        self.input_dictionary = dict()
        self.output_dictionary = dict()

    def get_file_path(self):
        """Parses path considering Linux and Windows scenarios"""
        file_path = self.args_file
        #if not file_path.strip():
        #    return None
        file_path = self.args_file.strip()
        if os.path.isfile(file_path):
            # file exists
            return file_path
        else:
            # file_path is non-empty but not a full filepath
            slash = "/"
            if os.name == "nt":
                #Windows
                slash = "\\"
            # Assume file with no directory refers to current directory
            if slash not in file_path:
                file_path = os.path.dirname(os.path.realpath(sys.argv[0])) + slash + file_path
                if os.path.isfile(file_path):
                    return file_path

            # Nothing specified, try default config.txt
            file_path = os.path.dirname(os.path.realpath(sys.argv[0])) + slash + "config.txt"
            if os.path.isfile(file_path):
                return file_path
            else:
                return None

    def parse_args_from_file(self):
        """Iterates through all arguments found in the file"""
        file_path = self.get_file_path()

        if file_path:
            with open(file_path) as argsfile:
                lines = argsfile.readlines()
                for line in lines:
                    if line is None or line == "" or line.startswith("#"):
                        continue
                    columns = line.split(':', 1)
                    if len(columns) == 2:
                        key = columns[0].strip()
                        value = columns[1].strip()
                        self.set_args_value(key, value)

    def set_args_value(self, key, value):
        """Sets class properties from key value pair"""
        if str(value).lower() == "true" or str(value).lower() == "false":
            bool_value = str(value).lower() == "true"
            setattr(self, key, bool_value)
            return
        if key == "command":
            setattr(self, key, str(value).upper())
            return

        setattr(self, key, value)

    def parse_args_from_command_line(self):
        """Parses arguments from command line and settings file if present"""
        parser = argparse.ArgumentParser(
            description="""A command-line tool to run genomics processes on
                        the Microsoft Genomics platform.
                        Example usage: please consult documentation""")

        parser.add_argument(
            "-f",
            help="""Specifies a settings file to look for
                    command-line arguments.
                    Command-line arguments will take precedence
                    and override the file.""",
            required=False)


        parser.add_argument("-command", help="", required=False)
        parser.add_argument("-workflow_id", help="", required=False)

        parser.add_argument("-process_name",
                            help="Name of the genomics process.",
                            required=False)
        parser.add_argument("-process_args",
                            help="Arguments for the genomics process.", required=False)

        parser.add_argument("-input_storage_account_type", help="", required=False)
        parser.add_argument("-input_storage_account_name", help="", required=False)
        parser.add_argument("-input_storage_account_key", help="", required=False)
        parser.add_argument("-input_storage_account_container", help="", required=False)
        parser.add_argument("-input_storage_account_vdir", help="", required=False)
        parser.add_argument("-input_blob_name_1", help="", required=False)
        parser.add_argument("-input_blob_name_2", help="", required=False)
        parser.add_argument("-local_input_1", help="", required=False)
        parser.add_argument("-local_input_2", help="", required=False)
        parser.add_argument("-blobxfer_path", help="", required=False)

        parser.add_argument("-output_storage_account_type", help="", required=False)
        parser.add_argument("-output_storage_account_name", help="", required=False)
        parser.add_argument("-output_storage_account_key", help="", required=False)
        parser.add_argument("-output_storage_account_container", help="", required=False)
        parser.add_argument("-output_storage_account_vdir", help="", required=False)
        parser.add_argument("-output_blob_name_prefix", help="", required=False)
        parser.add_argument("-output_overwrite", help="", required=False)
        parser.add_argument("-output_filename_base", help="", required=False)
        parser.add_argument("-output_include_logfiles", help="", required=False)
        parser.add_argument("-local_output_path", help="", required=False)
        parser.add_argument("-azure_as_cache_mode", help="", required=False)

        parser.add_argument("-no_poll", help="", required=False)
        parser.add_argument("-api_url_base", help="", required=False)
        parser.add_argument("-debug_mode", help="", required=False)
        parser.add_argument("-subscription_key", help="", required=False)

        args = vars(parser.parse_args())

        arg_name = "f"
        if args[arg_name] != None:
            self.args_file = str(args[arg_name]).strip()

        self.parse_args_from_file()


        # manually parse each arg and override values from settings file
        for key, value in args.iteritems():
            if value != None:
                self.set_args_value(key, value)

    def validate(self):
        """Checks if required arguments provided"""
        if self.command == "SUBMIT":
            return
        elif self.command == "GETSTATUS":
            if self.workflow_id == "":
                print """You must specify a worklow_id in config.txt
                         or via the commandline, like: -workflow_id 101"""
                sys.exit(1000)
        elif self.command == "CANCEL":
            if self.workflow_id == "":
                print """You must specify a worklow_id in config.txt
                      or via the commandline, like: -workflow_id 101"""
                sys.exit(1000)
        elif self.command == "LIST":
            return

    def get_storage_accounts_info(self):
        """
        Returns a named tuple with the input and output storage information
        """
        AccountInfo = namedtuple(
            "AccountInfo",
            "name key container virtual_dir")
        StorageInfo = namedtuple(
            "StorageInfo",
            "input output")
        storage_info = StorageInfo(
            AccountInfo(
                self.input_storage_account_name,
                self.input_storage_account_key,
                self.input_storage_account_container,
                self.input_storage_account_vdir),
            AccountInfo(
                self.output_storage_account_name,
                self.output_storage_account_key,
                self.output_storage_account_container,
                self.output_storage_account_vdir))

        return storage_info
