# -*- coding: utf-8 -*-
import os
import sys
import logging
import time


logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format='%(asctime)s %(message)s', datefmt='%d/%m/%Y %I:%M:%S %p')

SC_ROOT_PATH = os.path.join(os.path.dirname(__file__),'isomorphic/')
showEdges = False

logging.debug('smartClient log: *[ SC_ROOT_PATH: '+SC_ROOT_PATH+' ]*********************************************************')


class HTML5():
    MAIN_PAGE = """<HTML><HEAD>
    <SCRIPT>var isomorphicDir="/isomorphic/";</SCRIPT>
    <SCRIPT>isc_css3Mode="on";</SCRIPT>
    <SCRIPT SRC=/isomorphic/system/modules/ISC_Core.js></SCRIPT>
    <SCRIPT SRC=/isomorphic/system/modules/ISC_Foundation.js></SCRIPT>
    <SCRIPT SRC=/isomorphic/system/modules/ISC_Containers.js></SCRIPT>
    <SCRIPT SRC=/isomorphic/system/modules/ISC_Grids.js></SCRIPT>
    <SCRIPT SRC=/isomorphic/system/modules/ISC_Forms.js></SCRIPT>
    <SCRIPT SRC=/isomorphic/system/modules/ISC_DataBinding.js></SCRIPT>
    <SCRIPT SRC=/isomorphic/system/modules/ISC_History.js></SCRIPT>
    <SCRIPT SRC=/isomorphic/system/modules/ISC_Calendar.js></SCRIPT>
    <SCRIPT SRC=/isomorphic/system/modules/ISC_RichTextEditor.js></SCRIPT>
    <!-- SKIN DISPONIBILI
    <SCRIPT SRC=/isomorphic/skins/BlackOps/load_skin.js></SCRIPT>
    <SCRIPT SRC=/isomorphic/skins/Cupertino/load_skin.js></SCRIPT>
    <SCRIPT SRC=/isomorphic/skins/Enterprise/load_skin.js></SCRIPT>
    <SCRIPT SRC=/isomorphic/skins/EnterpriseBlue/load_skin.js></SCRIPT>
    <SCRIPT SRC=/isomorphic/skins/Graphite/load_skin.js></SCRIPT>
    <SCRIPT SRC=/isomorphic/skins/Mobile/load_skin.js></SCRIPT>
    <SCRIPT SRC=/isomorphic/skins/SilverWave/load_skin.js></SCRIPT>
    <SCRIPT SRC=/isomorphic/skins/Simplicity/load_skin.js></SCRIPT>
    <SCRIPT SRC=/isomorphic/skins/SmartClient/load_skin.js></SCRIPT>
    <SCRIPT SRC=/isomorphic/skins/standard/load_skin.js></SCRIPT>
    <SCRIPT SRC=/isomorphic/skins/TreeFrog/load_skin.js></SCRIPT>
    --!>
    <SCRIPT SRC=/isomorphic/skins/Enterprise/load_skin.js></SCRIPT>
</HEAD>
<BODY><SCRIPT>
    //$__INSERT_HERE_JS__$
    window.onload = function(){
        var ws = new WebSocket("ws://localhost:8080/websocket");
        ws.onopen = function() {
            ws.send("Hello, world!");
        };
        ws.onmessage = function (event) {
            strJS = event.data.replace(/\|/g, '"')
            eval(strJS);
            //isc.say(event.data);
        };
    };
    function myGlobalCallback(data) {
        //isc.say(data);
        //window.alert(document.cookie);
        var responseJ=JSON.parse(data);
        if (responseJ.response.status == "ok") {
            strJS = responseJ.response.js.replace(/\|/g, '"')
            eval(strJS);
        }
        if (responseJ.response.status == "ko") {
            window.alert(responseJ.response.msg);
        }
        if (responseJ.response.status == "cookie") {
            if (responseJ.response.data.login != "") {
                window.alert(document.cookie)// = document.cookie + ";login:'"+responseJ.response.data.login+"'"
            }
        }
    };
    function manageSelect(p1, p2) {
        var par = {
            p1: p1,
            p2: p2
        }
        //url2Req = 'manageRequest/'+reqURL
        //isc.RPCManager.sendRequest({'params':par, callback: 'myGlobalCallback(data)', actionURL: url2Req});
        isc.RPCManager.sendRequest({'params':par, callback: 'myGlobalCallback(data)', actionURL: 'manageRequest/{"event":"select","operation":"changed","object":{"object":"p2"}}'});
    };
    //$__INSERT_HERE_KEYBOARD_MANAGER_JS__$
    isc.Page.setEvent('keyPress', 'myKeyboardManager()');
</SCRIPT></BODY>
</HTML>
    """
    CRLF = ';\n'
    INSERT_HERE_JS = "//$__INSERT_HERE_JS__$"
    INSERT_HERE_KEYBOARD_MANAGER_JS = "//$__INSERT_HERE_KEYBOARD_MANAGER_JS__$"
    #INSERT_HERE_JS = "//$__INSERT_HERE_JS__$"
    ID = "$ID$"

    def __init__(self, clientSession={}):
        self.idName = 0

        self.mainPage = HTML5.MAIN_PAGE
        self.session = clientSession

        self.addeOnce = False
        self.componentList = []
        self.componentListMaster2Remove = []
        self.componentList2Remove = []
        self.insertHereJS = ''
        self.finalMerge = []
        self.keyboardManager = KeyboardManager('myKeyboardManager')
        self.enter = False

        self.idName = self.session.get('pysc_idName', 0)
        #self.tagList = []
        #self.tagList.append(HTML5.INSERT_HERE_JS)


    def renderMainPage(self, componentList, nameId=0):
        for c in componentList:
            #if isinstance(c, (ListGrid)):
            #    self.enter = True

            if len(c.componentList) > 0:
                nameId = self.renderMainPage(c.componentList, nameId)

            localComponent = c.getComponentJS(self, nameId)
            if localComponent != '':
                self.insertHereJS = self.insertHereJS + localComponent + HTML5.CRLF
                nameId = nameId + 1

        return nameId

    def renderAddMembers(self, componentList):
        for c in componentList:
            for innerC in c.componentList:
                self.renderAddMembers(c.componentList)
                if innerC.addedMembers != True:
                    innerC.addedMembers = True
                    if isinstance(c, (Window)):
                        self.insertHereJS = self.insertHereJS + self.getID(c) + '.addItems(' + self.getID(innerC) + ')' + HTML5.CRLF
                    elif isinstance(c, (SectionStack, MenuLink, MainMenu)):
                        pass#self.insertHereJS = self.insertHereJS + c.getID() + '.addItems(' + innerC.getID() + ')' + HTML5.CRLF
                    else:
                        self.insertHereJS = self.insertHereJS + self.getID(c) + '.addMembers(' + self.getID(innerC) + ')' + HTML5.CRLF

    def renderRemoveMembers(self, componentListMaster, componentList2Remove):
        for index in range(len(componentListMaster)):
            cM = componentListMaster[index]
            c2R = componentList2Remove[index]
            if isinstance(cM, (Window)):
                self.insertHereJS = self.insertHereJS + self.getID(cM) + '.removeItem(' + self.getID(c2R) + ')' + HTML5.CRLF
            else:
                self.insertHereJS = self.insertHereJS + self.getID(cM) + '.removeMember(' + self.getID(c2R) + ')' + HTML5.CRLF

    def renderAddKeyboardManager(self, keyboardManager):
        #logging.debug('...keyboardManager=' + str(keyboardManager))
        localIF = ''
        if keyboardManager != None:
            #logging.debug('...keyboardManager.keyList2Manage=' + str(keyboardManager.keyList2Manage))
            if keyboardManager.keyList2Manage != None:
                for k in keyboardManager.keyList2Manage:
                    #logging.debug('...***k.ctrl='+str(k.ctrl))
                    #logging.debug('...***k.alt='+str(k.alt))
                    #logging.debug('...***k.key='+str(k.key))
                    #logging.debug('...***k.component='+str(k.component.getID()))
                    localJS = ''
                    for event in k.eventList:
                        localStr = event % k.component.getID()
                        localJS = localJS + localStr

                    #logging.debug('...***localJS=' + str(localJS))
                    localIF = localIF + "if(isc.Event.getKey() === '"+k.key+"') {" + localJS + "return false;} "
            if localIF == '' and self.enter == False:
                localIF = "if(isc.Event.getKey() === 'Enter') {alert('Enter key is  disabled'); return false;} "
            keyboardManager.insertHereKeyboardJS = "function "+keyboardManager.functionName+" () { "+localIF+"return true;};"

    def getID(self, c, appendAnyway=False):
        local_id = c.getID()
        if local_id in ('$ID$'):
            local_id = '%s'
            self.finalMerge.append(c)
        elif appendAnyway:
            self.finalMerge.append(c)
        return local_id

    def renderFinalMerge(self):
        local_js = self.insertHereJS
        if self.finalMerge <> []:
            local_component_list = []
            for c in self.finalMerge:
                local_js = local_js.replace('%s', c.getID(),1)

            self.insertHereJS = local_js


    """
    function myKeyboardManager () {
        /*
        if(isc.Event.ctrlKeyDown() && isc.Event.getKey() === 'N'){
            return false;
        }
        */
        if(isc.Event.getKey() === 'Enter'){
            btt_5.setFocus(true);
            btt_5.click();
            return false;
        };
        return true;
    };
    """

    def getMainPage(self, main=True):
        self.insertHereJS = ''
        logging.debug('self.renderMainPage(self.componentList)')
        self.idName = self.renderMainPage(self.componentList, self.idName)
        logging.debug('self.renderAddMembers(self.componentList)')
        self.renderAddMembers(self.componentList)
        logging.debug('self.renderRemoveMembers(self.componentList)')
        self.renderRemoveMembers(self.componentListMaster2Remove, self.componentList2Remove)
        logging.debug('self.keyboardManager')
        self.renderAddKeyboardManager(self.keyboardManager)
        logging.debug('self.finalMerge')
        self.renderFinalMerge()

        localMainPage = self.insertHereJS
        if main == True:
            localMainPage = self.mainPage.replace(HTML5.INSERT_HERE_JS, localMainPage + HTML5.INSERT_HERE_JS)
            localMainPage = localMainPage.replace(HTML5.INSERT_HERE_KEYBOARD_MANAGER_JS, self.keyboardManager.insertHereKeyboardJS + HTML5.INSERT_HERE_KEYBOARD_MANAGER_JS)

        #logging.debug(localMainPage)
        return localMainPage

    def addComponent(self, c):
        if self.addeOnce == False:
            self.addeOnce = True
            self.componentList.append(c)
        else:
            if not isinstance(c, (Window)):
                logging.debug('*********************************************************')
                logging.debug('NON si possono aggiungere due componenti sulla home page!')
                logging.debug('*********************************************************')
            else:
                self.componentList.append(c)

    def removeComponent(self, master, c):
        self.componentListMaster2Remove.append(master)
        self.componentList2Remove.append(c)

    def add2Session(self, key, value, window=None):
        if window!=None:
            if window.pre_name != None and window.pre_name != '':
                key = key + window.pre_name

        self.session[key] = value

    def getFromSession(self, key, defValue=None, istanza=None):
        if istanza!=None:
            key = key + istanza

        return self.session.get(key, defValue)

    def removeFromSession(self, key, istanza=None):
        if istanza!=None:
            key = key + istanza

        if key in self.session:
            del(self.session[key])

    def updateSession(self):
        self.session['pysc_idName'] = self.idName

    def clearSession(self):
        keys = self.session.keys()
        for key in keys:
            if isinstance(self.session.get(key), (Component)):
                self.removeFromSession(key)

    def getNewIdName(self):
        name = self.idName
        self.idName = self.idName + 1
        return name


