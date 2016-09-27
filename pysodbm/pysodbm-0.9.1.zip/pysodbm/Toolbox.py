#!/usr/bin/env python
# -*- coding: utf-8 -*-


import base64
import calendar
import csv
import fnmatch
import hashlib
import inspect
import json
import logging
import os
import math
import shutil
import socket
import urllib
import urllib2
import urlparse
import random
import string
import pickle
import cPickle
import random
from operator import ior

import bs4
import dateutil.parser
import mechanicalsoup
import mechanize
import psutil
import subprocess
import platform
from json import encoder

__author__ = 'Marco'

import cgi
import time
from datetime import datetime, date, timedelta
from os import urandom

import locale
import threading

from datetime import datetime
from contextlib import contextmanager

LOG = logging.getLogger(__name__)

@contextmanager
def setlocale(name):
    saved = locale.setlocale(locale.LC_ALL, name)
    LOG.debug("locale saved: {lc}".format(lc=saved))
    LOG.debug("locale set: {lc}".format(lc=name))
    try:
        yield
    finally:
        LOG.debug("reset locale to: {lc}".format(lc=saved))
        locale.setlocale(locale.LC_ALL, saved)


def isWindows():
    return True if platform.system().lower() == "windows" else False


if isWindows():
    import win32gui
    import win32process
    import win32api

try:
    from PyQt4 import QtCore


    def qtSleep(sleepTime):
        sleepTime *= 1000
        time = QtCore.QTime()
        time.restart()
        while time.elapsed() < sleepTime:
            QtCore.QCoreApplication.processEvents(QtCore.QEventLoop.AllEvents, 50)
except:
    def qtSleep(sleepTime):
        time.sleep(sleepTime)


def loadAmazonConfigFor(conf=None, configName=None):
    if "amazonShipment" in conf["amazon"]:
        config = conf["amazon"]["amazonShipment"]
        if configName in config:
            config = config[configName]
            LOG.debug("Load config for {configName}".format(configName=configName))
        else:
            errorText = "Can't load config for {configName}".format(configName=configName)
            LOG.warning(errorText)
            raise Exception(errorText)

    else:
        errorText = "Can't load config for amazon"
        LOG.warning(errorText)
        raise Exception(errorText)

    return config


def dailTelephoneNumber(esgento=None, number="", extension=""):
    if esgento:
        number = number.strip()
        if number == "":
            return
        number = number.replace("!", "")
        number = number.replace(" ", "")
        number = number.replace(".", "")
        number = number.replace("-", "")

        if len(number) != 2:
            if not number.startswith("0"):
                number = "0" + number

        number = number.replace("+", "00")

        # dialPath = os.path.join(esgento.binDirectory, "dial.exe")
        # os.system("%s %s" % (dialPath, number))
        uri = "http://10.1.3.%s/command.htm?number=%s&outgoing_uri=URI" % (extension, number)
        # print uri
        br = mechanize.Browser()
        br.set_handle_robots(False)
        br.add_password(uri, "admin", "Am9elit0815")
        result = br.open(uri)
        # print result


def checkMD5(srcMD5, dstMD5):
    return True if srcMD5 == dstMD5 else False


def getFileMD5CheckSum(fileName):
    file2Check = open(fileName, "rb")
    fileData = file2Check.read()
    file2Check.close()

    return hashlib.md5(fileData).hexdigest()


def readMD5CheckSumFromFile(localMD5Path=None):
    if localMD5Path is not None:
        dstMD5File = open(localMD5Path, "rb")
        splitList = dstMD5File.readlines()

        return splitList[3].split(" ")[0]


def gerneratePassword(length=21):
    """Function to generate a password"""

    password = []
    specialCounter = 0

    char_set = {'small': 'abcdefghijklmnopqrstuvwxyz',
                'nums': '0123456789',
                'big': 'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
                'special': '!.,-@+'
                }

    while len(password) < length:
        while True:

            key = random.choice(char_set.keys())
            if key == "special":
                if specialCounter < 2:
                    specialCounter += 1
                    break
            else:
                break

        a_char = random.choice(char_set[key])
        if len(password) != 0:
            if a_char == password[-1]:
                continue
        password.append(a_char)

    return ''.join(password)


def factorToPercent(factor):
    return (factor - 1) * 100


