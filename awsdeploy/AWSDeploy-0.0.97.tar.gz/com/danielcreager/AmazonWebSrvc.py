__all__ = ['AppSpecFactory', 'AWSToolbox']
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


Class:    AppSpecFactory.py
Written:  October 2016
Author:   Daniel R Creager
Desc:     Generate a CodeDeploy Application Specification (appspec.yml) 
'''

from os import walk
from com.danielcreager.Profile import Profile
import boto3, botocore, datetime, re, os, sys, time, zipfile

class AppSpecFactory(object):
    '''
    Generate a CodeDeploy Application Specification (appspec.yml).
    
    The application specifications produced by this class are based upon specific 
    implied meanings of directory names within the deployment package. 
    
    Directory (Default Setup)
       /          = files to copy into the 'home' directory  
       script     = scripts to execute during the 'afterInstall' phase
       conf.d     = Apache configuration files
       html       = Apache Static Content
       conf       = Tomcat configuration files
       webapps    = Tomcat applications
    
    Methods
    instanceOf(src, verbose)
               src      = The directory which holds the deployment package 
                         default = 'C:/Users/Z8364A/Downloads/JavaStack'
                     
               verbose  = True = Generate an individual copy operation for each file
                          False = (default) Generate fewer directory level copy operations
                           
    persist(dst, specStr) 
               dst     = The location in which to place the appspec.yml file
               specStr = application specification string          
    '''

    def __init__(self, profile):
        self.current_time  = lambda: long(round(time.time() * 1000))
        self.currTimeStamp = lambda : self.getTimeStamp(self.current_time())
        self.getTemplate   = lambda: {'version': 0.0, 'os': 'linux', 'files': [], 'permissions': [], 'hooks': []}
        self.getDay        = lambda millis: datetime.datetime.fromtimestamp(millis / 1000.0).strftime('%d')
        self.getDateStamp  = lambda millis: datetime.datetime.fromtimestamp(millis / 1000.0).strftime('%Y-%m-%d')
        self.getTimeStamp  = lambda millis: datetime.datetime.fromtimestamp(millis / 1000.0).strftime('%H:%M:%S.%f')[0:12]+'   '
        self.profile       = profile
        self.indent        = '  ';
        
        self.stdPath       = lambda arg: arg.replace("\\\\","\\").replace("\\","/")
        self.absPath       = lambda arg: self.stdPath(profile.path + "\\" +arg)
        self.relPath       = lambda arg: '.\\' + arg + '\\'
        self.relDstPath    = lambda arg: arg + "/" 
        
    def dump(self, specStr, f):
        if specStr.has_key('version'):
            f.write("version: %s\n" % (specStr['version'])) 
            f.write("os: %s\n" % (specStr['os']))
        
        if specStr.has_key('files'):
            f.write("files:\n")
            for itm in specStr['files']:
                self.dumpNode(itm.items(), 1, f)
         
        if specStr.has_key('permissions'):
            f.write("permissions:\n")
            for itm in specStr['permissions']:
                self.dumpPermission(itm.items(), 1, f)
        
        if specStr.has_key('hooks'):
            # Write the AfterInstall Hook
            f.write("hooks:\n  AfterInstall:\n")
            try:
                if len(specStr['hooks']) > 0:
                    for itm in specStr['hooks']:
                        self.dumpNode(itm.items(), 2, f)
                    
            except TypeError as ex1:
                print("AmazonWebSrvc::dump TypeError. "), ex1
            
    def dumpNode(self, items, indCnt, f):
        dlmtr = '-'
        for itm in items:
            if type(itm[1]) == type(dict()):
                f.write("%s%s %s:\n%s%s: %s\n" % (indCnt*self.indent, dlmtr, itm[0], indCnt*3*self.indent, 
                       itm[1].items()[0][0], itm[1].items()[0][1]))
            else: 
                f.write("%s%s %s: %s\n" % (indCnt*self.indent, dlmtr, itm[0], itm[1]))
            dlmtr = ' '
       
    def dumpPermission(self, items, indCnt, f):
        for i in [2,0,3,4,1]:
            if i == 1:       # Type
                f.write("%s%s:\n%s- %s\n" % 
                       (indCnt*2*self.indent, items[i][0], indCnt*3*self.indent, items[i][1]))
            else:
                f.write("%s%s %s: %s\n" % 
                       (indCnt*self.indent, ('-' if i==2 else ' '), items[i][0], items[i][1]))

    def getFile(self, src, dst):
        return {'source': src.replace("\\","/"),'destination': dst.replace("\\","/")}
    
    def getPermission(self, obj, owner=None, group=None, mode=None, ltype=None):
        result = {'object': obj}
        if owner != None:
            result.update({'owner': owner})
        if group != None:
            result.update({'group': group})
        if mode != None:
            result.update({'mode': mode})
        if ltype != None:
            result.update({'type': ltype})
         
        return result
    
    def getHook(self, loc, timeout=None, runas=None):
        result = {'location': loc}
        if timeout != None:
            result.update({'timeout': timeout})
        if runas != None:
            result.update({'runas': runas})
        return result

    def instanceOf(self):
        tmplt = self.getTemplate();
        
        for (dirpath, dirnames, filenames) in walk(self.profile.path):
            #------------------------------------------------------------------------------#
            # Prepare the Hooks Section with Scripts to be Executed 
            #------------------------------------------------------------------------------#
            if self.stdPath(dirpath) == self.absPath(self.profile.deploy_hooks):
                after=[]
                for itm in filenames:
                    after = self.getHook(self.relDstPath(self.profile.deploy_hooks) + itm, 180)
                    
                if len(after) > 0:
                    tmplt['hooks'].append(after)
                else:
                    del tmplt['hooks']
             
            #------------------------------------------------------------------------------#
            # Prepare the Files Section for Apache configuration files   
            #------------------------------------------------------------------------------#   
            elif  self.stdPath(dirpath).startswith(self.absPath(self.profile.apache_config)):
                subDirPath = self.stdPath(dirpath[len(self.absPath(self.profile.apache_config))+1:])
                subDirPath += '\\' if len(subDirPath) > 0 else ''
                

                if self.profile.verbose: 
                    for itm in filenames:
                        #tmplt['files'].append(self.getFile("conf.d\\" + subDirPath + itm,
                        tmplt['files'].append(self.getFile(self.profile.apache_config + '\\' + subDirPath + itm,
                                                           '/usr/local/etc/httpd/conf.d/'+subDirPath))
                else:
                    #tmplt['files'].append(self.getFile(".\conf.d\\",'/usr/local/etc/httpd/conf.d/'))
                    tmplt['files'].append(self.getFile(self.relPath(self.profile.apache_config),
                                                       '/usr/local/etc/httpd/conf.d/'))
                    
            #------------------------------------------------------------------------------#
            # Prepare the Files Section for Tomcat configuration files   
            #------------------------------------------------------------------------------#
            elif self.stdPath(dirpath).startswith(self.absPath(self.profile.tomcat_config)):
                subDirPath = self.stdPath(dirpath[len(self.absPath(self.profile.tomcat_config))+1:])
                subDirPath += '\\' if len(subDirPath) > 0 else ''
                
                if self.profile.verbose: 
                    for itm in filenames:
                        #tmplt['files'].append(self.getFile("conf\\" + subDirPath + itm,'/usr/share/tomcat7/conf/'+subDirPath))
                        tmplt['files'].append(self.getFile(self.profile.tomcat_config + '\\' + subDirPath + itm,
                                                           '/usr/share/tomcat7/conf/'+subDirPath))
                else:
                    #tmplt['files'].append(self.getFile(".\conf\\",'/usr/share/tomcat7/conf/'))
                    tmplt['files'].append(self.getFile(self.relPath(self.profile.tomcat_config),
                                                       '/usr/share/tomcat7/conf/'))
                    
            #------------------------------------------------------------------------------#
            # Prepare the Files Section for Apache static content files   
            #------------------------------------------------------------------------------#              
            elif self.stdPath(dirpath).startswith(self.absPath(self.profile.apache_content)):
                subDirPath = self.stdPath(dirpath[len(self.absPath(self.profile.apache_content))+1:])
                subDirPath += '\\' if len(subDirPath) > 0 else ''
                

                if self.profile.verbose: 
                    for itm in filenames:
                        #tmplt['files'].append(self.getFile("conf\\" + subDirPath + itm,'/usr/share/tomcat7/conf/'+subDirPath))
                        tmplt['files'].append(self.getFile(self.profile.apache_content + '\\' + subDirPath + itm,
                                                           '/var/www/html/' + subDirPath))
                else:
                    #tmplt['files'].append(self.getFile(".\conf\\",'/usr/share/tomcat7/conf/'))
                    tmplt['files'].append(self.getFile(self.relPath(self.profile.apache_content),
                                                       '/var/www/html/'))
            
            #------------------------------------------------------------------------------#
            # Prepare the Files Section for Tomcat Applications   
            #------------------------------------------------------------------------------#
            elif self.stdPath(dirpath).startswith(self.absPath(self.profile.tomcat_content)):
                subDirPath = self.stdPath(dirpath[len(self.absPath(self.profile.tomcat_content))+1:])
                subDirPath += '\\' if len(subDirPath) > 0 else ''
                

                if self.profile.verbose: 
                    for itm in filenames:
                        #tmplt['files'].append(self.getFile("conf\\" + subDirPath + itm,'/usr/share/tomcat7/conf/'+subDirPath))
                        tmplt['files'].append(self.getFile(self.profile.tomcat_content + '\\' + subDirPath + itm,
                                                           '/usr/share/tomcat7/webapps/' + subDirPath))
                else:
                    #tmplt['files'].append(self.getFile(".\conf\\",'/usr/share/tomcat7/conf/'))
                    tmplt['files'].append(self.getFile(self.relPath(self.profile.tomcat_content),
                                                       '/usr/share/tomcat7/webapps/'))
            #------------------------------------------------------------------------------#
            # Prepare the Files Section for root level files 
            #------------------------------------------------------------------------------#       
            else:
                subDirPath = self.stdPath(dirpath[len(self.profile.path)+1:])
                subDirPath += '\\' if len(subDirPath) > 0 else ''

                if self.profile.verbose:
                    for itm in filenames:
                        if itm == 'profile.ini':   # Don't propgate the deploy configuration file
                            pass
                        else:
                            #tmplt['files'].append(self.getFile(subDirPath + itm, self.profile.dst_path + subDirPath))
                            tmplt['files'].append(self.getFile(subDirPath + itm,
                                                  self.profile.dst_path + '/' + subDirPath  + itm))
                else:
                    tmplt['files'].append(self.getFile('\\', self.profile.dst_path))
        
        #------------------------------------------------------------------------------#
        # Prepare the Permissions Section 
        #------------------------------------------------------------------------------#
        tmplt['permissions'].append(self.getPermission('/var/log/httpd','root','apache',mode=775,ltype='directory'))
        tmplt['permissions'].append(self.getPermission('/var/run','root','apache',mode=775,ltype='directory'))
        tmplt['permissions'].append(self.getPermission('/var/www','root','apache',mode=775,ltype='directory'))
        tmplt['permissions'].append(self.getPermission('/usr/local/etc/httpd','root','apache',mode=775,ltype='directory'))
                
        tmplt['permissions'].append(self.getPermission('/var/log/tomcat7','root','tomcat',mode=775,ltype='directory'))
        tmplt['permissions'].append(self.getPermission('/var/cache/tomcat7','root','tomcat',mode=775,ltype='directory'))
        tmplt['permissions'].append(self.getPermission('/var/lib/tomcat7','root','tomcat',mode=775,ltype='directory'))

        tmplt['permissions'].append(self.getPermission('/home/ec2-user','ec2-user','ec2-user',mode=775,ltype='directory'))
        return tmplt

    def persist(self, dst, specStr):
        '''
        Serialize the specStr out to the file system 
        '''
        try:
            with open(dst, 'w') as yamlFile:
                #yaml.dump(specStr,yamlFile,default_flow_style=False)
                self.dump(specStr, yamlFile)  
                yamlFile.close()
            
        except IOError as ex1:
            print '%s %s' % (self.currTimeStamp(),ex1)
            

class AWSToolBox(object):
    '''
    A collection of tools for working with the AWS Python SDK (boto3).
    '''


    def __init__(self,profile):
        '''
        Constructor
        '''
        self.currTimeStamp = lambda: self.getTimeStamp(self.current_time())
        self.currDateStamp = lambda: self.getDateStamp(self.current_time())
        self.current_time  = lambda: long(round(time.time() * 1000))
        self.getDay        = lambda millis: datetime.datetime.fromtimestamp(millis / 1000.0).strftime('%d')
        self.getDateStamp  = lambda millis: datetime.datetime.fromtimestamp(millis / 1000.0).strftime('%Y-%m-%d')
        self.getTimeStamp  = lambda millis: datetime.datetime.fromtimestamp(millis / 1000.0).strftime('%H:%M:%S.%f')[0:12]+'   '
        self.profile       = profile
        self.deployment_time = 0L
        
        self.lines = []
        
        self.session = boto3.Session(profile_name=self.profile.profile)
        self.cdClnt  = self.session.client('codedeploy', self.profile.region)
        self.s3Clnt  = self.session.resource('s3', self.profile.region)
        self.logClnt = self.session.client('logs', self.profile.region)
   
    def condenseMsg(self, msg, indent):
        '''
        Condense long messages into a more compact linear format.
        '''
        wrk = msg.split()
        newMsg = ''
        
        # rearrange the whole lines
        for i in range(0, len(wrk) / 10):
            for j in range(i*10+0,i*10+10):
                newMsg += (wrk[j] + " ")
            newMsg += '\n' + indent
          
        # add the last partial line
        for k in range(j+1,j + len(wrk) % 10 + 1):
            newMsg +=(wrk[k] + " ")
        return newMsg
        
    def convert_file(self, fileName, targetOS="lin"):
        '''
        Convert File from local line delimiters into Linux line delimiters.
        
        '''

        # read the file converting local new character to Unix newlines
        with open(fileName, "U") as f: 
            self.lines = f.readlines()
        
        #
        # rewrite the file with the appropriate newline char at the end
        # Note: This code assumes it is being run on a Windows OS
        #
        with open(fileName, "wb" if targetOS == "lin" else "w") as f: 
            for line in self.lines:
                f.write(line)
     
        return fileName
    
    def create(self, srcPath, dstPath, fileName, targetOS="lin"):
        '''
        Creates a deployment package.
        
        Features
        - Recurse into subdirectories
        - Convert line delimiters for the target Operating System
        - Converts the deployment package into an archive (.zip)
        '''
        zfile = zipfile.ZipFile(dstPath + "/" + fileName, "w")
        fileList = [os.path.join(dirpath, f) for dirpath, 
                    dirnames, 
                    files in os.walk(srcPath) for f in files]
        for itm in fileList:
            # insert a converted file with relative Path names
            zfile.write(self.convert_file(itm,targetOS), 
                        self.profile.rename(itm[len(srcPath):]), 
                        zipfile.ZIP_DEFLATED)
        zfile.close()
        print("%s Created Deployment Package in AWS using %s"  
         % (self.currTimeStamp(), self.profile.working_dir + "/" + self.profile.file_name))
        return 
    
    def deploy(self, s3Obj, profile, region, desc, targetOS="lin"):
        '''
        Create and run an S3 based deployment package.
         
        '''
        #
        # Retrieve the Deployment Application and Group
        #
        resp = self.cdClnt.list_applications()
        resp = self.cdClnt.list_deployment_groups(applicationName=resp['applications'][0])
    
        try:
            deployment_time = self.current_time()
            print ("%s Requested deployment of %s from AWS S3(%s)." % 
                  (self.getTimeStamp(deployment_time),s3Obj.key,s3Obj.bucket_name))
            
            resp = self.cdClnt.create_deployment(
                applicationName=resp['applicationName'],
                deploymentGroupName=resp['deploymentGroups'][0],
                revision={
                    'revisionType': 'S3',
                    's3Location': {
                    'bucket': s3Obj.bucket_name,
                    'key': s3Obj.key,
                    'bundleType': 'zip',
                    'version': s3Obj.version_id,
                    'eTag': s3Obj.e_tag
                    }
                },
                deploymentConfigName='CodeDeployDefault.OneAtATime',
                description=desc,
                ignoreApplicationStopFailures=False,
                autoRollbackConfiguration={
                    'enabled': True,
                    'events': ['DEPLOYMENT_FAILURE']
                },
                updateOutdatedInstancesOnly=False
            )
            
        except botocore.exceptions.ClientError as ex1:
            resp = ex1.response
            if ex1.response['Error']['Code'] == 'DeploymentLimitExceededException':  
                print ('%s Specified deployment Group is currently busy! - Please try again later.\n'
                       % (self.currTimeStamp()))
            else:
                print ("%s %s" % (self.currTimeStamp(),ex1.response['Error']['Message']))
        
        return resp
    
    def download(self, profile, region, bucketRegEx, path, fileName):
        '''
        Download a deployment package from AWS.
        
        '''
        p = re.compile(bucketRegEx, re.IGNORECASE)
        
        # locate the specified Bucket and upload into it
        try: 
            for bucket in self.s3Clnt.buckets.all():
                match = re.search(p,bucket.name,0)
                if match:
                    self.s3Clnt.Bucket(bucket.name).download_file(fileName, path + "/" + fileName)
                    print "%s Downloaded AWS S3(%s) to %s" % (self.currTimeStamp(), bucket.name,  path + "/" + fileName)
        
        except botocore.exceptions.ClientError as ex1:
            if ex1.response['Error']['Code'] == 'ExpiredToken':  
                print("%s Abnormal Termination! %s\n\t\tPlease run CCHelper and try again." % 
                      (self.currTimeStamp(), ex1.response['Error']['Message']))
                sys.exit()
            else:
                print ex1.response
                
    def getLogEvents(self, grpName,strmName, maxLines, profile, region):
        '''
        Retrieve the log entries from CloudWatch.
        
        '''
        log = ''
        
        #
        # Retrieve the Custom Log entries
        #
        rsp = self.logClnt.get_log_events(
            logGroupName=grpName,
            logStreamName=strmName,
            limit=maxLines,
            startFromHead=False
        )
        
        #
        # Format the Custom Log entries
        #
        if len(rsp['events']) > 0:
            prevDay = rsp['events'][0]['timestamp']
            log = "Date: %s\n" % (self.getDateStamp(prevDay))
            for i in range(0,len(rsp['events'])):
                today = rsp['events'][i]['timestamp']
                if (self.getDay(today) != self.getDay(prevDay)):
                    log += "\nDate: %s\n" % (self.getDateStamp(today))
                    prevDay = today
                log += ("%s %s\n" % (self.getTimeStamp(today),
                                     rsp['events'][i]['message']))
        return log
    
    def upload(self, profile, region, bucketRegEx, path, fileName):
        '''
        Upload the new deployment package to AWS.
        
        '''
        s3Obj   = None
        data    = open(path + "/" + fileName, 'rb')
        p       = re.compile(bucketRegEx, re.IGNORECASE)
        
        # locate the specified Bucket and upload into it
        try: 
            print "%s Commencing Upload to AWS ..." % (self.currTimeStamp())
            for bucket in self.s3Clnt.buckets.all():
                match = re.search(p,bucket.name,0)
                if match:
                    s3Obj = self.s3Clnt.Bucket(bucket.name).put_object(Key=fileName, Body=data)
                    print "%s Uploaded %s to AWS S3(%s)" % (self.currTimeStamp(),  fileName, bucket.name)
            data.close()
            
            if s3Obj == None:
                print "%s Unable to locate an S3 bucket using %s. Uploading %s failed." % (self.currTimeStamp(), bucketRegEx, fileName)
        
        except botocore.exceptions.ClientError as ex1:
            if ex1.response['Error']['Code'] == 'ExpiredToken':  
                print("%s Abnormal Termination! %s\n\t\tPlease run CCHelper and try again." % (self.currTimeStamp(), ex1.response['Error']['Message']))
                sys.exit()
            else:
                print ex1.response
                
        return s3Obj
    
    def waitForCompletion(self, rsp, profile, region):
        result = False
        
        try:
            # Block execution until the deployment completes
            print ("%s Waiting for completion ..." % (self.currTimeStamp()))
            self.cdClnt.get_waiter('deployment_successful').wait(deploymentId=rsp['deploymentId'])
            result = True
            
        except botocore.exceptions.WaiterError as ex1:
            print "%s The requested deployment failed!\n" % (self.currTimeStamp())
            if (('deploymentInfo' in ex1.last_response) == True):
                print "\t\tApplication:\t%s" % (ex1.last_response['deploymentInfo']['applicationName'])
                print "\t\tVersion:\t%s"   % (ex1.last_response['deploymentInfo']['revision']['s3Location']['version'])
                print "\t\tBucket:\t\t%s"  % (ex1.last_response['deploymentInfo']['revision']['s3Location']['bucket'])
                print "\t\tObject:\t\t%s"  % (ex1.last_response['deploymentInfo']['revision']['s3Location']['key'])
                print "\t\teTag:\t\t%s\n"    % (ex1.last_response['deploymentInfo']['revision']['s3Location']['eTag']) 
                                       
                if (('errorInformation' in ex1.last_response['deploymentInfo']) == True ):      
                    print "\t\tError"
                    print ("\t\tCode:\t\t%s"    % 
                          (ex1.last_response['deploymentInfo']['errorInformation']['code']))
                    print ("\t\tMessage:\t%s\n"   % 
                          (self.condenseMsg(ex1.last_response['deploymentInfo']['errorInformation']['message'],'\t\t\t\t')))
                    
                if (('rollbackInfo' in ex1.last_response['deploymentInfo']) == True):        
                    print "\t\tRollBack"
                    print ("\t\tMessage:\t%s\n" % 
                          (self.condenseMsg(ex1.last_response['deploymentInfo']['rollbackInfo']['rollbackMessage'],'\t\t\t\t')))
            
        return result
    
if __name__ == "__main__": 
    fact = AppSpecFactory(Profile(sys.argv[1]))
    prod = 'C:\Users\Z8364A\Downloads\JavaStack\\appspec.yml'
    devl = 'appspec.yml'

    fact.persist(devl,fact.instanceOf())          