class KeyboardManager():
    class KeyCode():
        def __init__(self, component=None, key='Enter', ctrl=False, alt=False):
            self.ctrl = ctrl
            self.alt = alt
            self.key = key
            self.component = component
            self.eventList = []  # setFocus(true); click();


    def __init__(self, functionName):
        self.keyList2Manage = []
        self.insertHereKeyboardJS = ''
        self.functionName = functionName

    def addEventList2Component(self, component=None, eventList=[], key='Enter', ctrl=False, alt=False): # ['%s.setFocus(true);', '%s.click();']
        if component != None and eventList != []:
            logging.debug('eventList: ' + str(eventList))
            localKey = self.KeyCode(component, key, ctrl, alt)
            for event in eventList:
                localKey.eventList.append(event)
            self.keyList2Manage.append(localKey)


class Component():
    NAME = '$name$'
    DICT = '$dict$'

    def __init__(self):
        # DEVO IMPOSTARE I DEFAULT **kwargs??? DA VEDERE
        self.addedOnce = False
        self.addedMembers = False
        self.pre_name = ''

        self.showEdges = showEdges

        self.component = ''
        self.dataSource = None
        self.actionUrl = []
        self.validator = []

        self.transformValue = None
        self.dict = {
            "ID":HTML5.ID,
            "height":"100%",
            "width":"100%",
            #"membersMargin":5,
            #"layoutMargin":0,
        }

        if self.showEdges:
            self.dict["showEdges"] = "true"

        self.dictLists = {
            "members":[], # in teoria non dovrebbe mai essere usata
            "fields": [],
            "valueMap": [],
            "controlGroups": [],
            "sections": [],
            "data": [],
        }

        self.componentList = []
        self.keyboardManager = None  # fixme

    def getID(self):
        return self.dict.get("ID", "UNASSIGNED")

    def getDataSource(self):
        return self.dataSource

    def setDataSource(self, dataSource):
        self.dataSource = dataSource
        for au in self.dataSource.actionUrl:
            au.addDataURL = True
            au.fetchDataURL = True
            au.removeDataURL = True
            au.updateDataURL = True

    def addComponent(self, c):
        if c.dataSource != None:
            self.componentList.append(c.dataSource)

        if self.pre_name != None and self.pre_name != '':
            c.pre_name = self.pre_name
        self.componentList.append(c)

    def addActionUrl(self, actionUrl=None):
        if actionUrl != None:
            self.actionUrl.append(actionUrl)

    def addValidator(self, validator=None, position=0):
        localV = []
        if len(self.validator) > position:
            localV = self.validator[position]
        else:
            self.validator.append(localV)
        if validator != None:
            localV.append(validator)

    def getProperty(self, key, subList=None, position=0):
        localDict = self.dict

        if subList == None:
            return localDict.get(key, None)
        else:
            localList = self.dictLists.get(subList, [])
            if localList != []:
                if len(localList) > position:
                    localDict = localList[position]
                    return localDict.get(key, None)
                else:
                    return None
            else:
                return None


    def setProperty(self, key, value, subList=None, position=0):
        localDict = self.dict

        localPropertySetted = True
        if subList == None:
             localDict[key] = value
             if isinstance(self, (MainMenu)) and key == 'menu':
                 self.addComponent(value)
        else:

             localList = self.dictLists.get(subList, None)
             if subList in ('controlGroups', 'valueMap'): # LISTA DI ELEMENTI
                 if localList != None:
                     localList.append(value)
                 else:
                     localPropertySetted = False

             elif subList in ('fields', 'sections', 'data'): # LISTA di DIZIONARI
                 if localList != []:
                     if len(localList) > position:
                         localDict = localList[position]
                         localDict[key] = value
                     else:
                         localDict = {}
                         localDict[key] = value
                         localList.append(localDict)
                 else:
                     localDict = {}
                     localDict[key] = value
                     localList.append(localDict)

                 if isinstance(self, (SectionStack)) and key == 'items':
                     self.addComponent(value)
                 if isinstance(self, (MenuLink)) and key == 'submenu':
                     self.addComponent(value)

             elif subList == 'members': # LISTA di DIZIONARI
                 localPropertySetted = False

             else:
                 localPropertySetted = False

        if localPropertySetted == False:
             logging.debug("localPropertySetted: " + str(localPropertySetted))
             logging.debug('key='+str(key)+', value='+str(value)+', subList='+str(subList)+', position='+str(position))

        return localPropertySetted

    def removeProperty(self, key):
        if key in self.dict:
            del self.dict[key]

    def getComponentJS(self, page, nameId):
        localComponent=''
        if self.addedOnce == False:
            self.addedOnce = True

            fields = self.dictLists.get('fields', [])
            members = self.dictLists.get('members', [])
            valueMap = self.dictLists.get('valueMap', [])
            controlGroups = self.dictLists.get('controlGroups', [])
            sections = self.dictLists.get('sections', [])
            data = self.dictLists.get('data', [])

            #logging.debug(">>> elaboro dict: " + str(self.dict))
            if self.pre_name != None and self.pre_name != '':
                self.dict['ID']=self.name+'_'+str(self.pre_name)+'_'+str(nameId)
            else:
                self.dict['ID'] = self.name + '_' + str(nameId)

            if self.dataSource != None:
                self.dict['dataSource'] = page.getID(self.dataSource)

            localDictComponent = ''
            for key in self.dict:
                if localDictComponent != '':
                   localDictComponent=localDictComponent+','

                localDictComponent=localDictComponent+'"' + key + '":'
                if isinstance(self.dict[key], (int, long, float, complex)):
                    localDictComponent=localDictComponent+str(self.dict[key])
                elif isinstance(self.dict[key], (Component)):
                    localDictComponent = localDictComponent + str(page.getID(self.dict[key]))
                else:
                    localDictComponent=localDictComponent+'"'+str(self.dict[key])+'"'

            if len(controlGroups) > 0:
                #logging.debug(">>> elaboro controlGroups: " + str(controlGroups))
                localCG = ''
                for elem in controlGroups:
                   if localCG != '':
                      localCG=localCG+','

                   localCG=localCG+'"' + elem + '"'
                localDictComponent = localDictComponent + ',"controlGroups":['+localCG+']'

            if len(sections) > 0:
                #logging.debug(">>> elaboro controlGroups: " + str(controlGroups))
                localS = ''
                for elem in sections:
                   if localS != '':
                       localS=localS+','

                   localDict = ''
                   for key in elem:
                       if localDict != '':
                           localDict = localDict + ','

                       localDict = localDict + '"' + key + '":'
                       if isinstance(elem[key], (int, long, float, complex)) or key in ('items'):
                           if isinstance(elem[key], (Component)):
                               localDict = localDict + str(page.getID(elem[key]))
                           else:
                               localDict = localDict + str(elem[key])
                       else:
                           localDict = localDict + '"' + str(elem[key]) + '"'

                   localS = localS + '{'+localDict+'}'

                localDictComponent = localDictComponent + ',"sections":['+localS+']'

            if len(data) > 0:
                #logging.debug(">>> elaboro controlGroups: " + str(controlGroups))
                localS = ''
                for elem in data:
                   if localS != '':
                       localS=localS+','

                   localDict = ''
                   for key in elem:
                       if localDict != '':
                           localDict = localDict + ','

                       localDict = localDict + '"' + key + '":'
                       if isinstance(elem[key], (int, long, float, complex)) or key in ('menu'):
                           if isinstance(elem[key], (Component)):
                               localDict = localDict + str(page.getID(elem[key]))
                           else:
                               localDict = localDict + str(elem[key])
                       elif isinstance(elem[key], (ActionUrl)):
                           au = elem[key]
                           localDict = localDict + au.getClickJs(page)
                       elif key in ('submenu'):
                           localDict = localDict + str(page.getID(elem[key]))
                       else:
                           localDict = localDict + '"' + str(elem[key]) + '"'

                   localS = localS + '{'+localDict+'}'

                localDictComponent = localDictComponent + ',"data":['+localS+']'

            if isinstance(self, (TextArea, EditField, Link, PasswordField, DateField, CheckBox, RadioGroup, SelectField, Spacer, Header, PickList)):
                self.setProperty('name', page.getID(self), 'fields', 0)

            if len(fields) > 0:
                #logging.debug(">>> elaboro fields: " + str(fields))
                localF = ''
                for index in range(len(fields)):
                    elem = fields[index]
                    if localF != '':
                        localF=localF+','

                    localDict=''
                    for key in elem:
                        if localDict != '':
                            localDict = localDict + ','

                        localDict = localDict + '"' + key + '":'
                        if isinstance(elem[key], (int, long, float, complex)):
                            #localDict = elem + str(elem[key])
                            localDict = localDict + str(elem[key])
                        elif isinstance(elem[key], (list)):
                            strElemLocal = ''
                            for ele in elem[key]:
                                if strElemLocal != '':
                                    strElemLocal = strElemLocal + ','

                                strL_ele = str(ele)
                                if strL_ele==ele:
                                    strElemLocal = strElemLocal + '"'+strL_ele+'"'
                                else:
                                    strElemLocal = strElemLocal + strL_ele
                            localDict = localDict + '['+strElemLocal+']'
                        elif isinstance(elem[key], (ActionUrl)):
                            au = elem[key]
                            localDict = localDict + au.getClickJs(page)
                        else:
                            #localDict = localDict + '"' + str(elem[key]) + '"'
                            strL_ele = str(elem[key])
                            if strL_ele == elem[key]:
                                localDict = localDict + '"' + strL_ele + '"'
                            else:
                                localDict = localDict + strL_ele

                    if len(valueMap) > 0:
                        # logging.debug(">>> elaboro valueMap: " + str(valueMap))
                        localVM = ''
                        for elem in valueMap:
                            if localVM != '':
                                localVM = localVM + ','

                            localVM = localVM + "'" + elem + "'"
                        localDict = localDict + ',"valueMap":"[' + localVM + ']"'

                    if self.transformValue != None:
                        localDict = localDict + ',"transformInput":' + self.transformValue

                    if len(self.validator) > index:
                        localV = self.validator[index]
                        localStrV = ''
                        for v in localV:
                            if localStrV != '':
                                localStrV = localStrV + ','

                            localStrV = localStrV + v.getValidator()

                        localDict = localDict + ',"validators":[' + localStrV + ']'
                        #logging.debug("localStrV: " + localStrV)
                    localF=localF+'{' + localDict + '}'

                localDictComponent = localDictComponent + ',"fields":['+localF+']'

            if isinstance(self, (Window)):
                localDictComponent = localDictComponent + ',"items":[]'
                localDictComponent = localDictComponent + ',"name":"'+self.dict['ID']+'"'
                localDictComponent = localDictComponent + ',"componentName":"'+self.dict['ID']+'"'

            for au in self.actionUrl:
                localDictComponent = localDictComponent + ',"'+au.getEvent()+'":' + au.getClickJs(page)

                localOp=au.getOperation()
                if au.fetchDataURL:
                    au.setOperation('fetchDataURL')
                    actUrl = au.getBaseRequest() + au.getActionUrl()
                    localDictComponent = localDictComponent + ',"fetchDataURL":'+"'"+actUrl+"'"

                if au.addDataURL:
                    au.setOperation('addDataURL')
                    actUrl = au.getBaseRequest() + au.getActionUrl()
                    localDictComponent = localDictComponent + ',"addDataURL":'+"'"+actUrl+"'"

                if au.updateDataURL:
                    au.setOperation('updateDataURL')
                    actUrl = au.getBaseRequest() + au.getActionUrl()
                    localDictComponent = localDictComponent + ',"updateDataURL":'+"'"+actUrl+"'"

                if au.removeDataURL:
                    au.setOperation('removeDataURL')
                    actUrl = au.getBaseRequest() + au.getActionUrl()
                    localDictComponent = localDictComponent + ',"removeDataURL":'+"'"+actUrl+"'"

                #localDictComponent = localDictComponent + ',"queryData":' + "'" + au.getParams() + "'"

                au.setOperation(localOp)

            if len(members) > 0:
                logging.debug("??? elaboro members: " + str(members))

            localComponent = self.component.replace(Component.DICT,localDictComponent)
            localComponent = localComponent.replace(Component.NAME,page.getID(self))
            #logging.debug("DEFINIZIONE: " + self.component)

        #else:
        #    logging.debug('COMPONENTE già inserito')

        return localComponent


