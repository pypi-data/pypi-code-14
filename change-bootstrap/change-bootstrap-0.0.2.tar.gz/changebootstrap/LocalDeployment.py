#!/usr/bin/env python
# coding=utf8

import os
import sys
import time
import logging
import subprocess
import shutil
import argparse
import stat
import json
import re
import urllib

import LocalDeploymentSettings


class LocalDeployment(object):

    def __init__(self, systemroot, localRepoPath, deployId, envAlias, packages, configs=None, envs=None, logger=None):
        self.PKG_REPO_PATH = localRepoPath
        SYSTEM_ROOT = systemroot
        self.DEPLOY_PKG_PATH = "%s/packages" % SYSTEM_ROOT
        self.DEPLOY_ROOT = "%s/_envs" % SYSTEM_ROOT
        self.EVN_ROOT = "%s/envs" % SYSTEM_ROOT
        self.VAR_LOG_ROOT = "%s/var/log" % SYSTEM_ROOT
        self.VAR_SHARE_ROOT = "%s/var/share" % SYSTEM_ROOT

        if not os.path.isdir(SYSTEM_ROOT):
            print('System root "%s" does not exists' % SYSTEM_ROOT)
            raise Exception('SYSTEM_ROOT: %s does not exists' % SYSTEM_ROOT)
        if not os.path.isdir(self.PKG_REPO_PATH):
            os.makedirs(self.PKG_REPO_PATH)
        if not os.path.isdir(self.DEPLOY_PKG_PATH):
            os.makedirs(self.DEPLOY_PKG_PATH)
        if not os.path.isdir(self.DEPLOY_ROOT):
            os.makedirs(self.DEPLOY_ROOT)
        if not os.path.isdir(self.EVN_ROOT):
            os.makedirs(self.EVN_ROOT)
        if not os.path.isdir(self.VAR_LOG_ROOT):
            os.makedirs(self.VAR_LOG_ROOT)
        if not os.path.isdir(self.VAR_SHARE_ROOT):
            os.makedirs(self.VAR_SHARE_ROOT)

        self.envAlias = envAlias
        # 本地仓库的包名称，不需要绝对路径
        self.packages = packages
        self.deployId = deployId
        self.deployEnvPath = os.path.join(self.DEPLOY_ROOT, self.envAlias)
        self.currentDeployPath = os.path.join(self.deployEnvPath, self.deployId)
        self.currentEnvPath = os.path.join(self.EVN_ROOT, self.envAlias)

        self.configs = None
        if configs is not None:
            if type(configs) is dict:
                self.configs = configs
            else:
                self.configs = json.loads(configs)

        self.envs = None
        if envs is not None:
            if type(envs) is dict:
                self.envs = envs
            else:
                self.envs = json.loads(envs)

        self.logger = logger
        if self.logger is None:
            self.logger = logging.getLogger('LocalDeployment')
            self.logger.addHandler(logging.StreamHandler())
            self.logger.setLevel(logging.INFO)

    def downloadPackages(self):
        downloaded = []
        for k, v in self.packages.iteritems():
            repoClient = PackageRepoClient(self.PKG_REPO_PATH, v)
            succeed = repoClient.download()
            if succeed:
                downloaded.append(repoClient.getLocalFilePath())
            else:
                print 'download package [%s] failure' % v['source']
                return False, None
        return True, downloaded

    # 下载软件包，解压软件包，创建目录，创建链接
    def preStage(self, packages):
        packageFiles = {}
        for p in packages:
            if not os.path.isfile(p):
                self.logger.error('package %s does not exist, abort deployment', p)
                return False
        unzipPackagePath = []
        for packageFile in packages:
            unzipPath = os.path.join(self.DEPLOY_PKG_PATH, os.path.basename(packageFile).split('.zip')[0])
            unzipPackagePath.append(unzipPath)
            if os.path.isdir(unzipPath):
                self.logger.info('package %s already unzipped', unzipPath)
                continue
            succeed = self._unzipPackage(packageFile, unzipPath)
            if not succeed:
                return False

        if not os.path.isdir(self.deployEnvPath):
            os.makedirs(self.deployEnvPath)
        if not os.path.isdir(self.currentDeployPath):
            os.makedirs(self.currentDeployPath)
        # create link
        for path in unzipPackagePath:
            cmd = 'rsync -apl --link-dest=%s/ %s/ %s' % (path, path, self.currentDeployPath)
            self.logger.info('create hard link by command: %s', cmd)
            p = subprocess.Popen(cmd, shell=True)
            p.communicate()
            self.logger.info('run hard link command %s with exit code: %s', cmd, p.returncode)
            if p.returncode != 0:
                return False

        # create direcotries
        if not os.path.isdir(os.path.join(self.VAR_LOG_ROOT, self.envAlias)):
            os.makedirs(os.path.join(self.VAR_LOG_ROOT, self.envAlias))
        if not os.path.isdir(os.path.join(self.VAR_SHARE_ROOT, self.envAlias)):
            os.makedirs(os.path.join(self.VAR_SHARE_ROOT, self.envAlias))
        return True

    def _unzipPackage(self, packageFile, unzipPath):
        cmd = ''
        if packageFile.endswith('.zip'):
            cmd = 'unzip -d %s %s' % (unzipPath, packageFile)
        elif packageFile.endswith('.rpm'):
            cmd = 'rpm -i --prefix=%s %s' % (unzipPath, packageFile)
        elif packageFile.endswith('.tar.gz'):
            cmd = 'tar zxf %s -C %s' % (packageFile, unzipPath)
        else:
            self.logger.info('%s is unsupported package file types', packageFile)
            return False
        self.logger.info('unzip file by command: %s', cmd)
        p = subprocess.Popen(cmd, shell=True)
        p.communicate()
        self.logger.info('install package with command %s and exit code: %s', cmd, p.returncode)
        if p.returncode != 0:
            return False
        return True

    # 生成部署文件
    def deploy(self):
        deployEnvFile = os.path.join(self.currentDeployPath, 'change-output/envs.properties')
        deployConfigFile = os.path.join(self.currentDeployPath, 'change-output/configs.properties')

        # 设置目录
        parent = os.path.dirname(deployEnvFile)
        if not os.path.isdir(parent):
            print 'setup path %s' % parent
            os.makedirs(parent)

        # 文件已经存在则不处理
        if os.path.isfile(deployEnvFile):
            self.logger.info('env file: %s already exist', deployEnvFile)
        baseenvs = {}
        baseenvs['APP_ROOT'] = self.currentDeployPath
        baseenvs['APP_LOG_PATH'] = os.path.join(self.VAR_LOG_ROOT, self.envAlias)
        baseenvs['APP_SHARE_PATH'] = os.path.join(self.VAR_SHARE_ROOT, self.envAlias)

        # 追加用户定义的环境变量
        envs = {}
        envs.update(baseenvs)
        if self.envs is not None:
            envs.update(self.envs)

        self.logger.info('write env file: %s', deployEnvFile)
        with open(deployEnvFile, 'w+') as fp:
            for k, v in envs.iteritems():
                fp.write('%s=%s' % (k, v))
                fp.write('\n')

        # 写configs
        configs = {}
        configs.update(baseenvs)
        if self.configs is not None:
            configs.update(self.configs)
        self.logger.info('write configs file: %s', deployConfigFile)
        with open(deployConfigFile, 'w+') as fp:
            for k, v in envs.iteritems():
                fp.write('%s=%s' % (k, v))
                fp.write('\n')

        return True

    # 切换到新部署
    def flip(self):
        if os.path.islink(self.currentEnvPath):
            os.unlink(self.currentEnvPath)
        elif os.path.isdir(self.currentEnvPath):
            shutil.rmtree(self.currentEnvPath)
        os.symlink(self.currentDeployPath, self.currentEnvPath)
        self.logger.info('symbol link %s to source %s', self.currentDeployPath, self.currentEnvPath)
        return True

    def preactivate(self):
        return self._executeScript('preactivate') == 0

    # 执行服务的activate脚本
    def activate(self):
        return self._executeScript('activate') == 0

    def postactivate(self):
        return self._executeScript('postactivate') == 0

    def predeactivate(self):
        return self._executeScript('predeactivate') == 0

    # 执行服务的 deactivate脚本
    def deactivate(self):
        return self._executeScript('deactivate') == 0

    def postdeactivate(self):
        return self._executeScript('postdeactivate') == 0

    def _executeScript(self, command):
        scriptPath = os.path.join(self.currentEnvPath, 'change-commands', command)
        if not os.path.isdir(scriptPath):
            self.logger.info('no %s scripts', command)
            return 0
        f = lambda script: os.path.join(scriptPath, script)
        scripts = [f(script) for script in os.listdir(scriptPath) if os.path.isfile(f(script)) and script.endswith('.sh')]
        self.logger.info('execute %s scripts', command)
        for script in scripts:
            self.logger.info('execute %s', script)
            st = os.stat(script)
            os.chmod(script, st.st_mode | stat.S_IEXEC)
            p = subprocess.Popen(script, shell=True)
            p.communicate()
            self.logger.info('execute %s script with exit code: %s', command, p.returncode)
            if p.returncode != 0:
                return p.returncode

        return 0


