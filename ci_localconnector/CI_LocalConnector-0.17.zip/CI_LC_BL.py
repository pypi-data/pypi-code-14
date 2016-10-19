#remarks test
import httplib, urllib , json , requests , urllib2, logging , time, datetime ,sys, os , threading , socket, ConfigParser ,random
#import pkg_resources  # part of setuptools
import cpppo
from cpppo.server.enip import address, client

TagsDefenitionFileName = 'TagsDefenition.txt'
TagsValuesFileName = '[NEW]TagsValues'
TagsValueDir = 'TagValues'
HomeDir = 'CI_LC'
HTTP_PREFIX = 'https' # https / http
#HTTP_PREFIX = 'https'

#config
cfg_serverAddress = ''
cfg_userName = ''
cfg_passWord = ''
cfg_plcMode = ''
        
#VER = pkg_resources.require("CI_LocalConnector")[0].version
VER = '0.17'
sugestedUpdateVersion = ''
configFile = 'config.ini'

def getLocalVersion():
    return VER
def getServerSugestedVersion():
    return sugestedUpdateVersion

def initLog():
    logging.basicConfig(filename='CI_LocalConnector.log',level=logging.INFO , format='%(asctime)s %(message)s')    
    logging.info('===============================')
    logging.info('CI_LocalConnector Init')

def ci_print(msg , level = ''):
    try:
        if level=='info':
            logging.info(msg)
        else:
            logging.warning(msg)
            
        print(msg)
    except Exception as inst:
        logging.warning('Main Exception :: ' + inst)

def initConfig():
    global cfg_serverAddress
    global cfg_userName
    global cfg_passWord
    global cfg_plcMode
    #check if config exists
    try:
        filePath = "/" + HomeDir + "/" +configFile
        exists = os.path.exists(filePath)
        strPlcModeOptions = ' other options (Simulation , ModbucTCP , EtherNetIP)'
        if exists == True:
            ci_print ("Found config in " + filePath)
            Config = ConfigParser.ConfigParser()
            d = Config.read(filePath)
            cfg_serverAddress = Config.get("Server", "Address")
            cfg_userName = Config.get("Server", "username")
            cfg_passWord = Config.get("Server", "password")
            cfg_plcMode = Config.get("Server", "plcMode")
            #single = Config.getboolean("Server", "Address")
            ci_print ("serverAddress:" + cfg_serverAddress)
            ci_print ("userName:" + cfg_userName)
            ci_print ("password:" + cfg_passWord)
            ci_print ("plcMode:" + cfg_plcMode + strPlcModeOptions)
        else:
            ci_print ("config not found , creating new one in " + filePath)
            config = ConfigParser.RawConfigParser()
            config.add_section('Server')
            config.set('Server', 'Address', 'localhost')
            config.set('Server', 'username', 'user_lc@site.com')
            config.set('Server', 'password', '123456')
            config.set('Server', 'plcMode', 'Simulation')

            with open(filePath, 'wb') as configfileTmp:
                config.write(configfileTmp)
    except Exception as inst:
        ci_print('initConfig Exception :: ' + str(inst))
    

