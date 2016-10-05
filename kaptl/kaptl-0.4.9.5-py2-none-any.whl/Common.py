import os
import sys
import zipfile

import pyprind
import requests

from Utils import Utils

KAPTL_HOST = "https://www.kaptl.com"
#KAPTL_HOST = "http://kaptl.dev"
#KAPTL_HOST = "http://localhost:62958"
KAPTL_PARSE_URL = KAPTL_HOST + "/api/apps/parse"
KAPTL_DOWNLOAD_URL = KAPTL_HOST + "/api/apps/download"


class Common:
    def __init__(self, session):
        self.session = session

    @staticmethod
    def parse_rules(session, rules, stack, kaptl_cookie=None, license=None, recipe=None, app_name=""):
        print "Parsing the rules..."
        try:
            response = Common.send_parse_rules_request(session, rules, stack, kaptl_cookie, license, recipe, app_name)
            response_content = response.json()
            if response.status_code and response_content["success"]:
                print "KAPTL build completed successfully."
                return response_content["sessionName"]
            else:
                print "ERROR: KAPTL build error."
                if response_content["compilerOutput"]:
                    print response_content["compilerOutput"]
                return None
        except requests.exceptions.RequestException:
            print("ERROR: API is unavailable at the moment, please try again later")
            sys.exit()

    @staticmethod
    def send_parse_rules_request(session, rules, stack, kaptl_cookie=None, license=None, recipe=None, app_name="", return_compiler_output = False):
        request_data = dict(rulesText=rules.replace('\\', '').replace('\'', '"'), stack=stack, licenseKey=license,
                            recipe=recipe, appName=app_name, returnCompilerOutput = return_compiler_output)
        if recipe is not None:
            request_data["recipe"] = recipe
        try:
            if kaptl_cookie is not None:
                response = session.post(KAPTL_PARSE_URL, json=request_data, cookies=kaptl_cookie)
            else:
                response = session.post(KAPTL_PARSE_URL, json=request_data)
            return response
        except requests.exceptions.RequestException:
            print("ERROR: API is unavailable at the moment, please try again later")
            sys.exit()


    @staticmethod
    def isUpdate(mode):
        if mode is None:
            return True
        if mode == "full":
            return False
        return True

    @staticmethod
    def get_file_info(session, session_name, rules, stack, recipe, mode, angular_only=False, app_id=0, license=None,
                      app_name=None, email=None):
        print "Downloading the generated app..."
        request_data = dict(app = {
            'appId': app_id,
            'sessionName': session_name,
            'appName': app_name,
            'rulesText': rules,
            'stack': stack,
            'licenseKey': license,
            'recipe': recipe
        }, email=email, angularOnly=angular_only, isUpdate=Common.isUpdate(mode))


        try:
            response = session.post(KAPTL_DOWNLOAD_URL, json=request_data)
            response_content = response.json()
            if response.status_code and response_content["success"]:
                return response_content["fileUrl"], response_content["fileName"]
            else:
                return None
        except requests.exceptions.RequestException:
            print("ERROR: API is unavailable at the moment, please try again later.")
            sys.exit()

    @staticmethod
    def download_file(session, file_info):
        try:
            with open(file_info[1], 'wb') as f:
                r = session.get(file_info[0], stream=True)
                total_length = int(r.headers.get('content-length'))
                bar = pyprind.ProgBar(total_length / 1024)
                if total_length is None:  # no content length header
                    f.write(r.content)
                else:
                    for chunk in r.iter_content(1024):
                        f.write(chunk)
                        bar.update()
        except IOError:
            print "ERROR: Couldn't download a file"
            sys.exit()

    @staticmethod
    def unzip_archive(filename, existing):
        try:
            with open(filename, "rb") as f:
                z = zipfile.ZipFile(f)
                if existing:
                    result = Utils.query_yes_no("This action may override changes you already made to your project "
                                                "in the current directory. Do you want to proceed?")
                    if result == "yes" or result == "y":
                        for name in z.namelist():
                            z.extract(name, os.getcwd())
                    elif result == "no" or result == "n":
                        print "Exiting the program..."
                else:
                    for name in z.namelist():
                        z.extract(name, os.getcwd())
            try:
                print "Cleaning up..."
                os.remove(filename)
            except IOError:
                print "ERROR: Couldn't delete a zip file"
        except IOError:
            print "ERROR: Couldn't unzip the file"
