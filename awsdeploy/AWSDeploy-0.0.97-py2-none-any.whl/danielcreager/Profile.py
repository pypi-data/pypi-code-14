__all__ = ['Profile']
'''
Copyright 2016 Daniel Ross Creager

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

#------------------------------------------------------------------------------#
# Class:    Profile.py
# Written:  November 2016
# Author:   Daniel R Creager
# Desc:     Supports user, application, and AWS Account customization 
#
# Input:    profile.ini 
#------------------------------------------------------------------------------#
'''
import ConfigParser, os, sys, time, re
class Profile(object):
    '''
    Profile for an AWS Code Deployment 
    '''
    def __init__(self, configFilePath):
        '''
        Constructor
        '''
        self.profilePath        = lambda arg: self.path + "\\" + arg
        self.configFilePath = configFilePath
        self.config = ConfigParser.ConfigParser()
        self.config.read(self.configFilePath)
        self.config.sections() 

        section                  = self.configSectionMap("Source")
        if ((type(section) != type(None)) and (len(section) > 0)):
            self.path            = section['path']
            self.file_name       = time.strftime("DeploymentPackage.%Y%m%d.zip")
            self.tomcat_config   = section['tomcat_config'].replace('\\','/').replace('/','')  #: conf
            self.tomcat_content  = section['tomcat_content'].replace('\\','/').replace('/','') #: webapps
            self.apache_config   = section['apache_config'].replace('\\','/').replace('/','')  #: conf.d
            self.apache_content  = section['apache_content'].replace('\\','/').replace('/','') #: html
            self.deploy_hooks    = section['deploy_hooks'].replace('\\','/').replace('/','')   #: scripts
            
        section                  = self.configSectionMap("CodeDeploy")
        if ((type(section) != type(None)) and (len(section) > 0)):
            self.dst_path        = section['dst_path']
            self.region          = section['region']
            self.bucket_regex    = section['bucket_regex']
            self.profile         = section['profile']
            self.log_group_name  = section['log_group_name']
            self.log_stream_name = section['log_stream_name']
            
        section                  = self.configSectionMap("Runtime")
        if ((type(section) != type(None)) and (len(section) > 0)):
            self.working_dir     = section['working_dir']
            self.log_max_lines   = section['log_max_lines']
            
            self.sleepInterval   = self.config.getint("Runtime","sleepInterval")   # Seconds
            self.blocking        = self.config.getboolean("Runtime","blocking")
            self.logging         = self.config.getboolean("Runtime","logging")
            self.rewriteAppSpec = self.config.getboolean("Runtime","rewriteAppSpec")
            self.verbose         = self.config.getboolean("Runtime","verbose") 
    
        self.renameSec           = self.configSectionMap("Rename")

        '''
        Validate the names of directories
        '''
        msg="Directory mapping(%s) is inconsistent."
        if  not os.path.exists(self.profilePath(self.tomcat_config)):
            raise Warning(msg % ('tomcat_config'))
         
        if  not os.path.exists(self.profilePath(self.tomcat_content)):
            raise Warning(msg % ('tomcat_content'))
         
        if  not os.path.exists(self.profilePath(self.apache_config)):
            raise Warning(msg % ('apache_config'))
         
        if  not os.path.exists(self.profilePath(self.apache_content)):
            raise Warning(msg % ('apache_content'))
         
        if  not os.path.exists(self.profilePath(self.deploy_hooks)):
            raise Warning(msg % ('deploy_hooks'))
  
    def configSectionMap(self,section):
        results = {}
        try:
            for option in self.config.options(section):
                try:
                    results[option] = self.config.get(section, option)
                    if results[option] == -1:
                        print("skip: %s" % option)
                except:
                    print("exception on %s!" % option)
                    results[option] = None

        except ConfigParser.NoSectionError as ex1:
            if section != 'Rename':
                print "Abnormal Termination because %s" % (ex1)
                sys.exit(-1)
            
        return results
    
    def rename(self, arg):
        if ((type(self.renameSec) != type(None)) and (len(self.renameSec) > 0)):
            #
            # Check each rename within the profile.ini
            #
            for itm in self.renameSec.items():
                arg = re.sub(itm[0],itm[1],arg)
        return arg  
    
if __name__ == "__main__": 
    pfl = Profile(sys.argv[1]) 
        