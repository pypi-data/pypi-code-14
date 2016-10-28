# -*- coding: utf-8 -*-
import json
import os
import time
from ConfigParser import SafeConfigParser
from collections import OrderedDict
from collections import namedtuple

import requests

import GlobalValue
from GlobalValue import ZetModule
from GlobalValue import templateType_map
from InputOutputDefine import Input
from InputOutputDefine import Output
from InputOutputDefine import Param

curdir = GlobalValue.currentDir

class Util:
    @staticmethod
    def makedir(path):
        path = path.lower()
        if not os.path.exists(path):
            os.makedirs(path)

    @staticmethod
    def getParamterFromcfg():
        '''get parameter from screwjack.cfg'''
        cfg = SafeConfigParser()
        cfg.read(os.path.expanduser("~/.screwjack.cfg"))
        return cfg

    @staticmethod
    def tarballFiles(_moudleName):
        '''tar package'''
        import re
        fileroot = "%s/upload/%s/tar" % (curdir,_moudleName)
        files = [i[0][0] for i in
                 [re.findall(r'^ADD (.*) (.*)$', line) for line in open(os.path.join(fileroot,"Dockerfile"))]
                 if len(i) > 0]
        files.append("Dockerfile")
        with open(os.path.join(fileroot,"spec.json"), "r") as sj:
            sj = json.load(sj, object_pairs_hook=OrderedDict)
        filename = "%s-%s.tar" % (sj['Name'].lower(), sj['Version'])

        print("Packaging files: %s into '%s'" % (files, filename))
        import tarfile

        with tarfile.open(os.path.join(fileroot,filename), "w") as tar:
            for name in files:
                tar.add(os.path.join(fileroot,name),name)

        return "%s/upload/%s/tar/%s" % (GlobalValue.currentDir, _moudleName, filename)

    @staticmethod
    def submit(zetmoudle,notebookrealpath,templateType,is_private=False):
        '''is_private：wether only myself seen
        submit
        '''
        def async_wait_submit(zetmoudle, job_id):
            print("Waiting :'%s'" % job_id)
            while True:
                time.sleep(1)
                spec_status_url = "http://%s/status" % zetmoudle.spec_server

                r = requests.get(spec_status_url,
                                 params={"id": job_id},
                                 headers={'x-spec-auth': cfg.get('user', 'spec_auth')})
                rj = r.json()
                if rj['status'] == 'success':
                    return True
                elif rj['status'] == 'pending':
                    print ".",
                    continue
                elif rj['status'] == 'failed':
                    print("Failed to build : '%s'" % rj['message'])
                    return False
                else:
                    print("Unknow status : '%s'" % rj['status'])
                    return False
        print "Importing to spec_server : '%s' ..." % zetmoudle.spec_server
        spec_push_url = "http://%s/spec/import" % zetmoudle.spec_server

        sj = zetmoudle.spec_json

        spec_push_params = {
            "user": zetmoudle.username,
            "templateType": templateType_map[templateType],
            "private": is_private
        }

        cfg = SafeConfigParser()
        cfg.read(os.path.expanduser("~/.screwjack.cfg"))

        r = requests.post(spec_push_url,
                          files={'moduletar': open(notebookrealpath, "rb")},
                          headers={'x-spec-auth': cfg.get('user', 'spec_auth')},
                          params=spec_push_params)

        if r.status_code != 200:
            return "ERROR : Failed to submit\n%s\n%s" % (r.text,r.url)
        else:
            print(r.text)
            if not async_wait_submit(zetmoudle, r.json()["id"]):
                res = "ERROR : Failed to submit module %s" % notebookrealpath
                print(res)
                return res
            else:
                res = "Successful submit module %s" % notebookrealpath
                print (res)
                return res




    @staticmethod
    def get_settings_from_file(filename):

        _globalscripts = filename#os.path.join(os.path.dirname(filename),"global.json")
        with open(filename, "r") as f:
            _jsondict = json.load(f)
        _moudleName = _jsondict["Name"]

        def global_param_builder(param_json):
            return {k: v['Val'] for k, v in param_json.items()}

        def input_output_builder(spec_input, spec_output):
            inputs = "%s/upload/%s/inputs" % (curdir,_moudleName)
            #TODO
            inputSettings = namedtuple('InputSettings', spec_input.keys())
            # for in_k, in_type in spec_input.items():
            #     ll = []
            #     for fileName in os.listdir(inputs):
            #         if fileName.endswith(in_type[0]):
            #             ll.append(fileName)
            #     print ll
            #     dictss = {in_k,Input(ll,in_type)}
            #     print dictss
            in_params = {in_k: Input([fileName for fileName in os.listdir(inputs) if fileName.endswith(in_type[0])], in_type) for in_k, in_type in spec_input.items()}
            input_settings = inputSettings(**in_params)

            OutputSettings = namedtuple('OutputSettings', spec_output.keys())
            out_params = {out_k: Output(out_k, out_type) for out_k, out_type in spec_output.items()}
            output_settings = OutputSettings(**out_params)

            return input_settings, output_settings

        def get_json_file(filename):
            with open(filename, "r") as f:
                return json.load(f)

        def param_builder(spec_param, param_json):
            def get_param(k):
                    return spec_param[k]['Default']

            ParamSettings = namedtuple('ParamSettings', spec_param.keys())
            param_dict = {k: Param(get_param(k), v,v.get("scope",None)) for k, v in spec_param.items()}
            env_settings = ParamSettings(**param_dict)
            return env_settings

        def get_settings(spec_json,_globalscripts):
            moderate_keys = ['Name', 'Param', 'Input', 'Output', 'Cmd', 'Description']
            if not all(k in spec_json for k in moderate_keys):
                raise ValueError("One of param from %s may not exist in 'spec.json'" % str(moderate_keys))

            # TODO: condition for appending 'GlobalParam'
            moderate_keys.append('GlobalParam')
            ModuleSetting = namedtuple('ModuleSetting', moderate_keys)

            param_json = get_json_file(_globalscripts)

            param = param_builder(spec_json['Param'], param_json['PARAM'])
            json_input, json_output = input_output_builder(spec_json['Input'], spec_json['Output'],)

            # TODO:
            global_param = global_param_builder(param_json['GLOBAL_PARAM'])
            settings = ModuleSetting(Name=spec_json['Name'], Description=spec_json['Description'], Param=param,
                                     Input=json_input, Output=json_output, Cmd=spec_json['Cmd'], GlobalParam=global_param)
            return settings



        with open(filename, "r") as f:
            return get_settings(_jsondict,_globalscripts)


if __name__ == "__main__":

    import GlobalValue
    curDir = GlobalValue.currentDir
    obj = ZetModule("/home/lj/IdeaProjects/FlaskTest/upload/testlj/")
    Util.submit(obj,"/home/lj/IdeaProjects/FlaskTest/upload/testlj/tar/testlj-.tar","none")