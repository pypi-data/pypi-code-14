#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

import logging
import paramiko

import sys
import threading

__author__ = 'Marco Bartel'

LOG = logging.getLogger(__name__)


class SshConnection(object):
    connections = {}

    def __init__(self, hostname=None, port=22, username=None, password=None):
        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password
        self.connectionObject = self.getConnectionObject(
            host=self.hostname,
            port=self.port,
            user=self.username,
            passwd=self.password,
        )

    @classmethod
    def getConnectionObject(self, hostname=None, port=22, username=None, password=None):
        conString = "ssh://{user}:{passwd}@{host}:{port}".format(
            host=hostname,
            port=port,
            user=username,
            passwd=password,
        )

        if conString not in SshConnection.connections:
            SshConnection.connections[conString] = SshConnectionObject(
                hostname=hostname,
                port=port,
                username=username,
                password=password
            )

        return SshConnection.connections[conString]

    def __enter__(self):
        return self.getConnectionObject()

    def __exit__(self, ex_type, ex_value, traceback):
        if ex_type is None:
            return True

        elif isinstance(ex_value, Exception):
            LOG.exception(ex_value)
            return False


class SshConnectionObject(object):
    def __init__(self, hostname=None, port=None, username=None, password=None):
        self.writFileDataLock = threading.Lock()
        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password
        self.open = False

        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    def realConnect(self):
        print(self.port)
        self.ssh.connect(
            hostname=self.hostname,
            username=self.username,
            password=self.password,
            port=self.port,
        )
        self.ftp = self.ssh.open_sftp()

    def connect(self):

        if self.open == False:
            self.realConnect()
            self.open = True

        tr = self.ssh.get_transport()
        if tr is None:
            self.open = False
            self.realConnect()
            self.open = True
        else:
            if not tr.is_active():
                self.open = False
                self.realConnect()
                self.open = True

    def makeDirs(self, dirPath):
        currentDir = '/'
        for dirElement in dirPath.split('/'):
            if dirElement:
                currentDir += dirElement + '/'
                try:
                    self.ftp.mkdir(currentDir)
                    LOG.debug('Directory created on :' + currentDir)
                except:
                    pass  # fail silently if remote directory already exists

    def writeFileData(self, targetFilePath, data):
        with self.writFileDataLock:
            self.connect()
            partFilePath = targetFilePath + ".part"
            dirPath = os.path.dirname(targetFilePath)
            self.makeDirs(dirPath=dirPath)
            file = self.ftp.file(partFilePath, "w")
            file.write(data)
            file.flush()
            try:
                self.ftp.stat(targetFilePath)
                LOG.debug("Remote file {f} exists already. Removing...".format(f=targetFilePath))
                self.ftp.remove(targetFilePath)
            except:
                pass
            finally:
                # LOG.debug("Renaming {pf} to {tp}".format(pf=partFilePath, tp=targetFilePath))
                self.ftp.rename(partFilePath, targetFilePath)

    def close(self):
        if not self.open:
            return
        self.ftp.close()
        self.ssh.close()
        self.open = False


class File(object):
    python3 = sys.version_info > (3, 0)

    def __init__(self, filePath=None, mode=None, encoding="utf8"):
        self.filePath = filePath
        self.mode = mode
        self.encoding = encoding
        self.fd = None

    def open(self):
        self.createPath()

        if self.python3:
            self.fd = open(self.filePath, self.mode, encoding=self.encoding)
        else:
            self.fd = open(self.filePath, self.mode)

    def createPath(self):
        dirPath = os.path.dirname(self.filePath)
        if not os.path.exists(dirPath):
            os.makedirs(dirPath)

    def write(self, data):
        if not self.python3:
            data = data.encode(self.encoding)
        self.fd.write(data)

    def read(self):
        data = self.fd.read()
        if not self.python3:
            data = data.decode(self.encoding)
        return data

    def readlines(self):
        return self.read().splitlines()

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.fd.close()
        if exc_type is None:
            return True

        elif isinstance(exc_val, Exception):
            LOG.exception(exc_val)
            return False


class FileSSH(File):
    def __init__(self, filePath=None, mode=None, hostname=None, port=22, username=None, password=None, encoding="utf8"):
        self.filePath = filePath
        self.mode = mode
        self.encoding = encoding
        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password
        self.connection = SshConnection.getConnectionObject(
            hostname=self.hostname,
            port=self.port,
            username=self.username,
            password=self.password
        )

    @property
    def partFilePath(self):
        return self.filePath + ".part"

    def createPath(self):
        dirPath = os.path.dirname(self.filePath)
        self.connection.makeDirs(dirPath=dirPath)

    def renamePartFile(self):
        try:
            self.connection.ftp.stat(self.filePath)
            LOG.debug("Remote file {f} exists already. Removing...".format(f=self.filePath))
            self.connection.ftp.remove(self.filePath)
        except:
            pass
        finally:
            # LOG.debug("Renaming {pf} to {tp}".format(pf=partFilePath, tp=targetFilePath))
            self.connection.ftp.rename(self.partFilePath, self.filePath)

    def open(self):
        self.connection.connect()
        self.createPath()
        filePath = self.partFilePath if self.mode in ("w", "wb") else self.filePath
        self.fd = self.connection.ftp.file(filePath, self.mode)

    def close(self):
        self.fd.close()
        if self.mode in ("w", "wb"):
            self.renamePartFile()

    def write(self, data):
        data = data.encode(self.encoding)
        self.fd.write(data)
        self.fd.flush()

    def read(self):
        data = self.fd.read()
        data = data.decode(self.encoding)
        return data

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

        if exc_type is None:
            return True

        elif isinstance(exc_val, Exception):
            LOG.exception(exc_val)
            return False
