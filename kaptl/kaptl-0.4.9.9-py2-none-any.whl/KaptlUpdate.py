import os
import sys

from Utils import Utils

from Common import Common


class KaptlUpdate:
    def __init__(self, session, arguments):
        for filename in os.listdir(os.getcwd() + "/.kaptl"):
            if filename.endswith(".kaptl.old"):
                self.app_name = Utils.get_manifest_data()["appName"]

        if self.app_name is "":
            print "ERROR: Directory does not contain a KAPTL project"
            sys.exit()

        rec = arguments["--recipe"]
        if rec:
            try:
                oldRecipe = Utils.get_manifest_data()["recipe"]
                if oldRecipe != rec:
                    # Change in the recipe continue to update the recipe
                    print("Changing recipe from {} to {}\n".format(oldRecipe, rec))
                    Utils.set_manifest_data("recipe", rec)
            except KeyError:
                print("Old recipe not found in manifest, setting recipe to {}.".format(rec))
                Utils.set_manifest_data("recipe",rec)


        self.kaptl_cookie = {"kaptl-session-id": self.app_name}
        self.arguments = arguments
        self.session = session
        self.license = Utils.manifest("license") if not arguments["--license"] else arguments["--license"]
        self.recipe = Utils.manifest("recipe")
        if not self.recipe:
            print("ERROR: Recipe not found in manifest or not set in command parameters.")
            sys.exit()
        self.common_methods = Common(self.session)
        self.rules = Utils.read_rules_from_file(os.getcwd() + "/app.kaptl")
        self.rules_old = Utils.read_rules_from_file(os.getcwd() + "/.kaptl/app.kaptl.old")
        self.file_info = None
        self.angular_only = False
        self.stack = Utils.get_stack_info_from_manifest()
        self.app_id = Utils.get_id_from_manifest()
        self.angular_only = Utils.check_if_angular_only(self.stack)
        self.mode = arguments["--mode"]


    def update_project(self):
        session_name = self.common_methods.parse_rules(self.session, self.rules, self.stack, self.kaptl_cookie,
                                                       self.license, self.recipe, self.app_name)
        if session_name is not None:
            self.file_info = self.common_methods.get_file_info(self.session, session_name, self.rules, self.stack,
                                                               self.recipe, self.mode, self.angular_only, self.app_id,
                                                               self.license, self.app_name)
            if self.file_info is not None:
                self.common_methods.download_file(self.session, self.file_info)
                self.common_methods.unzip_archive(self.file_info[1], existing=False)
            else:
                print "ERROR: Couldn't retrieve a file from the server. Try again later."
                sys.exit()
        else:
            # just exit, parse_rules will print the info about what happened
            sys.exit()