"""
RPCManager.sendRequest({
    httpMethod: "POST",
    actionURL: "/rest/addUser",
    params: {
        userId: 1,
        userName: "aaa",
        userUserName: "aaa"
    },
    paramsOnly: true,
})
function () { 
   isc.RPCManager.sendRequest({ 
      data: { "theDate": "'+click+'" }, 
      httpMethod: "POST",
      useSimpleHttp: true, 
      contentType: "application/json", 
      evalResult: true, 
      callback: "myGlobalCallback(data)", 
      actionURL: "tryForBelieve"
   }); 
},
{
    "response": {
       "status": 0,
       "data": [
           {"countryCode": "value11", "countryName": "value11", "capital": "value11"},
       ]
    }
}
isc.RPCManager.sendRequest({ 
    actionURL: "tryForBelieve",
    data: { theDate : new Date() },
    httpMethod: "POST",
    contentType: "application/json",
    useSimpleHttp: true,
    evalResult: true,
    callback: "callback(data)"
});
"""


class ReplyClick():
    TAG_DATA = "$data$"
    TAG_MSG = "$msg$"
    TAG_STATUS = "$status$"
    TAG_JS = "$js$"

    def __init__(self):
        self.reply = '{"msg":"' + ReplyClick.TAG_MSG + '","data":' + ReplyClick.TAG_DATA + ',"status":"' + ReplyClick.TAG_STATUS + '","js":"' + ReplyClick.TAG_JS + '"}'
        self.status = 'ok'
        self.data = '{}'
        self.msg = 'no message'
        self.js = 'window.alert(dataJ.msg); '

    def getData(self):
        return self.data

    def getMsg(self):
        return self.msg

    def getStatus(self):
        return self.status

    def getJs(self):
        return self.js

    def setData(self, data):
        self.data = data

    def setMsg(self, msg):
        self.msg = msg

    def setStatus(self, status):
        self.status = status

    def setJs(self, js, lastToken=True):
        self.js = js
        if lastToken == True:
            self.js = self.js +'; '

    def addJs(self, js, lastToken=True):
        self.js = self.js + js
        if lastToken == True:
            self.js = self.js + '; '

    def getReply(self):
        reply = self.reply.replace(ReplyClick.TAG_DATA, self.getData())
        reply = reply.replace(ReplyClick.TAG_MSG, self.getMsg())
        reply = reply.replace(ReplyClick.TAG_STATUS, self.getStatus())
        reply = reply.replace(ReplyClick.TAG_JS, self.getJs().replace('"',"|").replace('\n',''))
        reply = '{"response":'+reply+'}'
        return reply