def readEtherNetIP_Tags(tagsDefenitions):
    ci_print("start readEtherNetIP_Tags")
    ans  = []    
    try:
        maxOffset=0
        for index in range(len(tagsDefenitions)):
            try:
                offset = int(tagsDefenitions[index][u'OpcAddress'])
            except ValueError:
                offset = 0
            maxOffset = max(maxOffset,offset)
            
        strTags = "Data_Array[0-" + str(maxOffset) + "]"   
        host                        = '14.1.3.128'  # Controller IP address
        port                        = address[1]    # default is port 44818
        depth                       = 1             # Allow 1 transaction in-flight
        multiple                    = 0             # Don't use Multiple Service Packet
        fragment                    = False         # Don't force Read/Write Tag Fragmented
        timeout                     = 1.0           # Any PLC I/O fails if it takes > 1s
        printing                    = False         # Print a summary of I/O
        #tags                        = ["Data_Array[0]","Data_Array[1]"]
        #tags                        = ["Tag[0-9]+16=(DINT)4,5,6,7,8,9", "@0x2/1/1", "Tag[3-5]"]
        tags                        = [strTags]
        with client.connector( host=host, port=port, timeout=timeout ) as connection:
            operations              = client.parse_operations( tags )
            failures,transactions   = connection.process(
                operations=operations, depth=depth, multiple=multiple,
                fragment=fragment, printing=printing, timeout=timeout )

        ci_print("transactions " + str(transactions))
        ci_print("failures " + str(failures))
        #client.close()
        #sys.exit( 1 if failures else 0 )

        for index in range(len(tagsDefenitions)):
            try:
                offset = int(tagsDefenitions[index][u'OpcAddress'])
                CounterId = int(tagsDefenitions[index][u'CounterId'])
          
                #value = transactions[0][offset]
                value = 5;
                ci_print ('get register offset=' + str(offset) + ' value=' + str(value))
                val= {'offset':offset,'CounterId':CounterId,'time': str(datetime.datetime.now()), 'value': value}
                ans.append(val)
            except ValueError:
                ci_print ('Wrong offset (not int) ' + tagsDefenitions[index][u'OpcAddress'])
                
        ci_print("End Read readEtherNetIP Tag")
        return ans
    except Exception as inst:
        ci_print("Error in readEtherNetIP_Tags " + str(inst))
        return ans
    
def readModBusTags(tagsDefenitions):
    ans  = []
    
    try:       
        maxOffset=0
        for index in range(len(tagsDefenitions)):
            offset = int(tagsDefenitions[index][u'OpcAddress'])
            maxOffset = max(maxOffset,offset)
    
        
        ci_print ("Start Read ModBus Tag")
        from pymodbus.client.sync import ModbusTcpClient as ModbusClient
        client = ModbusClient('14.1.3.123', port=502)
        client.connect()
        rr = client.read_holding_registers(1,1+maxOffset)
        ci_print (rr.registers)
        for index in range(len(tagsDefenitions)):
            offset = int(tagsDefenitions[index][u'OpcAddress'])
            CounterId = int(tagsDefenitions[index][u'CounterId'])
          
            value = rr.registers[offset]
            ci_print ("get register offset=" + str(offset) + ' value=' + str(value))
            val= {'offset':offset,'CounterId':CounterId,'time': str(datetime.datetime.now()), 'value': value}
            ans.append(val)
            #ans.update({offset:[offset,CounterId,datetime.datetime.now(),value]})   
        
        client.close()
        logging.info('readModBusTags ')
        logging.info('readModBusTags = ' + str(ans) )
        ci_print ("End Read ModBus Tag")
        return ans
    except Exception as inst:
        ci_print ("error reading modbus" + str(inst))
        return ans

def readSimulation_Tags(tagsDefenitions):
    ci_print("start readSimulation_Tags")
    ans  = []    
    try:
        for index in range(len(tagsDefenitions)):
            try:
                CounterId = int(tagsDefenitions[index][u'CounterId'])
                value = random.uniform(-10, 10);
                #ci_print ('get register offset=' + str(offset) + ' value=' + str(value))
                val= {'CounterId':CounterId,'time': str(datetime.datetime.now()), 'value': value}
                ans.append(val)
            except ValueError:
                ci_print ('ValueError error ')
                
        ci_print("End Read readSimulation_Tags")
        return ans
    except Exception as inst:
        ci_print("Error in readSimulation_Tags " + str(inst))
        return ans
    
def printTagValues(tagValues):
    ci_print ("Count " + str(len(tagValues)) + " Tags")
    for index in range(len(tagValues)):
        ci_print (str(tagValues[index]))

def readModBusTagsBakcUp():
    ans = 0
    try:
        ci_print ("Start Read ModBus Tag")
        from pymodbus.client.sync import ModbusTcpClient as ModbusClient
        client = ModbusClient('14.1.3.123', port=502)
        client.connect()
        rr = client.read_holding_registers(1,1)
        ci_print (rr.registers)
        client.connect()
        client.close()
        ci_print ("End Read ModBus Tag")
        return rr.registers[0]
    except Exception as inst:
        ci_print ("error reading readModBusTagsBakcUp " + str(inst))
        return ans

