__all__ = ['AWSToolBox']
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



@author: Daniel R Creager
Created on Nov 1, 2016
'''
import os, sys
from time import sleep
from com.danielcreager.Profile import Profile
from com.danielcreager.AmazonWebSrvc import AWSToolBox
from com.danielcreager.AmazonWebSrvc import AppSpecFactory


# type(s3Obj) == <class 'boto3.resources.factory.s3.Object'>
# type(resp) ==  <type  'dict'>


class ToolBox(object):
    '''
    A collection of tools for using AWS CodeDeploy in Python.
    '''
    def __init__(self,profile):
        '''
        Constructor
        '''
        self.profile = profile 
        self.tb   = AWSToolBox(profile)
        self.s3Obj = None
        self.isSuccess = lambda rsp: (('Error' in rsp.keys()) == False)
        self.isFailure = lambda rsp: (('Error' in rsp.keys()) == True )
        
    # Download the deployment package 
    def downloadPkg(self):
        '''
        '''
        print "Downloading %s" % (self.profile.working_dir + self.profile.file_name)
        self.tb.download(self.profile.profile, self.profile.region, self.profile.bucket_reqex, 
                     self.profile.working_dir, self.profile.file_name)
      
    def makePkg(self):
        '''
        Construct a deployment package.
        
        '''
        
        #------------------------------------------------------------------------------#
        # OnAppSpecMissing: Dynamically generate one 
        #------------------------------------------------------------------------------#
        filePath = self.profile.path + '/appspec.yml'
        
        # if indicated delete the appspec.yml and regenerate every time.
        if self.profile.rewriteAppSpec == True:
            if os.path.exists(filePath):
                print "%s Removing %s" % (self.tb.currTimeStamp(),filePath)
                os.remove(filePath)

        
        if os.path.exists(filePath) == False:
            f = AppSpecFactory(self.profile)
            f.persist(filePath,f.instanceOf())
            print "%s Generated Application Spec: %s" % (self.tb.currTimeStamp(),filePath)
        
        #------------------------------------------------------------------------------#
        # Prepare the Deployment Package 
        #------------------------------------------------------------------------------#         
        self.tb.create(self.profile.path,self.profile.working_dir,self.profile.file_name)
    
        #------------------------------------------------------------------------------#
        # Transfer the Deployment Package to AWS 
        #------------------------------------------------------------------------------#
        self.s3Obj = self.tb.upload(self.profile.profile, self.profile.region, self.profile.bucket_regex, 
                                   self.profile.working_dir, self.profile.file_name)
        
        #------------------------------------------------------------------------------#
        # Remove the Deployment Package locally 
        #------------------------------------------------------------------------------#
        print "%s Removed %s" % (self.tb.currTimeStamp(),
                                 self.profile.working_dir + "/" + self.profile.file_name)
        os.remove(self.profile.working_dir + "/" + self.profile.file_name)
        return self.s3Obj
    
    def printHeader(self):
        '''
        Print  a Runtime Header.
        
        '''
        print ("Command:\tdeploy\nParameters:\t%s\nPath:\t\t%s\nPackage:\t%s\nRegion:\t\t%s\n"
               "Bucket:\t\t%s\nProfile:\t%s\nRun Date:\t%s\nRun Mode:\t%s\n\nRun Log"
            % (self.profile.configFilePath, self.profile.path, self.profile.file_name, self.profile.region, 
               self.profile.bucket_regex, self.profile.profile, self.tb.currDateStamp(),
              ("Rewrite_AppSpec" if self.profile.rewriteAppSpec else "Use_Existing_AppSpec")
            + (" Wait_for_Completion" if self.profile.blocking else "") 
            + (" Retrieve_App_Logs" if self.profile.logging else "")))
        print("%s Initiated deployment request using %s." 
               % (self.tb.currTimeStamp(),self.profile.path))
            
    def printLog(self):
        '''
        Print out the custom log entries.
        
        '''
        print "Log Entries"
        sleep(self.profile.sleepInterval) # Time is seconds
        print self.tb.getLogEvents(self.profile.log_group_name,self.profile.log_stream_name, 
              self.profile.log_max_lines,self.profile.profile, self.profile.region)
        
    def runPkg(self):
        '''
        Run the deployment package.
        
        '''
        #------------------------------------------------------------------------------#
        # Trigger Deployment of the new Package
        #------------------------------------------------------------------------------#
        resp = self.tb.deploy(self.s3Obj, self.profile.profile, 
                           self.profile.region, 'Deploy Automation')
        
        if self.isSuccess(resp) and self.profile.blocking:
            if self.tb.waitForCompletion(resp, self.profile.profile, self.profile.region):
                print("%s Deployment using %s completed successfully." 
                    % (self.tb.currTimeStamp(), self.profile.file_name)) 
            else:
                if self.profile.logging:
                    self.printLog()
                print("%s Deployment using %s terminated abnormally." 
                    % (self.tb.currTimeStamp(),self.profile.file_name))
                
        elif self.isSuccess(resp):
            print("%s Deployment request for %s submitted successfully." 
                  % (self.tb.currTimeStamp(), self.profile.file_name)) 
            
        else:
            if self.profile.logging:
                self.printLog(self.profile)
            print("%s Deployment request for %s terminated abnormally." 
                % (self.tb.currTimeStamp(),self.profile.file_name))
        return resp
    
           
if __name__ == "__main__": 
    #------------------------------------------------------------------------------#
    # Create and execute an application deployment in AWS CodeDeploy on Linux  
    #------------------------------------------------------------------------------#
    tool = ToolBox(Profile(sys.argv[1]))
    tool.printHeader();
    s3Obj = tool.makePkg()
    if s3Obj != None:        # OnS3ObjMissing: Skip further processing 
        tool.runPkg()