class ActionUrl():
    TAG_EVENT = "$event$"
    TAG_OPERATION = "$operation$"
    TAG_OBJECT = "$object$"
    TAG_PARAMS = "$params$"
    TAG_ACT_URL = "$actUrl$"
    TAG_CUSTOM = "$custom$"
    TAG_JS = 'function(){var noButton = isc.Button.create({ title:"NO" });dlg_Yes_no=isc.Dialog.create({"message":"Sure?","isModal":"true","showModalMask":"true",icon:"[SKIN]ask.png",buttons:[noButton,isc.Button.create({ title:"YES" })],buttonClick : function (button, index) {if (index == 1){isc.RPCManager.sendRequest({$params$,"callback":"myGlobalCallback(data)",$actUrl$});};dlg_Yes_no.hide();}});noButton.focus();$custom$}'
    #TAG_JS = 'function(){var noButton = isc.Button.create({ title:"no" });dlg_Yes_no=isc.Dialog.create({message : "Sicuro?",icon:"[SKIN]ask.png",buttons:[noButton,isc.Button.create({ title:"sì" })],buttonClick : function (button, index) {if (index == 1){isc.RPCManager.sendRequest({$params$,"callback":"myGlobalCallback(data)",$actUrl$});}; dlg_Yes_no.hide();}});noButton.focus();}'
    TAG_JS_NO_CONF = 'function(){isc.RPCManager.sendRequest({$params$,"callback":"myGlobalCallback(data)",$actUrl$});$custom$}'

    def __init__(self, baseRequest='manageRequest/'):
        self.actionUrl = '{"event":"' + ActionUrl.TAG_EVENT + '","operation":"' + ActionUrl.TAG_OPERATION + '","object":' + ActionUrl.TAG_OBJECT + '}'

        self.event = 'click'
        self.operation = 'operation'
        self.object = 'object'
        self.params = '{}'
        self.paramsVarArgs = None
        self.baseRequest = baseRequest
        self.clickJs = None
        self.jsVarArgs = None
        self.clickJsCustom = ''
        self.jsVarArgsCustom = None
        self.custom = False
        self.appendCustom = False
        self.useQuote = False
        self.confirmation = False

        self.fetchDataURL = False
        self.addDataURL = False
        self.updateDataURL = False
        self.removeDataURL = False

    def getEvent(self):
            return self.event

    def getOperation(self):
        return self.operation

    def getObject(self):
        return self.object

    def getParams(self):
        params = self.params
        localParams = []
        if self.paramsVarArgs != None:
            for var in self.paramsVarArgs:
                if isinstance(var, (Component)):
                    localParams.append(var.getID())
                else:
                    localParams.append(var)

            params = params % tuple(localParams)
            #command = '{"user":%s.getValue(user.fields[0].%s),"password":%s.getValue(%s.fields[0].name)}' % (user.getID(), user.getID(), password.getID(), password.getID())
        return params

    def getBaseRequest(self):
        return self.baseRequest

    def getClickJs(self, page):
        localJS = ''
        if self.custom == False:
            if self.confirmation == True:
                localJS = ActionUrl.TAG_JS
            else:
                localJS = ActionUrl.TAG_JS_NO_CONF

            localJS = localJS.replace(ActionUrl.TAG_PARAMS, '"params":' + self.getParams())
            localJS = localJS.replace(ActionUrl.TAG_ACT_URL, '"actionURL":' + "'" + self.getBaseRequest() + self.getActionUrl() + "'")

            if self.appendCustom:
                localjsVarArgsCustom = []
                for c in self.jsVarArgsCustom:
                    l_id = page.getID(c, appendAnyway=True)

            localJS = localJS.replace(ActionUrl.TAG_CUSTOM, self.clickJsCustom)
        else:
            listVA = []
            for va in self.jsVarArgs:
                if isinstance(va, (Component)):
                    listVA.append(va.getID())
                else:
                    listVA.append(va)

            localJS = self.clickJs % tuple(listVA)

        if self.useQuote:
            localJS = '"' + localJS + '"'

        return localJS

    def setEvent(self, event):
        self.event = event

    def setOperation(self, operation):
        self.operation = operation

    def setObject(self, obj):
        self.object = obj

    def setParams(self, params, *arg):
        self.params = params
        self.paramsVarArgs = arg

    def setClickJs(self, clickJs, *arg):
        self.custom = True
        self.appendCustom = False
        self.clickJs = clickJs
        self.jsVarArgs = arg

    def appendClickJs(self, clickJs, var_arg):
        self.custom = False
        self.appendCustom = True
        self.clickJsCustom = clickJs
        self.jsVarArgsCustom = var_arg

    def setUseQuote(self, useQuote):
        self.useQuote = useQuote

    def setRequestConfirmation(self, confirmation=False):
        self.confirmation = confirmation

    def getActionUrl(self):
        actionURL = self.actionUrl.replace(ActionUrl.TAG_EVENT, self.getEvent())
        actionURL = actionURL.replace(ActionUrl.TAG_OPERATION, self.getOperation())
        actionURL = actionURL.replace(ActionUrl.TAG_OBJECT, self.getObject())
        return actionURL


"""
import jiphy
pycode = "getFromServer(%s, %s.getValue('%s'))"
paramsList.append(widget)
paramsList.append(widget)
paramsList.append(widget)

jsCode = jiphy.to.javascript(pycode)
logging.debug(jsCode)
"""


class Validator():
    TAG_TYPE = "$type$"
    TAG_ERROR_MESSAGE = "$errorMessage$"
    TAG_CONDITION = "$condition$"

    def __init__(self, baseRequest='manageRequest/'):
        self.validator = '{"validateOnChange":"true","type":"' + Validator.TAG_TYPE + '","errorMessage":"' + Validator.TAG_ERROR_MESSAGE + '","condition":"' + Validator.TAG_CONDITION + '"}'

        self.type = 'custom'
        self.errorMessage = 'what a terrible thing is appened!'
        self.condition = 'return value == true'

    def getType(self):
        return self.type

    def getErrorMessage(self):
        return self.errorMessage

    def getCondition(self):
        return self.condition

    def setType(self, type):
        self.type = type

    def setErrorMessage(self, errorMessage):
        self.errorMessage = errorMessage

    def setCondition(self, condition):
        self.condition = condition

    def getValidator(self):
        validator = self.validator.replace(Validator.TAG_TYPE, self.getType())
        validator = validator.replace(Validator.TAG_ERROR_MESSAGE, self.getErrorMessage())
        validator = validator.replace(Validator.TAG_CONDITION, self.getCondition())
        return validator

"""
    validators:[{
        type: "custom",
        condition: "return value == true",
        errorMessage: "You must accept the terms of use to continue"
    }]
"""

class HorizontalLayout(Component):
    def __init__(self):
        Component.__init__(self)
        self.name = "hly"
        self.component = "var $name$ = isc.HLayout.create({$dict$})"

        # DEVO IMPOSTARE I DEFAULT **kwargs??? DA VEDERE

        self.removeProperty('membersMargin')
        self.removeProperty('layoutMargin')


class VerticalLayout(Component):
    def __init__(self):
        Component.__init__(self)
        self.name = "vly"
        self.component = "var $name$ = isc.VLayout.create({$dict$})"

        # DEVO IMPOSTARE I DEFAULT **kwargs??? DA VEDERE

        self.removeProperty('membersMargin')
        self.removeProperty('layoutMargin')


class Label(Component):
    def __init__(self, strInit=None):
        Component.__init__(self)
        self.name = "lab"
        self.component = "var $name$ = isc.Label.create({$dict$})"

        # DEVO IMPOSTARE I DEFAULT **kwargs??? DA VEDERE
        if strInit != None:
            self.setProperty('contents', strInit)
        else:
            self.setProperty('contents','contents')

        self.setProperty('border','1px solid #808080') # '1px solid #808080', '1px solid gold'
        self.setProperty('align','center')
        self.setProperty('backgroundColor','#e8deb1') # lightblue
        self.setProperty('styleName','blackText')

        #self.setProperty('align','center')
        #self.setProperty('padding','4')
        #self.setProperty('showEdges','true')
        #self.setProperty('keepInParentRect','true')
        #self.setProperty('canDragReposition','true')

        #self.setProperty('canDragResize','true')
        #self.setProperty('edgeMarginSize','10')
        #self.setProperty('resizeFrom',["B", "R", "BR"])
        #self.setProperty('resizeFrom',["H", "L", "HL"])

        self.removeProperty('membersMargin')
        self.removeProperty('layoutMargin')