def percentToFactor(percent):
    return (percent / 100) + 1


def roundPrice(price, roundFactor):
    if roundFactor == 0:
        return price

    return math.ceil(price / roundFactor) * roundFactor
    # return int(price / roundFactor) * roundFactor


def isEqual(a, b, tol=0.000001):
    if type(a) == float and type(b) == float:
        # result = abs(math.log(a) - math.log(b))
        ret = abs(a - b) <= tol
    else:
        ret = a == b
    return ret


def poundToKg(weight):
    return weight * 0.45359237


def loadLastTimeDateFromFile(path=""):
    if len(path) == 0:
        raise AttributeError("Please insert Path !")

    dateTimeFile = open(path, "r")
    dateInFile = dateTimeFile.read()
    dateTimeFile.close()

    return dateInFile


def saveStartDateToFile(path="", dateTimeStr=None):
    if len(path) == 0:
        raise AttributeError("Please insert Path !")

    if dateTimeStr is None:
        dateTimeStr = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    dateTimeFile = open(path, "w")
    dateTimeFile.write(unicode(dateTimeStr))
    dateTimeFile.close()


def replaceHTML(mstr):
    mstr = cgi.escape(mstr)
    mstr = mstr.encode("ascii", "xmlcharrefreplace")
    return mstr


def fixPhoneNumber(phoneNumberString):
    ret = phoneNumberString
    ret = ret.replace(" ", "")
    ret = ret.replace("(", "")
    ret = ret.replace(")", "")
    ret = ret.replace("-", "")
    return ret


def nowSeconds():
    n = datetime.now()
    mt = int((n - datetime(1970, 1, 1)).total_seconds())
    return mt


def now():
    mt = nowSeconds()
    return mysqlTimeStr(mt)


def nowDateTime():
    return datetime.now()


def emptyDateTime():
    return datetime(1, 1, 1, 0, 0, 0)


def utcNowSeconds():
    n = datetime.utcnow()
    mt = int((n - datetime(1970, 1, 1)).total_seconds())
    return mt


def utcNow():
    mt = utcNowSeconds()
    return mysqlTimeStr(mt)


def mysqlTimeStr(timeA):
    timeA = time.gmtime(timeA)
    ret = time.strftime("%Y-%m-%d %H:%M:%S", timeA)
    return ret


def dateTimeToBobDate(dateTime):
    """
    Konvertiert DateTime nach BobDate

    :param dateTime:
    :return: str
    """
    m = unicode(dateTime.replace(microsecond=0, second=0, minute=0, hour=0))
    m = time.strptime(m, "%Y-%m-%d %H:%M:%S")
    m = time.strftime("%d/%m/%Y", m)
    return m


def isoDateToDateTime(isoDate):
    """
    Konvertiert einen isoDate String (%Y-%m-%dT%H:%M:%S) nach datetime
    :param isoDate: str
    :return: datetime
    """
    return datetime.strptime(isoDate, "%Y-%m-%dT%H:%M:%S")


def dateTimeToIsoDate(dateTime):
    """
    Konvertiert datetim nach isoDate
    :param dateTime: datetime
    :return: isoDatetime
    """
    m = unicode(dateTime.replace(microsecond=0))
    m = time.strptime(m, "%Y-%m-%d %H:%M:%S")
    m = time.strftime("%Y-%m-%dT%H:%M:%S", m)
    return m


def isoDateTime(m):
    m = time.strptime(m, "%Y-%m-%d %H:%M:%S")
    m = time.strftime("%Y-%m-%dT%H:%M:%S", m)
    return m


def jsonDateTime(dt):
    return "{dt:%Y-%m-%dT%H:%M:%S}".format(dt=dt)


def jsonDate(dt):
    return "{dt:%Y-%m-%d}".format(dt=dt)


def fromJsonDateTime(j):
    return dateutil.parser.parse(j)


def mysqlStrToDateTime(dateStr):
    pattern = "%Y-%m-%d %H:%M:%S"
    return datetime.strptime(dateStr, pattern)


def dateToMysqlStr(dateObj):
    if type(dateObj) == str:
        return dateObj
    else:
        pattern = "%Y-%m-%d"
        return dateObj.strftime(pattern)


