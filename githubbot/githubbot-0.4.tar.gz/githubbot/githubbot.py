import click
import configparser
import json
import getpass
import os
import re
import requests
import sys
import time

from flask import Flask, render_template, request

app = Flask(__name__)

"""
    This constant needs to be set according to the context in which it is run.
"""
PATH_TO_WEBCONFIG = 'webconfig.cfg'
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


class GitHubBot:
    instance = None

    def __init__(self, authFilePath, confFilePath, timeout, tokenType, repoOwner, repoName, defaultLabel, superswitch):
        """
        superswitch: 0 Label Issues & Pull_requests
                     1 Label Issues
                     2 Label Pull_requests
        """
        self.authFilePath = authFilePath
        self.confFilePath = confFilePath
        self.timeout = timeout
        self.tokenType = tokenType
        self.repoOwner = repoOwner
        self.repoName = repoName
        self.defaultLabel = defaultLabel
        self.superswitch = superswitch

        session = initSession(authFilePath, tokenType)
        self.apiConn = APIConnection(session, repoOwner, repoName)

    def work(self):
        testConnection(self.apiConn)
        while True:
            issues = getIssues(self.apiConn)
            print("Got issues.")
            for issue in issues.json():
                issueNumber = issue['number']
                if isLabelable(issue, self.superswitch) and issue['labels'] == []:
                    print("\tTrying to label this issue!")
                    labelIssue(self.apiConn, issue, self.confFilePath)
            time.sleep(self.timeout)

    def get_instance():
        if GitHubBot.instance == None:
            GitHubBot.instance = GitHubBot.init_gitHubBot()
        return GitHubBot.instance

    def init_gitHubBot():
        global PATH_TO_WEBCONFIG
        timeout = 0
        config = configparser.ConfigParser()
        config.read(PATH_TO_WEBCONFIG)
        webconfigKey = 'webconfig'
        try:
            authfile = config[webconfigKey]['authfile']
            configfile = config[webconfigKey]['configfile']
            tokenname = config[webconfigKey]['tokenname']
            repoowner = config[webconfigKey]['repoowner']
            repository = config[webconfigKey]['repository']
            defaultlabel = config[webconfigKey]['defaultlabel']
            superswitch = config[webconfigKey]['superswitch']
        except KeyError:
            print("An error occured while reading \"webconfig.cfg\".")
            exit()
        print("Reading config file: SUCCESS")
        try:
            mBot = GitHubBot(authfile, configfile, timeout, tokenname, repoowner, repository, defaultlabel, superswitch)
            testConnection(mBot.apiConn)
        except MyException as my_error:
            sys.stderr.write(my_error.messageError)
        return mBot

@click.group()
def cli1():
    pass

@cli1.command()
def web():
    """Simple program that label new issues on GitHub using webhooks."""
    print("Flask application created: SUCCESS")
    print("In __main__: " + os.path.abspath(__file__))
    app.run()

@click.group()
def cli2():
    pass

@cli2.command('console')
@click.option('--authfile', default='auth.cfg', help='Path to authorization file.')
@click.option('--configfile', default='configFile.cfg', help='Path to configure file.')
@click.option('--timeout', default=30, help='Number of secconds for checking new issues.')
@click.option('--tokenname', default="tokenRobot", help='Name of token in authfile.')
@click.option('--repoowner', prompt="Repository owner", help='Owner of the repository.')
@click.option('--repository', prompt="Repository name", help='Repository for automatic labeling.')
@click.option('--defaultlabel', default='NeedsLabel', help='Default label for not resolved issues.')
@click.option('--superswitch', default=1, help='Indicator whether to label issues, pull_requests or both.')
def bot(authfile, configfile, timeout, tokenname, repoowner, repository, defaultlabel, superswitch):
    """Simple program that label new issues on GitHub. AUTHFILE, REPOSITORY, REPOOWNER, CONFIGFILE, TOKENNAME, TIMEOUT, DEFAULTLABEL, SUPERSWITCH"""
    try:
        mBot = GitHubBot(authfile, configfile, timeout, tokenname, repoowner, repository, defaultlabel, superswitch)
        mBot.work()
    except MyException as my_error:
        sys.stderr.write(my_error.messageError)


@app.route('/')
def hello():
    return render_template('index.html')


@app.route('/hook', methods=['POST'])
def hook():
    data = request.get_json()
    bot = GitHubBot.get_instance()
    if bot == None:
        sys.stderr.write("An error occur while creating GitHubBot instance.")
        return
    labelIssue(bot.apiConn, data['issue'], bot.confFilePath)
    return 'success'

cli = click.CommandCollection(sources=[cli1, cli2])

def main():
    cli()

if __name__ == "__main__":
    main()


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