def readEtherNetIP_TagsBU():
    ci_print("start readEtherNetIP_Tags")
    ans  = []    
    try: 
        host                        = '14.1.3.128'  # Controller IP address
        port                        = address[1]    # default is port 44818
        depth                       = 1             # Allow 1 transaction in-flight
        multiple                    = 0             # Don't use Multiple Service Packet
        fragment                    = False         # Don't force Read/Write Tag Fragmented
        timeout                     = 1.0           # Any PLC I/O fails if it takes > 1s
        printing                    = False         # Print a summary of I/O
        tags                        = ["Data_Array[0]","Data_Array[1]"]
        #tags                        = ["Tag[0-9]+16=(DINT)4,5,6,7,8,9", "@0x2/1/1", "Tag[3-5]"]

        with client.connector( host=host, port=port, timeout=timeout ) as connection:
            operations              = client.parse_operations( tags )
            failures,transactions   = connection.process(
                operations=operations, depth=depth, multiple=multiple,
                fragment=fragment, printing=printing, timeout=timeout )         
        ci_print ("transactions " + str(transactions))
        ci_print ("failures " + str(failures))
        #sys.exit( 1 if failures else 0 )


        ci_print("End Read ModBus Tag")
        return ans
    except Exception as inst:
        ci_print("Error in readEtherNetIP_Tags" + str(inst))
        return ans

def getCloudToken():
    ci_print ("start getCloudToken")
    global cfg_serverAddress
    token="empty"
    url = ''
    try:
        ci_print ("About to get token from cloud")
        host = cfg_serverAddress

        #localhost:63485 #local dev
        #1.2.3.4/EnerWeb #by IP
        #host /EnerWeb #by host
        url = HTTP_PREFIX + '://'+ cfg_serverAddress +'/token'
        response = requests.get(url,
                                data = {
                                    'grant_type' : 'password',
                                    'username' : cfg_userName ,
                                    'password' : cfg_passWord ,
                                    },
                                headers = {
                                    'User-Agent': 'python',
                                    'Content-Type': 'application/x-www-form-urlencoded',
                                    })
        data = response.text

        #ci_print ('Token Data:' + data)
        jsonData = json.loads(data)
        token = jsonData[u'access_token']
        ci_print ("recieved Token ")# + token
    except Exception as inst:
        ci_print('URL :: ' + str(url))
        ci_print('Error getting Token :: ' + str(inst))
        token = "Error"
        err = 2
    return token

def getTagsDefenitionFromFile():
    try:
        ci_print ('Start getTagsDefenitionFromFile ')  
        f2 = open(TagsDefenitionFileName, 'r')
        tags = json.load(f2)
        f2.close()
        ci_print ("Got " + str(len(tags)) + " Tags From File")
        #print tags
        return tags
    except Exception as inst:
        ci_print('Error in getTagsDefenitionFromFile :: ' + str(inst))

def getTagsValuesFromFile(fileName):
    try:
        ci_print ('Start get Values From File ' + fileName ) 
        f2 = open(fileName, 'r')
        vals = json.load(f2)
        f2.close()
        ci_print ("Got " + str(len(vals)) + " Values From File ")      
        return vals
    except Exception as inst:
        ci_print('Error in getTagsValuesFromFile :: ' + str(inst))

def saveValuesToFile(values , fileName):
    try:
        if fileName=='':
            fileName = TagsValuesFileName + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")+ '.txt'
        #fileName = "./" + TagsValueDir + '/' + fileName
        fileName = "/" + HomeDir + "/" + TagsValueDir + '/' + fileName
        ci_print ('Start save Values To File ' + fileName ) 
        #write tags to file
        f = open(fileName, 'w')
        json.dump(values, f)
        f.close()
    except Exception as inst:
        ci_print('Error in saveValuesToFile :: ' + str(inst))