def timeToMysqlStr(timeObj):
    if type(timeObj) == str:
        return timeObj
    else:
        pattern = "%H:%M:%S"
        return timeObj.strftime(pattern)


def dateTimeToMysqlStr(datetimeObj):
    if type(datetimeObj) == str:
        return datetimeObj
    else:
        pattern = "%Y-%m-%d %H:%M:%S"
        return datetimeObj.strftime(pattern)


def dateToMysqlStr(dateObj):
    if type(dateObj) == str:
        return dateObj
    else:
        pattern = "%Y-%m-%d"
        return dateObj.strftime(pattern)


def generateTimeStamp(datetimeObj=None):
    if not datetimeObj:
        datetimeObj = datetime.now()
    pattern = "%Y_%m_%d-%H_%M_%S"
    return datetimeObj.strftime(pattern)


def addSuffixToFilename(fileName, suffix):
    parts = [fileName.split(".")[0] + "_" + suffix]
    parts.extend(fileName.split(".")[1:])
    fileName = ".".join(
        parts
    )
    return fileName


def decodeB64Pickle(value):
    return pickle.loads(base64.b64decode(value))


def encodeB64Pickle(value):
    return base64.b64encode(pickle.dumps(value))


def dateToDateTime(date):
    return datetime.combine(date, datetime.min.time())


def getLowestValueFromObjects(objects, attributeName, avoidValue=None):
    if len(objects) == 0:
        return None
    elif len(objects) == 1:
        return objects[0]
    else:
        ret = objects[0]
        if avoidValue is not None:
            for obj in objects:
                if getattr(obj, attributeName) != avoidValue:
                    ret = obj
                    break

        for obj in objects:
            if getattr(obj, attributeName) < getattr(ret, attributeName):
                if avoidValue is not None:
                    if getattr(obj, attributeName) != avoidValue:
                        ret = obj
                else:
                    ret = obj
        return ret


def getHighestValueFromObjects(objects, attributeName, avoidValue=None):
    if len(objects) == 0:
        return None
    elif len(objects) == 1:
        return objects[0]
    else:
        ret = objects[0]
        if avoidValue is not None:
            for obj in objects:
                if getattr(obj, attributeName) != avoidValue:
                    ret = obj
                    break

        for obj in objects:
            if getattr(obj, attributeName) > getattr(ret, attributeName):
                if avoidValue is not None:
                    if getattr(obj, attributeName) != avoidValue:
                        ret = obj
                else:
                    ret = obj
        return ret


def getMemoryUsage():
    ownPID = os.getpid()
    ownProcessInfo = psutil.Process(ownPID)
    ownMemoryUsage = ownProcessInfo.memory_info()[0]
    return ownMemoryUsage


def convertMySQLDateToISO(datum):
    t = datetime.strptime(datum, "%Y-%m-%d %H:%M:%S")
    return datetime.strftime(t, "%Y-%m-%dT%H:%M:%SZ")


def convertMySQLFromDateToISO(datum):
    if datum.endswith("Z"):
        datum = datum[:-1]
    t = datetime.strptime(datum, "%Y-%m-%dT%H:%M:%S")
    return datetime.strftime(t, "%Y-%m-%d %H:%M:%S")


def datetimeFromISO(datum):
    return datetime.strptime(datum, "%Y-%m-%dT%H:%M:%SZ")


def pNowSeconds():
    now = datetime.datetime.now()
    mt = int((now - datetime.datetime(1970, 1, 1)).total_seconds())
    return mt


def pNow():
    mt = pNowSeconds()
    return pMySQLTimeStr(mt)


def pUtcNowSeconds():
    now = datetime.utcnow()
    mt = int((now - datetime(1970, 1, 1)).total_seconds())
    return mt


def pUtcNow():
    mt = pUtcNowSeconds()
    return pMySQLTimeStr(mt)


def pMySQLTimeStr(timeA):
    timeA = time.gmtime(timeA)
    ret = time.strftime("%Y-%m-%d %H:%M:%S", timeA)
    return ret


def pISODateTime(m):
    m = time.strptime(m, "%Y-%m-%d %H:%M:%S")
    m = time.strftime("%Y-%m-%dT%H:%M:%S", m)
    return m


def unixTimeStampToDateTime(timeStamp):
    return datetime.utcfromtimestamp(timeStamp)