class TextArea(Component):
    def __init__(self, strInit=None):
        Component.__init__(self)
        self.name = "txa"
        self.component = "var $name$ = isc.DynamicForm.create({$dict$})"

        # DEVO IMPOSTARE I DEFAULT **kwargs??? DA VEDERE
        if strInit != None:
            self.setProperty('title', strInit)
        else:
            self.setProperty('title', 'title')

        self.setProperty('editorType', 'textArea', 'fields')
        self.setProperty('width', '100%', 'fields')
        self.setProperty('value', 'Hello World!', 'fields')
        #self.setProperty('titleOrientation', 'top')
        #self.setProperty('titleWidth', '0')
        #self.setProperty('titleSuffix', '::')
        #self.setProperty('titlePrefix', '::')

        self.removeProperty('height')
        self.removeProperty('membersMargin')
        self.removeProperty('layoutMargin')


class Header(Component):
    def __init__(self):
        Component.__init__(self)
        self.name = "hdr"
        self.component = "var $name$ = isc.DynamicForm.create({$dict$})"

        # DEVO IMPOSTARE I DEFAULT **kwargs??? DA VEDERE
        self.setProperty('editorType', 'header', 'fields')
        self.setProperty('width', '100%', 'fields')
        self.setProperty('value', 'Hello World!', 'fields')

        self.removeProperty('height')
        self.removeProperty('membersMargin')
        self.removeProperty('layoutMargin')


class Spacer(Component):
    def __init__(self):
        Component.__init__(self)
        self.name = "spc"
        self.component = "var $name$ = isc.DynamicForm.create({$dict$})"

        # DEVO IMPOSTARE I DEFAULT **kwargs??? DA VEDERE
        self.setProperty('editorType', 'spacer', 'fields')

        self.removeProperty('height')
        self.removeProperty('width')
        self.removeProperty('value')
        self.removeProperty('membersMargin')
        self.removeProperty('layoutMargin')


"""
isc.DynamicForm.create({
    ID:"order",
    width:500,
    fields: [
        { type:"header", defaultValue:"Select an item for your Order" },
"""


class EditField(Component):      
    def __init__(self, strInit=None):
        Component.__init__(self)
        self.name = "edf"
        self.component = "var $name$ = isc.DynamicForm.create({$dict$})"

        # DEVO IMPOSTARE I DEFAULT **kwargs??? DA VEDERE
        if strInit != None:
            self.setProperty('title', strInit, 'fields')
        else:
            self.setProperty('title', 'title', 'fields')

        #self.setProperty('editorType', '', 'fields') #IN QUESTO CASO NON CI VA!!!
        self.setProperty('width', '100%', 'fields')
        self.setProperty('value', 'value', 'fields')


        self.removeProperty('height')
        self.removeProperty('membersMargin')
        self.removeProperty('layoutMargin')


class Link(Component):      
    def __init__(self, strInit=None):
        Component.__init__(self)
        self.name = "lnk"
        self.component = "var $name$ = isc.DynamicForm.create({$dict$})"

        # DEVO IMPOSTARE I DEFAULT **kwargs??? DA VEDERE
        self.setProperty('height', '30')

        if strInit != None:
            self.setProperty('title', strInit, 'fields')
        else:
            self.setProperty('title', 'title', 'fields')

        self.setProperty('editorType', 'link', 'fields')
        self.setProperty('width', '100%', 'fields')
        self.setProperty('value', 'value', 'fields')
        self.setProperty('linkTitle', 'linkTitle', 'fields')
        self.setProperty('target', '_self', 'fields')
        #Value	Description
        #_blank	Load in a new window
        #_self	Load in the same frame as it was clicked
        #_parent	Load in the parent frameset
        #_top	Load in the full body of the window
        #framename	Load in a named frame

        self.removeProperty('membersMargin')
        self.removeProperty('layoutMargin')


class PasswordField(Component):      
    def __init__(self, strInit=None):
        Component.__init__(self)
        self.name = "pwf"
        self.component = "var $name$ = isc.DynamicForm.create({$dict$})"

        # DEVO IMPOSTARE I DEFAULT **kwargs??? DA VEDERE
        if strInit != None:
            self.setProperty('title', strInit, 'fields')
        else:
            self.setProperty('title', 'title', 'fields')

        self.setProperty('editorType', 'password', 'fields')
        self.setProperty('width', '100%', 'fields')
        self.setProperty('value', 'Hello World!', 'fields')

        self.removeProperty('height')
        self.removeProperty('membersMargin')
        self.removeProperty('layoutMargin')


class DateField(Component):      
    def __init__(self, strInit=None):
        Component.__init__(self)
        self.name = "df"
        self.component = "var $name$ = isc.DynamicForm.create({$dict$})"

        # DEVO IMPOSTARE I DEFAULT **kwargs??? DA VEDERE
        if strInit != None:
            self.setProperty('title', strInit, 'fields')
        else:
            self.setProperty('title', 'title', 'fields')

        self.setProperty('editorType', 'date', 'fields')
        self.setProperty('width', '100', 'fields')
        #self.setProperty('value', '01/01/2016', 'fields')
        #self.setProperty('inputFormat', 'DMY', 'fields')
        #self.setProperty('maskDateSeparator', '/', 'fields')
        self.setProperty('dateFormatter', 'toEuropeanShortDate', 'fields')
        self.setProperty('useTextField', 'true', 'fields')

        self.removeProperty('height')
        self.removeProperty('membersMargin')
        self.removeProperty('layoutMargin')


class CheckBox(Component):      
    def __init__(self, strInit=None):
        Component.__init__(self)
        self.name = "ckb"
        self.component = "var $name$ = isc.DynamicForm.create({$dict$})"

        # DEVO IMPOSTARE I DEFAULT **kwargs??? DA VEDERE
        if strInit != None:
            self.setProperty('title', strInit, 'fields')
        else:
            self.setProperty('title', 'title', 'fields')

        self.setProperty('editorType', 'checkbox', 'fields')
        self.setProperty('width', '100%', 'fields')
        self.setProperty('value', 'true', 'fields')

        self.removeProperty('height')
        self.removeProperty('membersMargin')
        self.removeProperty('layoutMargin')


class RadioGroup(Component):      
    def __init__(self, strInit=None):
        Component.__init__(self)
        self.name = "rdg"
        self.component = "var $name$ = isc.DynamicForm.create({$dict$})"

        # DEVO IMPOSTARE I DEFAULT **kwargs??? DA VEDERE
        if strInit != None:
            self.setProperty('title', strInit, 'fields')
        else:
            self.setProperty('title', 'title', 'fields')

        self.setProperty('editorType', 'radioGroup', 'fields')
        self.setProperty('width', '100%', 'fields')
        self.setProperty('value', '', 'fields')

        #self.setProperty('Employed', 'Employed', 'valueMap')
        #self.setProperty('Unemployed', 'Unemployed', 'valueMap')

        self.removeProperty('height')
        self.removeProperty('membersMargin')
        self.removeProperty('layoutMargin')


class SelectField(Component):      
    def __init__(self, strInit=None):
        Component.__init__(self)
        self.name = "slf"
        self.component = "var $name$ = isc.DynamicForm.create({$dict$})"

        # DEVO IMPOSTARE I DEFAULT **kwargs??? DA VEDERE
        if strInit != None:
            self.setProperty('title', strInit, 'fields')
        else:
            self.setProperty('title', 'title', 'fields')

        self.setProperty('editorType', 'select', 'fields')
        self.setProperty('width', '100%', 'fields')
        self.setProperty('value', '', 'fields')
        #self.setProperty('allowEmptyValue', 'true', 'fields')
        #self.setProperty('changed', "window.alert('ciao')", 'fields')
        #changed: "form.getField('department').setValueMap(item.departments[value])",
        #addUnknownValues:false

        self.removeProperty('height')
        self.removeProperty('membersMargin')
        self.removeProperty('layoutMargin')


class RichEditor(Component):      
    def __init__(self):
        Component.__init__(self)
        self.name = "rce"
        self.component = "var $name$ = isc.RichTextEditor.create({$dict$})"

        # DEVO IMPOSTARE I DEFAULT **kwargs??? DA VEDERE
        self.setProperty('height', 155)
        self.setProperty('overflow', 'auto')
        #self.setProperty('canDragResize', 'true')
        self.setProperty('autoDraw', 'true')
        self.setProperty('value', '')

        #value:ajaxDefinition

        self.setProperty('fontControls', 'fontControls', 'controlGroups')
        self.setProperty('formatControls', 'formatControls', 'controlGroups')
        self.setProperty('styleControls', 'styleControls', 'controlGroups')
        self.setProperty('colorControls', 'colorControls', 'controlGroups')
        self.setProperty('bulletControls', 'bulletControls', 'controlGroups')

        self.removeProperty('membersMargin')
        self.removeProperty('layoutMargin')


