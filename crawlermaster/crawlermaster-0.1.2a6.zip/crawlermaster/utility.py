# -*- coding: utf-8 -*-
"""
Copyright (C) 2015, MuChu Hsu
Contributed by Muchu Hsu (muchu1983@gmail.com)
This file is part of BSD license

<https://opensource.org/licenses/BSD-3-Clause>
"""
import json
import os
import datetime
from bennu.filesystemutility import FileSystemUtility
#共用工具程式
class Utility:
    
    #建構子
    def __init__(self):
        pass
    
    #儲存檔案
    def overwriteSaveAs(self, strFilePath=None, unicodeData=None):
        with open(strFilePath, "w+") as file:
            file.write(unicodeData.encode("utf-8"))
    
    #讀取 json 檔案內容，回傳 dict 物件
    def readObjectFromJsonFile(self, strJsonFilePath=None):
        dicRet = None
        with open(strJsonFilePath, "r") as jsonFile:
            dicRet = json.load(jsonFile, encoding="utf-8")
        return dicRet
    
    #將 dict 物件的內容寫入到 json 檔案內
    def writeObjectToJsonFile(self, dicData=None, strJsonFilePath=None):
        with open(strJsonFilePath, "w+") as jsonFile:
            jsonFile.write(json.dumps(dicData, ensure_ascii=False, indent=4, sort_keys=True).encode("utf-8"))
            
    #取得 dict 物件的 json 字串
    def getJsonifyString(self, dicData=None):
        return json.dumps(dicData, ensure_ascii=False, indent=4, sort_keys=True).encode("utf-8")
    
    #取得 strBasedir 目錄中，檔名以 strSuffixes 結尾的檔案路徑
    def getFilePathListWithSuffixes(self, strBasedir=None, strSuffixes=None):
        lstStrFilePathWithSuffixes = []
        for base, dirs, files in os.walk(strBasedir): 
            if base == strBasedir:#just check base dir
                for strFilename in files:
                    if strFilename.endswith(strSuffixes):#find target files
                        strFilePath = base + "\\" + strFilename
                        lstStrFilePathWithSuffixes.append(strFilePath)
        return lstStrFilePathWithSuffixes
        
    #取得檔案的建立日期
    def getCtimeOfFile(self, strFilePath=None):
        fCTimeStamp = os.path.getctime(strFilePath)
        dtCTime = datetime.datetime.fromtimestamp(fCTimeStamp)
        strCTime = dtCTime.strftime("%Y-%m-%d")
        return strCTime
        
    #取得陣列中的第一個物件
    def extractFirstInList(self, lstSource=[]):
        if len(lstSource) > 0:
            return lstSource[0]
        else:
            return None
    