def checkPidFileExists(esgento, fileName):
    filePath = os.path.join(esgento.runDirectory, fileName)

    if os.path.isfile(filePath):
        return filePath
    else:
        return None


def writePidToFile(esgento, fileName):
    filePath = os.path.join(esgento.runDirectory, fileName)

    if not os.path.isfile(filePath):
        pid = os.getpid()
        fd = open(filePath, "w")
        fd.write(unicode(pid))
        fd.close()


def deletePidFile(esgento, fileName):
    filePath = os.path.join(esgento.runDirectory, fileName)

    if os.path.isfile(filePath):
        os.remove(filePath)


def executeCmd(cmd, callback=None, async=False):
    if not async:
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        for line in iter(p.stdout.readline, ""):
            if callback:
                callback(line.strip())
    else:
        p = subprocess.Popen(cmd, shell=True)


def getRunningProcesses(applicationName, cmdContains=None):
    ret = []
    cleanedRet = []
    pids = psutil.pids()
    for pid in pids:
        try:
            process = psutil.Process(pid)
            if process.name() == applicationName:
                ret.append(process)

        except:
            pass

    if cmdContains:
        for process in ret:
            if any(cmdContains in part for part in process.cmdline()):
                cleanedRet.append(process)
        return cleanedRet
    else:
        return ret


def get_hwnds_for_pid(pid):
    def callback(hwnd, hwnds):
        if win32gui.IsWindowVisible(hwnd) and win32gui.IsWindowEnabled(hwnd):
            _, found_pid = win32process.GetWindowThreadProcessId(hwnd)
            if found_pid == pid:
                hwnds.append(hwnd)
        return True

    hwnds = []
    win32gui.EnumWindows(callback, hwnds)
    return hwnds


def bring_hwnd_to_front(hwnd):
    win32gui.SetForegroundWindow(hwnd)
    win32gui.SetActiveWindow(hwnd)
    win32gui.ShowWindow(hwnd, 9)


def terminate_process(pid):
    PROCESS_TERMINATE = 1
    handle = win32api.OpenProcess(PROCESS_TERMINATE, False, pid)
    win32api.TerminateProcess(handle, -1)
    win32api.CloseHandle(handle)


class sqlDictValues(object):
    SQL = None

    @classmethod
    def load(cls, esgento=None):
        ret = {}
        if cls.SQL:
            r = esgento.dbQueryObject(cls.SQL)
            for i in r:
                key, value = cls.recordParser(i)
                ret[key] = value
        return ret

    @classmethod
    def recordParser(cls, record):
        """
        Muss überladen werden
        :param record:
        """
        key, value = None
        return key, value


def quoteURL(sourceURL):
    scheme, netloc, path, params, query, fragment = urlparse.urlparse(sourceURL)
    path = urllib.quote(path)
    quotedURL = urlparse.urlunparse(
        (scheme, netloc, path, urllib.quote(params), urllib.quote(query), urllib.quote(fragment)))
    return quotedURL


def getNetworkIp(URL="www.electronic-shop.lu"):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect((URL, 0))
    ret = s.getsockname()[0]
    s.close()
    return ret


def quickPickle(fileName, write, func, *args, **kwargs):
    if write:
        dirName = os.path.basename(fileName)
        if not os.path.exists(dirName):
            os.makedirs(dirName)
        data = func(*args, **kwargs)
        cPickle.dump(data, open(fileName, "wb"))
        return data
    else:
        if os.path.exists(fileName):
            return cPickle.load(open(fileName, "rb"))
        else:
            raise IOError("File %s not found." % fileName)


def startDatePreviousMonth(datum):
    month = datum.month - 1 if datum.month - 1 > 0 else 12
    year = datum.year - 1 if month == 12 else datum.year
    startdate = startDateMonth(year, month)
    return startdate


def startDateMonth(year, month):
    lastday = calendar.monthrange(year, month)[1]
    startdate = date(year, month, 1)
    return startdate


def endDatePreviousMonth(datum):
    month = datum.month - 1 if datum.month - 1 > 0 else 12
    year = datum.year - 1 if month == 12 else datum.year
    enddate = endDateMonth(year, month)
    return enddate


def endDateMonth(year, month):
    lastday = calendar.monthrange(year, month)[1]
    enddate = date(year, month, lastday)
    return enddate


