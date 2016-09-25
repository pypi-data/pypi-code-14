#!/usr/bin/env python
# coding=utf8

# 本地部署的设置工具，设置本地部署时候参数，如系统根目录，日志目录等

import os
import sys
import json
import argparse

SYSTEM_ROOT = os.path.join(os.path.expanduser('~'), 'change')


class LocalDeploymentSettings:
    def __init__(self):
        # 设置文件写到user home目录下
        self._settingPath = SYSTEM_ROOT
        if not os.path.isdir(self._settingPath):
            os.makedirs(self._settingPath)
        self._settingFile = os.path.join(self._settingPath, 'settings.json')

        self._settings = {}
        if os.path.isfile(self._settingFile):
            with open(self._settingFile, 'rb') as fp:
                jsonStr = fp.read()
                self._settings = json.loads(jsonStr)

        # 设置默认值
        if not self._settings.get('system.root'):
            self._settings['system.root'] = SYSTEM_ROOT

    def getSystemRoot(self):
        return self.getSettings('system.root')

    def getProxy(self):
        return self.getSettings('proxy'), 3000

    def getRegion(self):
        return self.getSettings('region')

    def getToken(self):
        return self.getSettings('token')

    def getHostGroup(self):
        return self.getSettings('hostgroup')

    def setSystemRoot(self, systemroot):
        self.applySettings('system.root', systemroot)

    def getLocalPackageRepoPath(self):
        return os.path.join(self.getSystemRoot(), 'local_package_repo')

    def applySettings(self, key, value):
        self._settings[key] = value
        self._storeJson2File(self._settingFile, self._settings)

    def getSettings(self, key, default=''):
        return self._settings.get(key, default)

    def _storeJson2File(self, filepath, jsonObject):
        with open(filepath, 'w+') as fp:
            fp.write(json.dumps(jsonObject, sort_keys=True, indent=4, separators=(',', ': ')))

    def printSettings(self):
        print('Change settings:')
        for k, v in self._settings.iteritems():
            print('%s=%s' % (k, v))


def main(args):
    parser = argparse.ArgumentParser(prog='ccl config', description='Change config tool.')
    parser.add_argument('-p', '--print', dest='p', action="store_true", help="Print current configs")
    parser.add_argument('-sysroot', '--system.root', dest='root', help="System root path for deployment")
    parser.add_argument('-proxy', '--proxy', dest='proxy', help="Proxy address")
    parser.add_argument('-region', '--region', dest='region', help="Region name")
    parser.add_argument('-t', '--token', dest='token', help="Token for auth")
    parser.add_argument('-G', '--hostgroup', dest='hostgroup', help="Host group")
    knowArgs = parser.parse_args(args)

    p = knowArgs.p
    sysroot = knowArgs.root
    proxy = knowArgs.proxy
    region = knowArgs.region
    token = knowArgs.token
    hostgroup = knowArgs.hostgroup

    if not p and not sysroot and not proxy and not region and not token and not hostgroup:
        parser.print_usage()
        sys.exit(1)

    settings = LocalDeploymentSettings()

    if p:
        # 打印所有设置
        settings.printSettings()
    else:
        if sysroot is not None:
            settings.applySettings('system.root', sysroot)
        if proxy is not None:
            settings.applySettings('proxy', proxy)
        if region is not None:
            settings.applySettings('region', region)
        if token is not None:
            settings.applySettings('token', token)
        if hostgroup is not None:
            settings.applySettings('hostgroup', hostgroup)

if __name__ == '__main__':
    main(sys.argv[1:])
