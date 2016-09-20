#remarks test
import threading , CI_LC_BL

import sys, logging
import cpppo
from cpppo.server.enip import address, client

upgradeCounter = 0
serverVersion = ''
    
from threading import Timer
class RepeatedTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._timer     = None
        self.interval   = interval
        self.function   = function
        self.args       = args
        self.kwargs     = kwargs
        self.is_running = False
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False

def reloadLC():
    try:
        CI_LC_BL.ci_print('! Abount to reload')
	reload(CI_LC_BL)
    except Exception as inst: 
        print "Error reload " + str(inst)        
        logging.warning('Error in reload :: ' + str(inst))
		
def upgradeLC():
    try: 
        CI_LC_BL.ci_print('! Abount to upgrade ')
	CI_LC_BL = pip.main(['install','--upgrade','CI_LocalConnector'])
    except Exception as inst:
        print "Error upgrade " + str(inst)        
        logging.warning('Error in upgrade :: ' + str(inst))
    
def MainLoop():
    global serverVersion
    global upgradeCounter
    try:
        CI_LC_BL.MainLoop()
        localVer = str(CI_LC_BL.getLocalVersion())
        updateToVer=str(CI_LC_BL.getServerSugestedVersion())

        #to prevent upgrading to much in case of a problem we count upgrade attempts and stop when its too big, but if the version changes we try again
        if serverVersion != updateToVer:
            serverVersion = updateToVer
            upgradeCounter = 0

        #CI_LC_BL.ci_print ("local ver=" + localVer)
        #CI_LC_BL.ci_print ("server ver= " + updateToVer)
        if (bool(updateToVer!='') & bool(updateToVer!=localVer) & bool(upgradeCounter<10)):
            upgradeCounter = upgradeCounter + 1
            CI_LC_BL.ci_print('Local Version is deifferent than server suggested version, upgrading from:' + localVer + ' To:' + updateToVer + ' Upgrade count:'+str(upgradeCounter))
            #upgradeLC()
            reloadLC()
    except Exception as inst:
        CI_LC_BL.ci_print ("Error MainLoop " + str(inst))        

def StartMainLoop():
    try:
        CI_LC_BL.ci_print("CI_LocalConnector Started")
        rt = RepeatedTimer(10, MainLoop)
    except Exception as inst:
        CI_LC_BL.ci_print("Error MainLoopStart " + str(inst))     
        
def showHelp():
    print ('CI_LocalConnector.py :Start application')
    print ('CI_LocalConnector.py help : display command line help')
    print ('CI_LocalConnector.py getCloudTags : Get Tags defenition from Cloud and save into file' +TagsDefenitionFileName)
    print ('CI_LocalConnector.py showSavedTags : Show the tags saved in file' +TagsDefenitionFileName)
    print ('CI_LocalConnector.py readModBusTags : Read Tags Fom Modbus and save to file' +TagsDefenitionFileName)
    print ('CI_LocalConnector.py readEtherNetIP_Tags : Read Tags Fom EtehernatIP and save to file' +TagsDefenitionFileName)
    print ('CI_LocalConnector.py setCloudTagsValues : Send Values from file to cloud')
    print ('CI_LocalConnector.py handleAllValuesFiles : Send Values from all files to cloud')
    print ('CI_LocalConnector.py StartMainLoop : Start Main Loop')
    print ('CI_LocalConnector.py TestMainLoopOnce : test main loop functionality one time')
 
#handle
#print 'Number of arguments:', len(sys.argv), 'arguments.'
#print 'Argument List:', str(sys.argv)
#print 'Argument List:', str(sys.argv[1])
CI_LC_BL.initLog()
CI_LC_BL.createLibIfMissing()
CI_LC_BL.initConfig()

if (len(sys.argv)==1):
    MainLoopStart()
if (len(sys.argv)>1 and sys.argv[1]=='help'):
    showHelp()
if (len(sys.argv)>1 and sys.argv[1]=='getCloudTags'):
    token = CI_LC_BL.getCloudToken()
    CI_LC_BL.getCloudTags(token)
if (len(sys.argv)>1 and sys.argv[1]=='showSavedTags'):
    tagsDef = CI_LC_BL.getTagsDefenitionFromFile()
    CI_LC_BL.printTags(tagsDef)
if (len(sys.argv)>1 and sys.argv[1]=='readModBusTags'):
    tagsDef = getTagsDefenitionFromFile()
    #printTags(tagsDef)
    values = readModBusTags(tagsDef)
    printTagValues(values)
    saveValuesToFile(values,'')
if (len(sys.argv)>1 and sys.argv[1]=='readEtherNetIP_Tags'):
    tagsDef = getTagsDefenitionFromFile()
    printTags(tagsDef)
    values = readEtherNetIP_Tags(tagsDef)
    printTagValues(values)
    saveValuesToFile(values,'')
if (len(sys.argv)>1 and sys.argv[1]=='setCloudTagsValues'):
    token = getCloudToken()
    tagsDef = getCloudTags(token) #must to init server!!! - fix
    #tagsDef = getTagsDefenitionFromFile()
    printTags(tagsDef)
    values = readModBusTags(tagsDef)
    printTagValues(values)
    #fileName = TagsValuesFileName + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")+ '.txt'
    #saveValuesToFile(values,fileName)
    #setCloudTagsBackup(token,4)
    isOk = setCloudTags(token,values)
    #print str(isOk)
    #fileName = "./" + TagsValueDir + '/' + fileName
    #handleValuesFile(token,fileName)
if (len(sys.argv)>1 and sys.argv[1]=='handleAllValuesFiles'):
    token = getCloudToken()
    handleAllValuesFiles(token)
if (len(sys.argv)>1 and sys.argv[1]=='StartMainLoop'):
    StartMainLoop()
if (len(sys.argv)>1 and sys.argv[1]=='TestMainLoopOnce'):
    MainLoop()

#MainLoop()
    