def week_range(date):
    """Find the first/last day of the week for the given day.
    Assuming weeks start on Sunday and end on Saturday.

    Returns a tuple of ``(start_date, end_date)``.

    """
    # isocalendar calculates the year, week of the year, and day of the week.
    # dow is Mon = 1, Sat = 6, Sun = 7
    year, week, dow = date.isocalendar()

    # Find the first day of the week.
    if dow == 7:
        # Since we want to start with Sunday, let's test for that condition.
        start_date = date
    else:
        # Otherwise, subtract `dow` number days to get the first day
        start_date = date - timedelta(dow)

    # Now, add 6 for the last day of the week (i.e., count up to Saturday)
    end_date = start_date + timedelta(6)

    return (start_date, end_date)


def minutesToHourString(minutes):
    if minutes < 0:
        sign = "-"
        minutes = minutes * -1
    else:
        sign = "+"

    return "{sign}{hours}:{minutes:02}".format(
        sign=sign,
        hours=int(minutes / 60),
        minutes=minutes % 60
    )


def minutesToDaysString(minutes):
    tage = float(minutes) / float(480)
    return "{TAGE:.1f}".format(TAGE=tage) if tage != int(tage) else "{TAGE}".format(TAGE=int(tage))


def generateMonthCalendar(year=None, month=None):
    today = date.today()
    previousMonthCalendar = calendar.monthcalendar(2015, 12)
    currentMonthCalendar = calendar.monthcalendar(2016, 1)
    nextMonthCalendar = calendar.monthcalendar(2016, 2)


def makeObjCopy(obj, esgento):
    # ermittel Klasse
    baseClass = obj.__class__
    # lege dummy an
    newObj = baseClass(esgento=esgento)
    # kopiere daten
    newDataDict = obj.modelDataDict()
    primaryKeyFieldNames = obj.esgentoModel.primaryKey().fields().keys()
    for fName in primaryKeyFieldNames:
        if fName in newDataDict:
            del newDataDict[fName]

    newObj.loadFromDict(newDataDict)
    return newObj


def timeDeltaToMinutes(delta):
    seconds = delta.total_seconds()
    minutes = int(float(seconds) / float(60))
    return minutes


class dbNow(type):
    pass


class Alignment:
    Left, Right, Center = range(3)


# class DateTimeEncoder(json.JSONEncoder):
#     def default(self, o):
#         if isinstance(o, datetime):
#             return jsonDateTime(o)
#
#         return json.JSONEncoder.default(self, o)
def getCalledParameters():
    # get caller
    caller = inspect.currentframe().f_back

    # get parameter list
    flist = list(caller.f_code.co_varnames)
    # get values from parameters
    valuesFunc = inspect.getargvalues(caller)[3]
    ret = dict((key, valuesFunc[key]) for key in flist if key in valuesFunc)

    # entfernen von self, falls vorhanden
    if 'self' in ret:
        s = ret['self']
        del ret['self']
    else:
        s = None
    return s, ret


def copyFilterFilesRecursive(sourceDir=None, destDir=None, filter=None):
    print "Copy {filter} from {source} to {dest}".format(filter=filter, source=sourceDir, dest=destDir)
    for root, dir, files in os.walk(sourceDir):
        rel = root[len(sourceDir) + 1:]

        for file in fnmatch.filter(files, filter):
            inFile = os.path.join(root, file)
            outFile = os.path.join(destDir, rel, file)
            copyFile(inFile, outFile)


def copyFile(inFile, outFile):
    destPath = os.path.dirname(outFile)
    if not os.path.exists(destPath):
        os.makedirs(destPath)

    print "Copy {infile} to {outfile}".format(infile=inFile, outfile=outFile)
    shutil.copyfile(inFile, outFile)


