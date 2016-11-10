import sys

from Utils import Utils

from Common import Common
from exceptions import *


class KaptlInit:
    def __init__(self, session, arguments):
        self.arguments = arguments
        self.app_name = self.arguments["<name>"]
        self.session = session
        self.common_methods = Common(self.session)
        self.licenseKey = self.arguments["--license"]
        self.recipe = self.arguments["--recipe"]
        self.mode = self.arguments["--mode"]

        if self.arguments["<rules>"]:
            self.rules = self.arguments["<rules>"]
        elif self.arguments["--rules-file"]:
            self.rules = Utils.read_rules_from_file(self.arguments["--rules-file"])
        else:
            print "ERROR: Cannot find rules to use for creating a project. Aborting..."
            sys.exit()

        self.file_info = None

        self.stack = {}
        try:
            self.stack = Utils.get_stack_info(self.arguments)
        except WrongStackInfoException, e:
            print e.message
            sys.exit()

        self.angular_only = Utils.check_if_angular_only(self.stack)

    def initialize_project(self):
        self.session_name = self.common_methods.parse_rules(self.session, self.rules, self.stack, None, self.licenseKey, self.recipe, self.app_name)
        if self.session_name is not None:
            self.file_info = self.common_methods.get_file_info(
                self.session, self.session_name, self.rules, self.stack, self.recipe, "full", self.angular_only, False, self.licenseKey, self.app_name)
            if self.file_info is not None:
                self.common_methods.download_file(self.session, self.file_info)
                self.common_methods.unzip_archive(self.file_info[1], existing=False)
            else:
                print "ERROR: Couldn't retrieve a file from the server. Try again later."
                sys.exit()
        else:
            # just exit, parse_rules will print the info about what happened
            sys.exit()