def getCloudTags(token='' , building="Building 1"):
    global sugestedUpdateVersion
    ci_print ("start getCloudTags")
    tags= None
    try:        
        IpAddress = socket.gethostbyname(socket.gethostname())
        url = HTTP_PREFIX + '://'+ cfg_serverAddress +'/api/Site/GetCounters_V_1_1/?LocalConnectorBuilding='+building+'&version='+ VER + '&IpAddress='+IpAddress
        #ci_print(token)
        if token=='':
            ci_print('Using Basic Auth')
            response = requests.get(url,
                                    data = None,
                                    auth=(cfg_userName, cfg_passWord) )
            
        else:
            ci_print('Got Token Using Bearer auth')
            response = requests.get(url,
                                    data = None,
                                    headers={'Authorization': 'bearer %s' % token})
        
        #ci_print ('gettags response=' + response.text)
        ans = json.loads(response.text)
        updateToVersion = ans['m_Item1']
        tags = ans['m_Item2']

        sugestedUpdateVersion = updateToVersion
        if updateToVersion!= VER:
            ci_print('! > Local Version : ' + str(VER) + ' But Server suggest Other Version : ' + str(updateToVersion))        
        #write tags to file
        f = open(TagsDefenitionFileName, 'w')
        json.dump(tags, f)
        f.close()

        ci_print ("Get Cloud Counters recieved " + str(len(tags)) + " Tags")
        #printTags(tags)
    except Exception as err:
        ci_print ("Error getting tags from cloud ::" + str(err))
        tags = None
        
    if tags == None:
        tags = getTagsDefenitionFromFile()
    return tags

def printTags(tags):
    try:
        ci_print ("Print Tags : List Contains " + str(len(tags)) + " Tags")
        ci_print (tags)
        for index in range(len(tags)):
            msg = 'Counter Id: ' + str(tags[index][u'CounterId']) + ' Description: '+ str(tags[index][u'CounterDescription']) + ' OpcAddress: '+ str(tags[index][u'OpcAddress'])
            ci_print (msg)
            #print 'CounterId : ' + str(tags[index])
    except Exception as inst:
        tmpS = 'Error in printTags :: ' + str(inst)
        ci_print (tmpS)
        
def setCloudTags(tagValues , token=''):
    ci_print ("start setCloudTags")
    updatedSuccessfully = False
    try:
        url = HTTP_PREFIX + '://'+cfg_serverAddress+'/api/Site/SetCounterHistory/'
        
        payload = []
        for index in range(len(tagValues)):            
            counterId = tagValues[index][u'CounterId']
            timeStamp = str(tagValues[index][u'time'])
            value = tagValues[index][u'value']
            status = 2 #1 = Invalid , 2 = Valid
            ci_print ('CounterId = ' + str(counterId) + ' : ' + str(value))

            tagVal = {
                'CounterId':counterId
                 ,'CounterName': ''
                 ,'Error':None
                 ,'LCTimeStamp':timeStamp
                 ,'OpcAddress':''
                 ,'SiteId':0 #no relevant
                 ,'Status':status
                 ,'Value':value
                 }
            payload.append(tagVal)
                
        ci_print (str(payload))
        #response = requests.post(url,
        #                       data = json.dumps(payload),
         #                      headers={'Content-Type':"application/json",'Accept':'text/plain','Authorization': 'bearer %s' % token})


        if token=='':
            ci_print('Using Basic Auth')
            response = requests.post(url,
                                     data = json.dumps(payload),
                                     auth=(cfg_userName, cfg_passWord),
                                     headers={'Content-Type':"application/json",'Accept':'text/plain'} )

            
        else:
            ci_print('Got Token Using Bearer auth')
            response = requests.post(url,
                                     data = json.dumps(payload),
                                     headers={'Content-Type':"application/json",'Accept':'text/plain','Authorization': 'bearer %s' % token})



        ci_print (response)
        ci_print (response.text)
        logging.info('setCloudTags response = ' + str(response) + ' : ' + response.text )
        #print '==' + str(response.status_code)
        updatedSuccessfully = response.status_code == 200

    except Exception as inst:
        ci_print ("Error setting tags to cloud " + str(inst))
        return False

    return updatedSuccessfully

def handleValuesFile(fileName, token=''):
    try:
        ci_print("start handleValuesFile " + fileName)
        values = getTagsValuesFromFile(fileName)
        ci_print ('1-----------')
        errFile = '[ERR]' + fileName[5:]
        isOk = setCloudTags(values,token)
        if isOk :
            os.remove(fileName)
            ci_print("file removed " + fileName)
            return True
        else:
            os.rename(fileName, errFile)
            ci_print('Error Handling File ' + errFile)
    except Exception as inst:
        ci_print('Error in handleValuesFile :: ' + str(inst))
    return False
    
    