class Button(Component):
    def __init__(self, strInit=None, actionUrl=None):
        Component.__init__(self)
        self.name = "btt"
        self.component = "var $name$ = isc.Button.create({$dict$})"

        if actionUrl != None:
            self.actionUrl.append(actionUrl)

        # DEVO IMPOSTARE I DEFAULT **kwargs??? DA VEDERE
        if strInit != None:
            self.setProperty('title', strInit)
        else:
            self.setProperty('title', 'title')

        self.setProperty('title', 'Button')
        self.setProperty('height', '25') #40
        self.setProperty('value', '')
        #self.setProperty('icon', 'icons/16/icon_add_files.png')


class ListGrid(Component):
    # https://smartclientexperience.wordpress.com/category/tutorials/
    #http://forums.smartclient.com/forum/technical-q-a/21393-listgrid-inline-edit-how-to-properly-handle-a-server-side-validation-error
    def __init__(self):
        Component.__init__(self)
        self.name = "lsg"
        self.component = "var $name$ = isc.ListGrid.create({$dict$})"

        # DEVO IMPOSTARE I DEFAULT **kwargs??? DA VEDERE
        self.setProperty('height', 300)
        self.setProperty('alternateRecordStyles', 'true')
        self.setProperty('emptyCellValue', '-NULL-')
        self.setProperty('autoFetchData', 'true')
        self.setProperty('autoFitWidthApproach', 'true')
        self.setProperty('autoFitData', 'horizontal')

        #self.setProperty('sortFieldNum', 0)
        self.setProperty('sortField', 'name')

        self.setProperty('dataPageSize', 20)
        self.setProperty('cellHeight', 25)
        self.setProperty('headerHeight', 30)

        #self.setProperty('canEdit', 'true')
        #self.setProperty('showFilterEditor', 'true')

        #self.setProperty('dataSource', supplyItem)
        #self.setProperty('canDragRecordsOut', 'true')
        #self.setProperty('canAcceptDroppedRecords', 'true')
        #self.setProperty('canReorderRecords', 'true')
        #self.setProperty('showHeader', 'false')
        #self.setProperty('showEdges', 'true')
        #self.setProperty('border', '0px')
        #self.setProperty('bodyStyleName', 'normal')
        #self.setProperty('leaveScrollbarGap', 'false')

"""
        dragDataAction: "copy"

strJSP = '%s.invalidateCache(); %s.fetchData();' % (g1.getID(), g1.getID())

click: function (record) {
isc.say ("ID:" + record.id + "Name:" + record.Name);
}
showFilterEditor: true

isc.FilterBuilder.create({
    ID:"advancedFilter",
    dataSource:"countryDS"
});
"""


class FileUpload(Component): 
    # https://smartclientexperience.wordpress.com/category/tutorials/
    #http://forums.smartclient.com/forum/technical-q-a/21393-listgrid-inline-edit-how-to-properly-handle-a-server-side-validation-error
    def __init__(self, actionUrl=None):
        Component.__init__(self)
        self.name = "fup"
        self.component = "var $name$ = isc.DynamicForm.create({$dict$})"

        if actionUrl != None:
            self.actionUrl.append(actionUrl)

        # DEVO IMPOSTARE I DEFAULT **kwargs??? DA VEDERE
        self.setProperty('canSubmit', 'true')
        self.setProperty('action', 'manageFileUpload/da_cambiare')
        self.setProperty('target', '_blank', 'fields')
        #Value	Description
        #_blank	Load in a new window
        #_self	Load in the same frame as it was clicked
        #_parent	Load in the parent frameset
        #_top	Load in the full body of the window
        #framename	Load in a named frame


        self.setProperty('name', 'UploadFile', 'fields', 0)
        self.setProperty('type', 'UploadItem', 'fields', 0)
        self.setProperty('required', 'true', 'fields', 0)
        self.setProperty('width', '100%', 'fields', 0)

        self.setProperty('name', 'submit', 'fields', 1)
        self.setProperty('type', 'submit', 'fields', 1)
        self.setProperty('width', '100%', 'fields', 1)


"""
var fsquery = "abcd";
var emailId = "as@gmail.com";
var portalPsswd = "password";
var projectId = "123";
var kbUrl = "some url which will consume form post parameters";
var pv="1.2",pn="ADA";

this.kbform=isc.DynamicForm.create({
width: 300,
fields: [
{type: "hiddenitem", name: "EMAIL_ID", defaultValue:emailId },
{type: "hiddenitem", name: "PORTAL_PASSWORD", defaultValue:portalPsswd},
{type: "hiddenitem", name: "PROJECT_ID", defaultValue:projectId},
{type: "hiddenitem", name: "FSQUERY", defaultValue:fsquery},
{type: "hiddenitem", name: "PRODUCT_VERSION", defaultValue:pv},
{type: "hiddenitem", name: "PRODUCT_NAME", defaultValue:pn},
{type: "hiddenitem", name: "ORIGIN", defaultValue:"Administrator"},
{type: "submit", name: "submit", defaultValue: "submit"}
],
action: kbUrl,
target: "_blank",
method: "POST",
canSubmit: true
});

this.kbform.submit();
isc.DynamicForm.create({
    fields:[
            {
            name:"UploadItem0", 
            type:"upload"
            _constructor:"UploadItem"
            },
            {
            title:"UploadFile", 
            name:"btnMnGb_curve",
            _constructor:"ButtonItem",
            canSubmit:true,
            click:"disp()"
            }
    ],
    encoding:"multipart",
    canSubmit:true,
    action:"http://localhost/process.aspx",
    ID:"DynamicForm0",
    autoDraw:false
})


isc.DynamicForm.create({
    fields:[
            {
            name:"UploadItem0", 
            _constructor:"UploadItem"
            },
            {
            title:"UploadFile", 
            name:"btnMnGb_curve",
            _constructor:"ButtonItem",
            canSubmit:true,
            click:"disp()"
            }
    ],
    encoding:"multipart",
    canSubmit:true,
    action:"ftp://filehosting.net",
    ID:"DynamicForm0",
    autoDraw:false
})

function disp(){
      DynamicForm0.submitForm();
      alert("File Uploaded");
}

isc.VLayout.create({
    members:[
        DynamicForm0
    ],
    height:"100%",
    width:"100%",
    autoDraw:true
})

"""


class DataSource(Component):      
    def __init__(self, actionUrl=None):
        Component.__init__(self)
        self.name = "dts"
        self.component = "var $name$ = isc.RestDataSource.create({$dict$})"

        # DEVO IMPOSTARE I DEFAULT **kwargs??? DA VEDERE
        self.setProperty('dataFormat', 'json')

        if actionUrl != None:
            self.actionUrl.append(actionUrl)

        """
        # definisco l'actionURL
        if self.actionUrl == None:
         logging.debug("*** DATASOURCE ***********************************************************")
         logging.debug(".....------*****||||||     self.actionUrl = NULL    ||||||*****------....."
         self.actionUrl = ActionUrl()

         actionURL = ActionUrl()
         actionURL.setEvent('lg')
         actionURL.setOperation('read')
         actionURL.setObject('"user"')

        self.actionUrl.setOperation('read')
        actUrl = self.actionUrl.getBaseRequest() + self.actionUrl.getActionUrl()
        self.dict['fetchDataURL'] = actUrl

        self.actionUrl.setOperation('create')
        actUrl = self.actionUrl.getBaseRequest() + self.actionUrl.getActionUrl()
        self.dict['addDataURL'] = actUrl

        self.actionUrl.setOperation('update')
        actUrl = self.actionUrl.getBaseRequest() + self.actionUrl.getActionUrl()
        self.dict['updateDataURL'] = actUrl

        self.actionUrl.setOperation('delete')
        actUrl = self.actionUrl.getBaseRequest() + self.actionUrl.getActionUrl()
        self.dict['removeDataURL'] = actUrl
        """

        #<field name="file"          type="binary"   title="File"/>
        #self.dict['willHandleError'] = 'true'
        #self.dict['handleError'] = 'function(response,request){alert(response.data);}'
        #del self.dict['members']



