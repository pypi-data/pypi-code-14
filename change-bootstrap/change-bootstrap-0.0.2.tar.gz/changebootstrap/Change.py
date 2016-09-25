#!/usr/bin/env python
# coding=utf8

import time
import os
import sys
import shutil
import subprocess
import argparse
import logging
import json
import tempfile
import uuid
import subprocess
import datetime

import requests

import LocalDeployment
import LocalDeploymentSettings


class ChangeFacade(object):
    def __init__(self):
        pass

    def bootstrap(self, args):
        deployTemplateJsonStr = '''
{
    "environment": {
        "name": "ChangeAgent/Mao",
        "alias": "ChangeAgent"
    },
    "stage": {
        "name": "Product"
    },
    "deployment": {
        "id": "20160629000007",
        "type": "Full-Deployment",
        "systemRoot": "/Change"
    },
    "packages": {
    },
    "configs": {
    },
    "envs": {
    },
    "localOverrides": [
    ]
}
        '''

        deployTemplateJson = json.loads(deployTemplateJsonStr)
        settings = LocalDeploymentSettings.LocalDeploymentSettings()
        proxyaddr, port = settings.getProxy()
        packages, envs = self._getAgentVersion(proxyaddr, port)
        if packages is None or len(packages) == 0:
            print 'Cloud not get package from %s:%s, exit.' % (proxyaddr, port)
            sys.exit(1)
        for p in packages:
            pp = {}
            pp[os.path.basename(p)] = {'source': p}
            deployTemplateJson['packages'].update(pp)
        deployTemplateJson['envs'].update(envs)

        # 更新deployment属性
        deployTemplateJson['deployment']['id'] = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        deployTemplateJson['deployment']['systemRoot'] = settings.getSystemRoot()

        # 更新envs
        proxyHost, proxyPort = settings.getProxy()
        if proxyHost is not None and proxyPort is not None:
            deployTemplateJson['envs']['PROXY_HOST'] = proxyHost
            deployTemplateJson['envs']['PROXY_PORT'] = proxyPort
        token = settings.getToken()
        if token is not None:
            deployTemplateJson['envs']['TOKEN'] = token
        hostgroup = settings.getHostGroup()
        if hostgroup is not None:
            deployTemplateJson['envs']['HOSTGROUP'] = hostgroup

        # 模板写入到临时文件，执行部署
        templateFile = os.path.join(settings.getSystemRoot(), 'bootstrap-%s.json' % uuid.uuid1().hex)
        with open(templateFile, 'w+') as fp:
            fp.write(json.dumps(deployTemplateJson, sort_keys=True, indent=4, separators=(',', ': ')))
        cmd = 'ccl deploy -f %s' % templateFile
        p = subprocess.Popen(cmd, shell=True)
        p.communicate()
        if p.returncode == 0:
            print 'bootstrap succeed'
        else:
            print 'bootstrap failure'

        return p.returncode

    def _getAgentVersion(self, proxyaddr, port):
        url = 'http://%s:%s/rest/change/proxy/v1/agent-version' % (proxyaddr, str(port))
        r = requests.get(url)
        if r.status_code == 200:
            rjson = r.json()
            return rjson['packages'], rjson['envs']
        else:
            return None, None

    def deploy(self, args):
        return LocalDeployment.main(args)

    def settings(self, args):
        return LocalDeploymentSettings.main(args)


def main():
    # parser = argparse.ArgumentParser(description='nvwa command line.')
    # parser.add_argument('bootstrap', '--bootstrap', action='store_true', dest='bootstrap', help="bootstrap nvwa agent")
    # parser.add_argument('deploy', '--deploy', action='store_true', dest='deploy', help="deploy an environment")
    # parser.add_argument('config', '--config', action='store_true', dest='config', help="nvwa configs")

    args = sys.argv[1:]
    if len(args) == 0:
        print "Change command line tools."
        print "%s [bootstrap]|[deploy]|[config]" % os.path.basename(sys.argv[0])
        sys.exit(1)

    subcommand = args[0]
    if subcommand != "bootstrap" and subcommand != "deploy" and subcommand != "config":
        print "Change command line tools."
        print "%s [bootstrap]|[deploy]|[config]" % sys.argv[0]
        sys.exit(1)

    # knowArgs, leftArgs = parser.parse_known_args(sys.argv[1:])
    # bootstrap = knowArgs.bootstrap
    # deploy = knowArgs.deploy
    # settings = knowArgs.settings

    leftArgs = sys.argv[2:]
    change = ChangeFacade()
    exitcode = 0
    if "bootstrap" == subcommand:
        exitcode = change.bootstrap(leftArgs)
    elif "deploy" == subcommand:
        exitcode = change.deploy(leftArgs)
    elif "config" == subcommand:
        exitcode = change.settings(leftArgs)
    else:
        exitcode = 1
    return exitcode
if __name__ == '__main__':
    try:
        exitcode = main()
    except:
        exitcode = 255
    sys.exit(exitcode)

