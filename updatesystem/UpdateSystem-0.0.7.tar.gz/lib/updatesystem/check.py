
# -*- coding: UTF-8 -*-
import os
import sys
import subprocess
import ssl
import urllib2
#import traceback
import shlex
import configparser
reload(sys)
sys.setdefaultencoding('utf-8')

from log import logger as logging
import socket
import fcntl
import struct


class Checker(object):
    # monkey patch
    if hasattr(ssl,"_create_default_https_context"):
        ssl._create_default_https_context = ssl._create_unverified_context

    installed_patch_list = []
    
    
    section_name = "check"
    
    config_check_default = {
        #"version" :   "2.0.36053.20160811R",
        "version" :   "2.0.35757.20160622R",
        "rabbitmq" : "rabbitmq-server-3.3.5-16.el7.noarch",
        "redis" : "redis-2.8.19-2.el7.x86_64",
        "mariadb"  : "mariadb-server-5.5.44-2.el7.centos.x86_64",
        "tomcat": "/usr/local/apache-tomcat-8.0.32/", 
    }
    def __init__(self,patch_path="/home/update/02-bugfix/",cm_ip=None):
        self.patch_path = patch_path
        self.version_file="/usr/local/apache-tomcat-8.0.32/webapps/ROOT/WEB-INF/classes/version.properties"
        self._config = configparser.get_config(section_name=self.section_name,config_default=self.config_check_default)
        if cm_ip is None:
            self.cm_ip = self.get_cm_ip()
        else:
            self.cm_ip = cm_ip
        logging.debug(self._config)
    
    def get_cm_ip(self,ifname="eno16777984"):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(
            s.fileno(),
            0x8915,  # SIOCGIFADDR
            struct.pack('256s', ifname[:15])
        )[20:24])
    
    def check_cmd_match_result(self,cmd, expect_output, success_str=None,
            failed_str=None):
        """
        """
        cmd_list = shlex.split(cmd)
        try:
            output = subprocess.check_output(cmd_list,stderr=subprocess.STDOUT)
            output = output.strip()
            logging.debug(output)
            if output == expect_output:
                return True
            else:
                logging.debug("expect:({})".format(expect_output))
                logging.debug("actual:({})".format(output))
                return False
        except subprocess.CalledProcessError,e :
            logging.debug(e.output)
            logging.debug(cmd)
            logging.debug("Exception",exc_info=True)
            return False
        except:
            logging.debug(cmd)
            logging.debug("Exception", exc_info=True)
            return False
    
    def check_cm_visit(self):
        """
        检查cm可以访问
        """
        url="https://{ip}/".format(ip=self.cm_ip)
        #url="http://10.0.33.148:8000/navi/"
        req = urllib2.Request(url)
        try:
            s = urllib2.urlopen(req)
            if s.getcode() == 200:
                #logging.info(s.info())
                logging.info("connect cm  success(code:{})".format(s.code))
                return True
            else:
                logging.error("can not connect cm (code:{})".format(s.code))
                return False
        except:
            logging.error("connect url fail({})".format(url))
            logging.debug("Execption",exc_info=True)
            return False
    
    def check_patch_md5(self,):
        """
        检查patch完整性
        """
        path = self.patch_path
        logging.info("patch path:{}".format(path))
        if not os.path.exists(path):
            logging.error("{} is not exists! ".format(path))
            return False
        try:
            os.chdir(path)
        except:
            logging.error("chdir directory {} fail".format(path))
            return False
    
        try:
            output = subprocess.check_output(["/usr/bin/md5sum", "-c",
                "./md5"],stderr=subprocess.STDOUT)
            logging.info("output:{}".format(output))
            return True
            #retcode = 0
            #if retcode != 0:
            #    logging.error("{}md5 check failed".format(path))
            #    return False
            #else:
            #    return True
        except subprocess.CalledProcessError,e :
           # for line in e.output.split("\n"):
           #     logging.error(line) 
    
            logging.debug(e.output)
            logging.debug("Exception",exc_info=True)
            logging.error("{}md5 check failed".format(path))
            return False
        except :
            #logging.exception()
            logging.debug("Exception",exc_info=True)
            logging.error("{}md5 check failed".format(path))
            return False
    
    def check_self_version(self):
        """
        """
        return True
    
    def check_service_version(self):
        """
        """
        ret = True
        cmd_dict = {
                "rabbitmq":
                {"cmd": "rpm -q rabbitmq-server" , 
                "result":"rabbitmq-server-3.3.5-16.el7.noarch",},
                "redis":
                {"cmd": "rpm -q redis",
                "result":"redis-2.8.19-2.el7.x86_64",},
                "mariadb":
                {"cmd":"rpm -q mariadb-server" ,
                "result":"mariadb-server-5.5.44-2.el7.centos.x86_64",},
                "tomcat":
                {"cmd":"ls -d /usr/local/apache-tomcat-8.0.32/",
                "result":"/usr/local/apache-tomcat-8.0.32/" },
                }
        for name in cmd_dict:
            ret_status = self.check_cmd_match_result(cmd_dict[name]["cmd"],cmd_dict[name]['result'])
            if ret_status :
                logging.info( "service {}  version is right  ".format(name))
            else:
                ret = False
                logging.error( "service {} version is not match".format(name)) 
        return ret
    
    def check_service_status(self):
        """
        """
        ret = True
        service_name=["rabbitmq-server","redis","tomcat","mariadb"]
        for name in service_name:
            cmd = "service {} status".format(name)
            try:
                cmd_list = shlex.split(cmd)
                output = subprocess.check_output(cmd_list,stderr=subprocess.STDOUT)
                logging.info("{} status is OK".format(name))
                logging.debug(output)
                retcode = 0
            except subprocess.CalledProcessError, e:
                #logging.error(e.output) 
                #logging.exception("Exception")
                logging.debug(cmd)
                logging.debug("Exception",exc_info=True)
                logging.error("service {} status check failed ".format(name))
                ret = False
            except :
                logging.debug(cmd)
                logging.debug("Exception",exc_info=True)
                logging.error("service {} may be not exists".format(name))
                ret = False
        return ret
    
    
    def check_cm_version(self,):
        version_file=self.version_file
        expect_version = self._config['version']

        try:
            with open(version_file,"r") as f:
                line=f.read()
                version=line.strip().split("=")[1]
                logging.info(version)
                if version == expect_version:
                    return True
                else:
                    logging.error("cm version {} not match.(expect {})"\
                            .format(version, expect_version))
                    return False
        except:
            logging.debug("Exception",exc_info=True)
            logging.error("open version file {} failed ".format(version_file)) 
            return False
    
    
    
    def check_cm_patch_status(self):
        """
        """
        installed_patch_list = []
        if not os.path.exists("/usr/local/cm"):
            return installed_patch_list
        try:
            os.chdir("/usr/local/cm")
            output = subprocess.check_output("ls")
            installed_patch_list = output.strip().split("\n")
        except:
            logging.debug("",exc_info=True)
        return installed_patch_list
    
    
    def check_cm_file_status(self):
        return True
    
    def check_cm_task_running(self):
        url = "https://{}/task/getRunningTaskNum".format(self.cm_ip)
        req = urllib2.Request(url)
        try:
            s = urllib2.urlopen(req)
            info = s.read()
            if info == "0":
                logging.info("running task:{}".format(info))
                return True
            elif len(info) > 50 :
                logging.debug("running task info:{}".format(info))
                logging.debug("running task get wrong info:{}".format(info[:20]))
                return True
            else:
                logging.error("running task:{}".format(info))
                return False
        except:
            logging.error("connect url fail ({})".format(url))
            logging.debug("Execption",exc_info=True)
            return False

    
    def check_cm_online_people(self):
        url = "https://{}/userMgmt/getOnlineUserNum".format(self.cm_ip)
        req = urllib2.Request(url)
        try:
            s = urllib2.urlopen(req)
            info = s.read()
            if info == "0":
                logging.info("online people:{}".format(info))
                return True
            elif len(info) > 50:
                logging.debug("online people info:{}".format(info))
                logging.debug("oneline people get wrong info:{}".format(info[:20]))
                return True
            else:
                logging.error("online people:{}".format(info))
                return False
        except:
            logging.error("connect url fail({})".format(url))
            logging.debug("Execption",exc_info=True)
            return False
    
    def check_system_space(self):
        s = os.statvfs("/")
        size = s.f_bavail * s.f_frsize
        logging.debug(" avail block {}".format(size))
        if size < 1024 * 1024:
            logging.error("remain size less than 1G")
            return False
        else:
            logging.info("system space is enough")
            return True
    
    def check_before_update(self):
        env_ok = False
        env_ok = self.check_cm_visit() 
        env_ok = self.check_patch_md5() and env_ok
        #env_ok =self.check_self_version()  and env_ok 
        env_ok = self.check_service_version() and   env_ok 
        env_ok = self.check_service_status()  and env_ok 
        env_ok = self.check_cm_version() and  env_ok 
        installed_patch_list = self.check_cm_patch_status()  and env_ok 
        #env_ok = self.check_cm_file_status() and env_ok 
        env_ok = self.check_cm_task_running()  and env_ok 
        env_ok = self.check_cm_online_people() and  env_ok 
        env_ok = self.check_system_space() and  env_ok 
        if env_ok:
            logging.info("check enviroment: OK")
            return True
        else:
            logging.error("check enviroment: Fail")
            return False
    
    def check_after_update(self):
        env_ok = self.check_service_status() 
        env_ok = self.check_cm_visit() and env_ok 
        if env_ok:
            logging.info("check enviroment: OK")
            return True
        else:
            logging.error("check enviroment: Fail")
            return False

if __name__ == "__main__":
    ck = Checker(cm_ip="10.0.36.216")
    ck.check_before_update()