"""
StackPanel

isc.ListGrid.create({
    ID: "countryList",
    width:1500, height:224, alternateRecordStyles:true,
    data: sampleData,
    fields:[
        {name:"id", title:"Id"},
        {name:"name", title:"Name"},
        {name:"version", title:"Version"},
        {name:"release", title:"Release"},
    ],

    canReorderFields: true,
    selectionChanged: "someFunction(this.getSelection().getId())"
    recordClick: function (viewer, record, recordNum, field, fieldNum, value, rawValue) {
        alert('hi there' + record.name);
    }   
    click: function (record) {
        isc.say ("ID:" + record.id + "Name:" + record.Name); 
    }
    click: function (x) {
        alert('hi there' + x)
    }
})


validators:[
                {type:"integerRange", min:1}
            ]
            
function () {
   var data = "TEST DATI in ingresso";
   RPCManager.sendRequest({ data: data, callback: "myCallback(data)", actionURL: "tryForBelieve"});
}


isc.DataSource.create({
    ID: "ds",
    dataFormat: "json",
    dataURL: "/rest/hoge",
    fields: [
        { name: "id", title: "ID" },
        { name: "name", title: "Name" }
    ]
})

RPCManager.sendRequest({
    httpMethod: "POST",
    actionURL: "/rest/addUser",
    params: {
        userId: 1,
        userName: "aaa",
        userUserName: "aaa"
    },
    paramsOnly: true,
})



isc.DataSource.create({
    ID: "hogeDS",
    dataFormat: "json",
    dataURL: "/rest/hoge"
    fields: [
        { name: "id", title: "ID" },
        { name: "name", title: "Name" }
    ]
})

isc.ListGrid.create({
    ID: "hogeList",
    width: "100%", height: 500,
    dataSource: hogeDS,
    autoFetchData: true
})




var button = isc.IButton.create({
    title: "hogehoge"
});

button.click = function() {
    alert("hoge!!!");
};


isc.Button.create({
                    autoDraw: false,
                    width: 150,
                    title: "All Blank Descriptions",
                    click : function () {
                        listGrid.resizeField(0, 340);
                        listGrid.setData(resultSet.findAll('SKU',['45300','135900','951300','1089400','1090500']));
                    }
                })

var et_8 = isc.RichTextEditor.create({
            autoDraw:false,
            ID:"contentEditor",
            height:155,
            overflow:"hidden",
            canDragResize:true,
            controlGroups:["fontControls", "formatControls", "styleControls", "colorControls", "bulletControls"],
            value:ajaxDefinition
        });

var et_8 = isc.RichTextEditor.create({
      'canDragResize': 'true', 
      'value': 'ajaxDefinition', 
      'height': 155, 
      'controlGroups': ['fontControls', 'formatControls', 'styleControls', 'colorControls', 'bulletControls']
      'overflow': 'hidden', 
      'ID': 'Name_et_8', 
      'autoDraw': 'false'
      });

isc.DynamicForm.create({
    ID: "boundForm",
    colWidths: [100, 200],
    dataSource: "users",
    useAllDataSourceFields: true,
    fields: [
        {type:"header", defaultValue:"Registration Form"},
        {name: "password"},
        {name: "password2", title: "Password Again", type: "password", required: true, 
         wrapTitle: false, length: 20, validators: [{
             type: "matchesField",
             otherField: "password",
             errorMessage: "Passwords do not match"
         }]
        },
        {name: "acceptTerms", title: "I accept the terms of use.", type: "checkbox", width:150,
         defaultValue:false,
         validators:[{
            type:"custom",
            condition:"return value == true",
            errorMessage:"You must accept the terms of use to continue"
         }]
        },
        {name: "validateBtn", title: "Validate", type: "button", click: "form.validate()"}
        validators:[
                {type:"integerRange", min:1}
            ]
        validators:[
                {type:"integerRange", min:1}
            ]
    ],
    values : {
        firstName: "Bob",
        email: "bob@.com",
        password: "sekrit",
        password2: "fatfinger"
    }
});
"""      



class Window(Component):
    def __init__(self, strInit=None):
        Component.__init__(self)
        self.name = "win"
        self.component = "var $name$ = isc.Window.create({$dict$})"

        # DEVO IMPOSTARE I DEFAULT **kwargs??? DA VEDERE
        if strInit != None:
            self.setProperty('title', strInit)
        else:
            self.setProperty('title', 'title')

        self.setProperty('autoDraw', 'false')
        #self.setProperty('autoSize', 'true')
        #self.setProperty('autoCenter', 'true')
        self.setProperty('canDragReposition', 'true')
        self.setProperty('canDragResize', 'true')
        #self.setProperty('isModal', 'true')
        #self.setProperty('showModalMask', 'true')
        #self.dict['closeClick'] = 'true'

        self.removeProperty('width')
        self.removeProperty('height')
        self.removeProperty('membersMargin')
        self.removeProperty('layoutMargin')

"""
isc.Window.create({
    ID: "modalWindow",
    title: "Modal Window",
    autoSize:true,
    autoCenter: true,
    isModal: true,
    showModalMask: true,
    autoDraw: false,
    closeClick : function () { touchButton.setTitle('Touch This'); this.Super("closeClick", arguments)},
    items: [
        isc.DynamicForm.create({
            autoDraw: false,
            height: 48,
            padding:4,
            fields: [
                {name: "field1", type: "select", valueMap: ["foo", "bar"]},
                {name: "field2", type: "date"},
                {type: "button", title: "Done",
                 click: "modalWindow.hide();touchButton.setTitle('Touch This')" }
            ]
        })
    ]
});


isc.Label.create({
    ID: "theLabel",
    canFocus: true,
    showEdges: true,
    padding:4,
    contents: "Click me, then move me with arrow keys.",
    keyPress : function () {
        var left = this.getLeft();
        var top = this.getTop();
        switch (isc.EventHandler.getKey()) {
            case "Arrow_Left":
                left -= 10; break;
            case "Arrow_Right":
                left += 10; break;
            case "Arrow_Up":
                top -= 10; break;
            case "Arrow_Down":
                top += 10; break;
            default : return;
        }

        // don't go out of bounds
        if (left < 0) left = 0;
        if (top < 0) top = 0;

        this.setLeft(left);
        this.setTop(top);
    }
});


"""




class SectionStack(Component):      
    def __init__(self):
        Component.__init__(self)
        self.name = "sst"
        self.component = "var $name$ = isc.SectionStack.create({$dict$})"

        # DEVO IMPOSTARE I DEFAULT **kwargs??? DA VEDERE
        self.setProperty('visibilityMode', 'multiple')
        self.setProperty('animateSections', 'true')
        self.setProperty('overflow', 'hidden')
        #self.setProperty('border', '1px solid blue')
        #self.dict['closeClick'] = 'true'



"""
isc.SectionStack.create({
    sections:[
        { items:listGrid, title:"Monitors", controls:[addButton, removeButton], expanded:true },
        { items:statusReport, title:"Status", controls:systemSelector, expanded:true }
    ],
    visibilityMode:"multiple",
    animateSections:true,
    height:400,
    width:300,
    overflow:"hidden"
})
"""



class SplitPane(Component):      
    def __init__(self):
        Component.__init__(self)
        self.name = "spp"
        self.component = "var $name$ = isc.SplitPane.create({$dict$})"

        # DEVO IMPOSTARE I DEFAULT **kwargs??? DA VEDERE
        self.setProperty('navigationTitle', 'navigationTitle')
        self.setProperty('autoDraw', 'false')
        self.setProperty('showLeftButton', 'true')
        self.setProperty('showRightButton', 'true')
        self.setProperty('border', '1px solid blue')

        self.setProperty('detailPane', 'true')
        self.setProperty('listPane', 'true')
        self.setProperty('navigationPane', 'true')
        self.setProperty('autoNavigate', 'true')
        #self.dict['closeClick'] = 'true'

        self.removeProperty('width')
        self.removeProperty('height')
        self.removeProperty('membersMargin')
        self.removeProperty('layoutMargin')


"""
var splitPane = isc.SplitPane.create({
        autoDraw:false,
        navigationTitle:"Categories",
        showLeftButton:false,
        showRightButton:false,
        border:"1px solid blue",
        
        detailPane:detailPane,
        listPane:listPane,
        navigationPane:navigationPane,
        autoNavigate:true,
        listPaneTitleTemplate:"${record.categoryName}",
        detailPaneTitleTemplate:"${index + 1} of ${totalRows}"
    });




validatori???

isc.DynamicForm.create({
    width: 300,
    fields: [
        {title:"Item", type:"text",
         change : function (form, item, newValue, oldValue) {
             if (!isc.isA.String(newValue) || newValue.length < 3) return;
             // Obviously not a realistic transform, but just to demonstrate 'setSelectionRange' plus value change:
             var currentRange = this.getSelectionRange();
             var modifiedValue = newValue.substring(0,3) + ", " + newValue.substring(3);
             this.setValue(modifiedValue);
             this.setSelectionRange(currentRange[0],currentRange[1]);

         }
        }
    ]
});

myUsers.fetchData({ userId : "fred" }, "myForm.setValues(data)");

or

myUsers.fetchData({ userId : "fred" }, function (dsResponse, data, dsRequest) {
                                              myForm.setValues(data);
                                            });


    function refreshdata(t_ms, event, component){
        //btt_39.click();
        event()
        if (t_ms != -1) {
            isc.Timer.setTimeout("refreshdata("+t_ms.toString()+", "+component+"."+event.name+", '"+component+"')", t_ms);
        }
    };
    refreshdata(5000, btt_39.click, 'btt_39');



VALIDATORE
isc.DynamicForm.create({
  ID:"myForm",
  dataSource:"myDataSource",
  fields:[
    {name:"firstName",
      title:"First Name",
      width:100,

      transformInput: function(form, item, value, oldValue) {return value.toUpperCase()}
    },
    .... more fields
  ]
})


isc.Button.create({
    left: 200,
    autoFit: true,
    title: "CSS Button",
    icon: "icons/16/icon_add_files.png"
});


isc.ImgButton.create({
    left: 400,
    width:18,
	height:18,
	src:"[SKIN]/ImgButton/button.png"
});


isc.Img.create({
    ID:"widget",
    left:200,
    top:75,
    width:100,
    height:100,
    src:"other/yinyang.gif",
    contextMenu: mainMenu
});
"""