class PrettyString(object):
    @classmethod
    def fromDict(cls, d, indent=2, left=0):
        ret = u""

        if left == 0:
            ret += u"{\n"
            leftStr = u" " * (indent * left + 1)
        else:
            leftStr = u" " * (indent * left)

        for key in sorted(d):
            value = d[key]

            if isinstance(value, unicode) or isinstance(value, str):
                value = value.replace('\"', '\\\"')
                value = u"\"{val}\"".format(val=value)
            if isinstance(value, datetime) or isinstance(value, str):
                value = u"\"{val}\"".format(val=dateTimeToIsoDate(value))

            if isinstance(value, dict):
                ret += leftStr + u"\"{key}\": {{".format(key=key)
                if len(value) > 0:
                    ret += u"\n"
                    ret += cls.fromDict(value, indent=indent, left=left + 1)
                    ret += leftStr + u"},\n"
                else:
                    ret += u"},\n"

            elif isinstance(value, list):
                ret += leftStr + u"\"{key}\": [".format(key=key)
                if len(value) > 0:
                    ret += u"\n"
                    ret += cls.fromList(value, indent=indent, left=left + 1)
                    ret += leftStr + u"],\n"
                else:
                    ret += u"],\n"

            else:
                ret += leftStr + u"\"{key}\": {value},\n".format(
                    key=key,
                    value=value
                )
        if left == 0:
            ret += u"}\n"

        return ret

    @classmethod
    def fromList(cls, d, indent=2, left=0):
        ret = u""
        if left == 0:
            ret += u"[\n"
            leftStr = u" " * (indent * left + 1)
        else:
            leftStr = u" " * (indent * left)

        for value in d:

            if isinstance(value, unicode) or isinstance(value, str):
                value = u"\"{val}\"".format(val=value)

            if isinstance(value, dict):
                ret += leftStr + u"{"
                if len(value) > 0:
                    ret += u"\n"
                    ret += cls.fromDict(value, indent=indent, left=left + 1)
                    ret += leftStr + u"},\n"
                else:
                    ret += u"},\n"

            elif isinstance(value, list):
                ret += leftStr + u"["
                if len(value) > 0:
                    ret += u"\n"
                    ret += cls.fromList(value, indent=indent, left=left + 1)
                    ret += leftStr + u"],\n"
                else:
                    ret += u"],\n"

            else:
                ret += leftStr + u"{value},\n".format(
                    value=value
                )

        if left == 0:
            ret += u"]\n"
        return ret


def all_subclasses(cls):
    return cls.__subclasses__() + [g for s in cls.__subclasses__() for g in all_subclasses(s)]


def bitList(n):
    return list(2 ** i for i in range(n.bit_length()) if (n & 2 ** i == 2 ** i))


def intBitList(l):
    return reduce(ior, l)


def conditionalListAddRemove(itemlist, item, state):
    if state:
        if item in itemlist:
            return itemlist
        itemlist.append(item)
    else:
        if item not in itemlist:
            return itemlist
        itemlist.remove(item)
    return itemlist


def add_soup(response):
    if 'text/html' in response.headers.get('Content-Type', ''):
        try:
            response.soup = bs4.BeautifulSoup(response.content, "lxml")
        except:
            pass


def Browser():
    # falls man server vorgauckeln muss, das man mit browser eingelogt ist
    # cls.br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
    if isWindows():
        mechanicalsoup.Browser.add_soup = staticmethod(add_soup)
    br = mechanicalsoup.Browser()

    return br


def UnicodeDictReader(utf8_data, **kwargs):
    csv_reader = csv.DictReader(utf8_data, **kwargs)
    for row in csv_reader:
        yield {key: unicode(value, 'utf-8') for key, value in row.iteritems()}


def generateRandomPassword():
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    pw_length = 8
    mypw = ""

    for i in range(pw_length):
        next_index = random.randrange(len(alphabet))
        mypw = mypw + alphabet[next_index]

    # replace 1 or 2 characters with a number
    for i in range(random.randrange(1, 3)):
        replace_index = random.randrange(len(mypw) // 2)
        mypw = mypw[0:replace_index] + str(random.randrange(10)) + mypw[replace_index + 1:]

    # replace 1 or 2 letters with an uppercase letter
    for i in range(random.randrange(1, 3)):
        replace_index = random.randrange(len(mypw) // 2, len(mypw))
        mypw = mypw[0:replace_index] + mypw[replace_index].upper() + mypw[replace_index + 1:]

    return mypw


def commaSeparatedStrings(listStrings):
    return ",".join(
        list(
            "\"{s}\"".format(s=s) for s in listStrings
        )
    )



def sortByAttribute(sortList, attrName, reverse=False):
    return sorted(sortList, key=lambda x: getattr(x, attrName), reverse=reverse)