#Backup
def setCloudTagsBackup(token,value):
    ci_print ("start setCloudTags backup")
    tags="empty"
    try:
        #url = 'https://HOST/api/Site/SetCounterHistory/'
        url = HTTP_PREFIX + '://'+cfg_serverAddress+'/api/Site/SetCounterHistory/'

        payload = [
            {'CounterId':49
             ,'CounterName': 'idoTestDoNotTouch' #'Store 1 Energy'
             ,'Error':None
             ,'LCTimeStamp':str(datetime.datetime.now()) #'2016-06-26 09:52:00'
             ,'OpcAddress':'0' #'Channel1.Device1.Tag1'
             ,'SiteId':0 #no relevant
             ,'Status':2 #1 = Invalid , 2 = Valid
             ,'Value':value
             }
            ]
        
        response = requests.post(url,
                                data = json.dumps(payload),
                                headers={'Content-Type':"application/json",'Accept':'text/plain','Authorization': 'bearer %s' % token})
        ci_print (response)
        ci_print (response.text)
    
    except:
        ci_print ("Error setting tags to cloud")
        tags = "Error"
        err = 2
        raise
    #print "tags=" + str(tags)
    return tags

def handleAllValuesFiles(token=''):
    try:
        ci_print ('started handleAllValuesFiles')
        #if token=='':
        #    token = getCloudToken()
        i=0
        dirpath = "/" + HomeDir + "/" + TagsValueDir + "/"
        filesSortedByTime = [s for s in os.listdir(dirpath)
            if os.path.isfile(os.path.join(dirpath, s))]
        filesSortedByTime.sort(key=lambda s: os.path.getmtime(os.path.join(dirpath, s)))
        ci_print ('in Dir ' + dirpath + " Found " + str(len(filesSortedByTime)) + " files")
        for file in filesSortedByTime:
            if file.endswith(".txt") and file.startswith('[NEW]'):
                i=i+1
                ci_print ('about to process file:' + file)
                handleValuesFile("/" + HomeDir +"/" +TagsValueDir + '/' + file, token)
        
        if i>0:
            ci_print (str(i) + ' Files handled')
    except Exception as inst:
        ci_print ("Error handleAllValuesFiles " + str(inst))

def createLibIfMissing():
    try:
        dirName = "/" + HomeDir + "/"
        d = os.path.dirname(dirName)
        if not os.path.exists(d):
            os.makedirs(dirName)
            ci_print ('Home DIR  Created :: ' + dirName)
            
        dirName = "/" + HomeDir + "/" + TagsValueDir + "/"
        d = os.path.dirname(dirName)
        if not os.path.exists(d):
            os.makedirs(dirName)
            ci_print ('TagsValueDir Created')
    except Exception as inst:
        ci_print ("Error createLibIfMissing " + str(inst))        
        
def MainLoop(AuthMode='token'):
    try:    
        ci_print('=============================== AuthMode=' + AuthMode)
        ci_print('Loop started at ' + str(datetime.datetime.now()))
        token=''
        if (AuthMode=='token'):
            token = getCloudToken()
        # currently must get tags from cloud to init server before setting values
        tagsDef = getCloudTags(token)
        
        #printTags(tagsDef)
        if cfg_plcMode=='Simulation':
            values = readSimulation_Tags(tagsDef) 
        if cfg_plcMode=='ModbucTCP':
            values = readModBusTags(tagsDef)
        if cfg_plcMode=='EtherNetIP':
            values = readEtherNetIP_Tags(tagsDef)
    
        #printTagValues(values)
        saveValuesToFile(values,'')
        if token!='Error':
            handleAllValuesFiles(token)
        else:
            ci_print("No Token , skipping upload step")
    except Exception as inst:
        ci_print ("Error MainLoop " + str(inst))        
        logging.warning('Error in MainLoop :: ' + str(inst))

    ci_print('===============================')
    ci_print('CI_LocalConnector Ended')
    
