import csv
import os
import json


class History():

    def __init__(self, path, storeLog=False, logPath=""):
        self.path = path
        self.storeLog = storeLog
        self.logPath = logPath
        self.history = []
        self.initFiles()
        self.getHistory()

    def createIfNonExistent(self, filepath):
        if(not os.path.isfile(filepath)):
            with open(filepath, "w") as myfile:
                pass

    def initFiles(self):
        self.createIfNonExistent(self.path)
        if (self.storeLog):
            self.createIfNonExistent(self.logPath)
    
    def getHistory(self):
        self.initFiles()
        with open(self.path, "r") as f:
            self.history = f.read().splitlines()

    def dictHash(self, d):
        return str(hash(frozenset(d.items())))

    def isPresent(self, d):
        if self.dictHash(d) in self.history:
            return True
        else:
            return False

    def makeOneLiner(self, what):
        return what.replace('\n', '').replace('\r', '')

    def appendLine(self, to, what):
        with open(to, 'a') as f:
            f.writelines(what)
            f.writelines('\n')

    def writeHistory(self, d):
        dictHist = self.makeOneLiner(self.dictHash(d))
        self.appendLine(self.path, dictHist)
        self.history.append(dictHist)

    def writeLog(self, d):
        self.appendLine(self.logPath,
                        self.makeOneLiner(str(json.dumps(d))))

    def putHistory(self, histDict, logDict=None):
        self.initFiles()
        self.writeHistory(histDict)
        if self.storeLog == True:
            if logDict==None:
                logDict={}
            self.writeLog(logDict)