class MainMenu(Component):
    def __init__(self, strInit=None):
        Component.__init__(self)
        self.name = "mmn"
        self.component = "var $name$ = isc.MenuButton.create({$dict$})"

        if strInit != None:
            self.setProperty('title', strInit)
        else:
            self.setProperty('title', 'title')

        self.setProperty('styleName', 'CPmenuTable')
        self.setProperty('baseStyle', 'CPmenuTable')

        self.removeProperty('width')
        self.removeProperty('height')
        self.removeProperty('membersMargin')
        self.removeProperty('layoutMargin')


class MenuLink(Component):
    def __init__(self, strInit=None):
        Component.__init__(self)
        self.name = "men"
        self.component = "var $name$ = isc.Menu.create({$dict$})"

        if strInit != None:
            self.setProperty('title', strInit)
        else:
            self.setProperty('title', 'title')


        self.removeProperty('width')
        self.removeProperty('height')
        self.removeProperty('membersMargin')
        self.removeProperty('layoutMargin')

"""
isc.Menu.create({
    ID:"sizeMenu",
    autoDraw:false,
    data:[
        {title:"Small", checkIf:"widget.width == 50",
         click:"widget.animateResize(50,50)"},
        {title:"Medium", checkIf:"widget.width == 100",
         click:"widget.animateResize(100,100)"},
        {title:"Large", checkIf:"widget.width == 200",
         click:"widget.animateResize(200,200)"}
    ],
    width:150
});


isc.Menu.create({
    ID:"moveMenu",
    autoDraw:false,
    width:150,
    data:[
        {title:"Up", click:"widget.animateMove(widget.getLeft(),widget.getTop()-20)"},
        {title:"Right", click:"widget.animateMove(widget.getLeft()+20,widget.getTop())"},
        {title:"Down", click:"widget.animateMove(widget.getLeft(),widget.getTop()+20)"},
        {title:"Left", click:"widget.animateMove(widget.getLeft()-20,widget.getTop())"}
    ]
});

isc.Menu.create({
    ID:"mainMenu",
    width:150,
    data:[
        {title:"Visible", checkIf:"widget.isVisible()",
         click:"widget.isVisible() ? widget.animateHide('fade') : widget.animateShow('fade')"
        },
        {isSeparator:true},
        {title:"Size", submenu:sizeMenu, enableIf:"widget.isVisible()"},
        {title:"Move", submenu:moveMenu, enableIf:"widget.isVisible()"},
        {isSeparator:true},
        {title:"Reset",
            click:"widget.animateRect(200,75,100,100);widget.animateShow('fade')",
            icon:"other/yinyang.gif",
            iconWidth:20,
            iconHeight:20
        }
    ]
});

isc.MenuButton.create({
    ID:"mainMenuButton",
    title:"Widget",
    width:150,
    menu:mainMenu
});


isc.Img.create({
    ID:"widget",
    left:200,
    top:75,
    width:100,
    height:100,
    src:"other/yinyang.gif",
    contextMenu: mainMenu
});


isc.HTMLPane.create({
width:"100%",
contentsURL:pagePath,
contentsType: 'page',
overflow:"auto",
styleName:"defaultBorder"
})


isc.Canvas.create({
	        ID: "uploadFormIframe",
	        contents: "<iframe name=\"uploadFormIframe\">Chandra</iframe>",
	        autoDraw: true,
	        visibility: "hidden"
	      });
"""


class HTMLPane(Component):
    def __init__(self):
        Component.__init__(self)
        self.name = "htmlp"
        self.component = "var $name$ = isc.HTMLPane.create({$dict$})"

        self.setProperty('contents', "<iframe name='myIframe' width='100%' height='100%'>HTMLPane</iframe>")
        self.setProperty('contentsType', 'page')
        self.setProperty('overflow', 'auto')
        self.setProperty('styleName', 'defaultBorder')
        self.setProperty('width', '100%')
        self.setProperty('height', '200')


class Canvas(Component):
    def __init__(self):
        Component.__init__(self)
        self.name = "cvs"
        self.component = "var $name$ = isc.Canvas.create({$dict$})"

        self.setProperty('contents', "<iframe name='myIframe' width='100%' height='100%'>Canvas</iframe>")
        self.setProperty('autoDraw', 'true')
        self.setProperty('visibility', 'auto')

        self.removeProperty('height')
        self.removeProperty('membersMargin')
        self.removeProperty('layoutMargin')


class ViewLoader(Component):
    def __init__(self):
        Component.__init__(self)
        self.name = "vwl"
        self.component = "var $name$ = isc.ViewLoader.create({$dict$})"

        # DEVO IMPOSTARE I DEFAULT **kwargs??? DA VEDERE
        self.setProperty('autoDraw', 'false')
        self.setProperty('loadingMessage', 'Uploading file')
        #self.dict['title'] = 'Upload window'
        #self.dict['show'] = 'false'
        #self.dict['autoSize'] = 'true'
        #self.dict['autoCenter'] = 'true'
        #self.dict['isModal'] = 'true'
        #self.dict['showModalMask'] = 'true'
        #self.dict['canDragReposition'] = 'true'
        #self.dict['canDragResize'] = 'true'
        #self.dict['closeClick'] = 'true'

        self.removeProperty('width')
        self.removeProperty('height')
        self.removeProperty('membersMargin')
        self.removeProperty('layoutMargin')

"""
isc.ViewLoader.create({
                    autoDraw:false,
                    viewURL:isc.Page.getIsomorphicDocsDir()+"inlineExamples/advanced/loadedView.js",
                    loadingMessage:"Loading Grid.."
                })
"""


class Image(Component):
    def __init__(self):
        Component.__init__(self)
        self.name = "img"
        self.component = "var $name$ = isc.Img.create({$dict$})"

        # DEVO IMPOSTARE I DEFAULT **kwargs??? DA VEDERE
        #self.setProperty('appImgDir', 'default/32x32/')
        #self.setProperty('src', 'pdf.png')
        self.setProperty('left', '0')
        self.setProperty('top', '0')
        self.setProperty('width', '32')
        self.setProperty('height', '32')

        #self.setProperty('canDragReposition', 'true')
        #self.setProperty('keepInParentRect', 'true')
        #self.setProperty('dragAppearance', 'target')

        self.removeProperty('membersMargin')
        self.removeProperty('layoutMargin')
"""
isc.Img.create({
    ID: "myImage",
    left:120, top:20, width:48, height:48,
    appImgDir: "pieces/48/",
    src: "star_grey.png"
})
"""


class PickList(Component):
    def __init__(self):
        Component.__init__(self)
        self.name = "pkl"
        self.component = "var $name$ = isc.DynamicForm.create({$dict$})"

        # DEVO IMPOSTARE I DEFAULT **kwargs??? DA VEDERE
        #self.setProperty('appImgDir', 'default/32x32/')
        #self.setProperty('src', 'pdf.png')
        self.setProperty('title', 'title', 'fields', 0)
        self.setProperty('type', 'select', 'fields', 0)
        self.setProperty('width', '100%', 'fields', 0)
        #self.setProperty('pickListWidth', '400', 'fields', 0)
        #self.setProperty('optionDataSource', dsObj, 'fields', 0)
        #self.setProperty('displayField', 'itemName', 'fields', 0)
        self.setProperty('multiple', 'true', 'fields', 0)
        self.setProperty('multipleAppearance', 'picklist', 'fields', 0)
        #self.setProperty('multipleAppearance', 'grid', 'fields', 0)
        #self.setProperty('pickListFields', [{'name':'itemName'},{'name':'units'},{'name':'unitCost'}], 'fields', 0)
        #self.setProperty('values', "Cat, Dog", 'fields', 0)


        self.removeProperty('height')
        self.removeProperty('membersMargin')
        self.removeProperty('layoutMargin')


"""

isc.DynamicForm.create({
    ID:"exampleForm",
    width:300,
    fields: [
        {
            name:"itemID",
            type:"select",
            width:240,
            title:"Item",
            optionDataSource:"supplyItem",
            valueField:"SKU",
            displayField:"itemName",
            pickListWidth:450,
            pickListFields: [
                { name: "itemName" },
                { name: "units" },
                { name: "unitCost" }
            ]
        }
    ]
});
"""
