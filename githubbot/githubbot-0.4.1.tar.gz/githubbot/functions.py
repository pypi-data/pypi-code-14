import configparser
import json
import re
import requests

URL = "https://api.github.com"

class MyException(Exception):
    def __init__(self, messageError):
        self.messageError = messageError

    def __str__(self):
        return self.messageError 


class APIConnection():
    def __init__(self, session, userName, repoName):
        self.session = session
        self.userName = userName
        self.repoName = repoName

def getToken(authFileName, type):
    config = configparser.ConfigParser()
    try:
        config.read(authFileName)
        token = config['github'][type]
    except KeyError:
        raise MyException("An error occured while opening or reading authorization configure file.\n")
    return token

def loadLocalLabels(confFilePath):
    config = configparser.ConfigParser()
    config.read(confFilePath)
    labelsSections = config.sections()
    if labelsSections == []:
        raise MyException("An error occured while opening or reading local label configure file.\n")
    labels = []
    for section in labelsSections:

        label = {'section': section, 'name': config[section]['name'], 'color': config[section]['color'], 'regex' : config[section]['regex'], 'defaultLabel' : config[section]['defaultLabel']}
        labels.append(label)
    return labels

def initSession(authFileName, tokenType):
    token = getToken(authFileName, tokenType)
    session = requests.Session()
    session.headers = {'Authorization': 'token ' + token, 'User-Agent': 'Python'}
    return session

def testConnection(apiConn):
    test_connection = apiConn.session.get("https://github.com")
    if not test_connection.ok:
        raise MyException("An error occured while connection to GitHub server. Error code " + str(response.status_code) + "\n")
    getUrl = URL + "/repos/" + apiConn.userName + "/" + apiConn.repoName
    test_user_repo_existence = apiConn.session.get(getUrl)
    if not test_user_repo_existence.ok:
        raise MyException("An error occured while connecting to repository. Try to verify repository repository owner or repository name. Error code " + str(response.status_code) + "\n")


def getIssues(apiConn):
    getUrl = URL + "/repos/" + apiConn.userName + "/" + apiConn.repoName + "/issues"
    response = apiConn.session.get(getUrl)
    if not response.ok:
        raise MyException("An error occured while getting issues from repository. Error code " + str(response.status_code) + "\n")
    return response

def getAllLabels(apiConn):
    getUrl = URL + "/repos/" + apiConn.userName + "/" + apiConn.repoName + "/labels"
    response = apiConn.session.get(getUrl)
    if not response.ok:
        raise MyException("An error occured while getting all labels from repository. Error code " + str(response.status_code) + "\n")
    return response

def createRemoteLabel(apiConn, newLabel):
    payload = {'name':newLabel['name'], 'color':newLabel['color']}
    postUrl = URL + "/repos/" + apiConn.userName + "/" + apiConn.repoName + "/labels"
    r = apiConn.session.post(postUrl, data=json.dumps(payload))
    return r.ok

def updateLabelColor(apiConn, localLabel):
    lName = localLabel['name']
    lColor = localLabel['color']
    patchUrl = URL + "/repos/" + apiConn.userName + "/" + apiConn.repoName + "/labels/" + lName
    payload = {'name' : lName, 'color': lColor}
    r = apiConn.session.patch(patchUrl, data=json.dumps(payload))
    return r.ok

def isPullRequest(issue):
    return 'pull_request' in issue.keys()

def addLabelToIssue(apiConn, issue, labelsNameList):
    issueNumber = issue['number']
    postUrl = URL + "/repos/" + apiConn.userName + "/" + apiConn.repoName + "/issues/" + str(issueNumber) + "/labels"
    r = apiConn.session.post(postUrl, data=json.dumps(labelsNameList))
    return r.ok

def isLabelable(issue, superswitch):
    if superswitch == 0:
        return True
    isPullReq = isPullRequest(issue)
    if isPullReq and superswitch == 2:
        return True
    if not isPullReq and superswitch == 1:
        return True
    return False

def labelIssue(apiConn, issue, confFilePath):
    issueNumber = issue['number']
    localLabels = loadLocalLabels(confFilePath)
    issueTitle = issue['title']
    labelNameList = []
    defaultLabel = None
    for label in localLabels:
        makeLabelRemotelyPresent(apiConn, label)
        if label['defaultLabel'] == 'True':
            defaultLabel = label
            continue
        regExpr = label['regex']
        if re.search(regExpr, issueTitle, re.IGNORECASE) != None:
            labelNameList.append(label['name'])
    if labelNameList == []:
        labelNameList.append(defaultLabel['name'])
    print("Labeling issue " + str(issueNumber) + " with " + str(labelNameList))
    return addLabelToIssue(apiConn, issue, labelNameList)
        

def makeLabelRemotelyPresent(apiConn, localLabel):
    allRemoteLabels = getAllLabels(apiConn)
    exists = False
    for rLabel in allRemoteLabels.json():
        if rLabel['name'] == localLabel['name']:
            exists = True
            if rLabel['color'] != localLabel['color']:
                updateLabelColor(apiConn, localLabel)
            break
    if not exists:
        createRemoteLabel(apiConn, localLabel)