class DeploymentTemplate:
    def __init__(self, jsonObject):
        self._template = jsonObject

    def getPackages(self):
        return self._template.get('packages')

    def getConfigs(self):
        return self._template.get('configs')

    def getEnvs(self):
        return self._template.get('envs')

    def getEnvironmentName(self):
        env = self._template.get('environment')
        if not env:
            return None
        return env.get('name')

    def getEnvironmentAlias(self):
        env = self._template.get('environment')
        if not env:
            return None
        return env.get('alias')

    def getDeploymentId(self):
        deployment = self._template.get('deployment')
        if not deployment:
            return None
        return deployment.get('id')

    def getDeploymentType(self):
        deployment = self._template.get('deployment')
        if not deployment:
            return None
        return deployment.get('type')

    def getSystemRoot(self):
        deployment = self._template.get('deployment')
        if not deployment:
            return None
        return deployment.get('systemRoot')


class PackageRepoClient:
    def __init__(self, localRepoPath, packageJson):
        self.localRepoPath = localRepoPath
        self.source = packageJson['source']
        self.protocol, _, self.resource = self._parse(self.source)
        if 'file' == self.protocol:
            self.localFilePath = self.resource
        else:
            i = self.resource.rfind('/')
            self.localFilePath = os.path.join(self.localRepoPath, self.resource[i+1:])

    def _parse(self, source):
        pattern = '(file|http|https)(://)(.*)'
        m = re.search(pattern, source)
        groups = m.groups()
        return groups

    def download(self):
        if 'file' == self.protocol:
            return True
        elif 'http' == self.protocol:
            filename, headers = urllib.urlretrieve(self.source, self.localFilePath)
        elif 'https' == self.protocol:
            filename, headers = urllib.urlretrieve(self.source, self.localFilePath)
        else:
            print 'unsupported protocol [%s] for download packages' % self.protocol
            return False
        return True

    def getLocalFilePath(self):
        return self.localFilePath


