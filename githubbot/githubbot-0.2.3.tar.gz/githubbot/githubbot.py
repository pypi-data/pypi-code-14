import click
import configparser
import getpass
import requests
import sys
import time

from githubbot import functions
from flask import Flask, render_template, request


app = Flask(__name__)

"""
    This constant needs to be set according to the context in which it is run.
"""
PATH_TO_WEBCONFIG = 'webconfig.cfg'


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

        session = functions.initSession(authFilePath, tokenType)
        self.apiConn = functions.APIConnection(session, repoOwner, repoName)

    def work(self):
        functions.testConnection(self.apiConn)
        while True:
            issues = functions.getIssues(self.apiConn)
            print("Got issues.")
            for issue in issues.json():
                issueNumber = issue['number']
                if functions.isLabelable(issue, self.superswitch) and issue['labels'] == []:
                    print("\tTrying to label this issue!")
                    functions.labelIssue(self.apiConn, issue, self.confFilePath)
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
            functions.testConnection(mBot.apiConn)
        except functions.MyException as my_error:
            sys.stderr.write(my_error.messageError)
        return mBot

@click.group()
def cli1():
    pass

@cli1.command()
def web():
    """Simple program that label new issues on GitHub using webhooks."""
    print("Flask application created: SUCCESS")
    app.run(debug=True)

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
    except functions.MyException as my_error:
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
    functions.labelIssue(bot.apiConn, data['issue'], bot.confFilePath)
    return 'success'

cli = click.CommandCollection(sources=[cli1, cli2])

def main():
    cli()