def main(args):
    parser = argparse.ArgumentParser(prog='ccl deploy', description='Change deployment utilities.')
    parser.add_argument('-n', '--envname', dest='envname', help="Environment name")
    parser.add_argument('-a', '--alias', dest='alias', help="Environment alias (treated as local unzip parent path)")
    parser.add_argument('-p', '--packages', dest='packages', help="Packages for deployment")
    parser.add_argument('-c', '--configs', dest='configs', help="Configurations for deployment")
    parser.add_argument('-e', '--envs', dest='envs', help="Environment for deployment")
    parser.add_argument('-t', '--type', dest='type', help="Deployment types: Pre-Stage, Full-Deployment, Manully-Activate, Activate, Deactivate")
    parser.add_argument('-f', '--file', dest='template', help="Deployment template file")
    #parser.add_argument('-h', '--help', dest='help', action='store_true', help="Print the usage")

    knowArgs = parser.parse_args(args)
    #if args.help:
    #    parser.print_usage()
    #    sys.exit(0)

    template = knowArgs.template
    systemroot = None
    deployId = None
    envname = None
    alias = None
    packages = None
    configs = None
    envs = None
    deployType = None
    if template:
        if not os.path.isfile(template):
            print('Deployment template file %s does not exist' % template)
            return 10
        templateObject = None
        with open(template, 'rb') as fp:
            templateObject = json.loads(fp.read())
        if not templateObject:
            print('Deployment template file %s is not valid json file' % template)
            return 20
        templateObject = DeploymentTemplate(templateObject)
        envname = templateObject.getEnvironmentName()
        alias = templateObject.getEnvironmentAlias()
        packages = templateObject.getPackages()
        configs = templateObject.getConfigs()
        envs = templateObject.getEnvs()
        systemroot = templateObject.getSystemRoot()
        deployId = templateObject.getDeploymentId()
        deployType = templateObject.getDeploymentType()
    else:
        envname = knowArgs.envname
        # alias 是本地部署解压的父目录
        alias = knowArgs.alias
        packages = knowArgs.packages
        configs = knowArgs.configs
        envs = knowArgs.envs
        deployType = knowArgs.type

    if not deployType:
        # 默认是 Faull-Deployment
        deployType = 'Full-Deployment'

    if deployType.upper() in ['Full-Deployment'.upper(), 'Pre-Stage'.upper(), 'Manully-Activate'.upper()]:
        if not envname or not alias or not packages:
            parser.print_usage()
            return 30
    if deployType.upper() in ['Activate'.upper(), 'Deactivate'.upper()]:
        if not envname or not alias:
            parser.print_usage()
            return 30

    # 优先使用模板中的systemroot，如果模板中没有指定，则用settings中的
    settings = LocalDeploymentSettings.LocalDeploymentSettings()
    if not systemroot:
        systemroot = settings.getSystemRoot()
        # settings.setSystemRoot(systemroot)
    localRepoPath = os.path.join(systemroot, 'local_package_repo')
    if not deployId:
        deployId = str(int(round(time.time() * 1000)))

    # 不同的部署类型: Pre-Stage, Full-Deployment, Manully-Activate, Activate, Deactivate
    deployment = LocalDeployment(systemroot, localRepoPath, deployId, alias, packages, configs, envs)
    if deployType.upper() == 'Full-Deployment'.upper():
        succeed, downloaded = deployment.downloadPackages()
        if not succeed:
            return 1
        succeed = deployment.preStage(downloaded) and \
        deployment.deploy() and \
        deployment.flip() and \
        deployment.preactivate() and \
        deployment.activate() and \
        deployment.postactivate()
        if succeed:
            return 0
        else:
            return 1
    elif deployType.upper() == 'Pre-Stage'.upper():
        succeed, downloaded = deployment.downloadPackages()
        if not succeed:
            return 1
        succeed = deployment.preStage(downloaded)
        if succeed:
            return 0
        else:
            return 1
    elif deployType.upper() == 'Manully-Activate'.upper():
        succeed, downloaded = deployment.downloadPackages()
        if not succeed:
            return 1
        succeed = deployment.preStage(downloaded) and \
        deployment.deploy() and \
        deployment.flip()
        if succeed:
            return 0
        else:
            return 1
    elif deployType.upper() == 'Activate'.upper():
        succeed = deployment.preactivate() and \
        deployment.activate() and \
        deployment.postactivate()
        if succeed:
            return 0
        else:
            return 1
    elif deployType.upper() == 'Deactivate'.upper():
        succeed = deployment.predeactivate() and \
        deployment.deactivate() and \
        deployment.postdeactivate()
        if succeed:
            return 0
        else:
            return 1
        return 0
    else:
        print 'Unknown deployment type: %s' % deployType
        return 40


if __name__ == '__main__':
    exitcode = main(sys.argv[1:])
    sys.exit(exitcode)
