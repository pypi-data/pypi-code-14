# -*- coding: utf-8 -*-
"""
Copyright (C) 2015, MuChu Hsu
Contributed by Muchu Hsu (muchu1983@gmail.com)
This file is part of BSD license

<https://opensource.org/licenses/BSD-3-Clause>
"""
import logging
from scrapy import Selector
from crawlermaster.utility import Utility
from crawlermaster.cmselector import CmSelector
from crawlermaster.cmspider import CmSpider

class CmParser:

    #建構子
    def __init__(self, strCssJsonFilePath=None):
        self.cmUtility = Utility()
        self.cmSelector = CmSelector(strCssJsonFilePath=strCssJsonFilePath)
        self.cmSpider = CmSpider()
        self.intIterateStartIndex = 0
        self.intMaxHtmlFilePerIteration = 1000
        
    #檢查 selector 正確性
    def selectorTestParse(self):
        lstDicCssSelector = self.cmSelector.getCssSelectorList()
        lstDicTestResultRawData = []
        for dicCssSelector in lstDicCssSelector:
            dicRawData = {}
            strPageSource = self.cmSpider.spiderTempUrlPage(strUrl=dicCssSelector["sampleUrl"], lstDicPreAction=dicCssSelector["preAction"])
            root = Selector(text=strPageSource)
            lstStrAns = root.css(dicCssSelector["cssRule"]).extract()
            dicRawData["name"] = dicCssSelector["name"]
            dicRawData["cssRule"] = dicCssSelector["cssRule"]
            dicRawData["ans"] = lstStrAns
            dicRawData["sampleAns"] = dicCssSelector["sampleAns"]
            if lstStrAns == dicCssSelector["sampleAns"]:
                dicRawData["isExactPass"] = True
                dicRawData["isExistPass"] = True
            elif dicCssSelector["ansType"] == "exist" and len(lstStrAns) > 0:
                dicRawData["isExactPass"] = False
                dicRawData["isExistPass"] = True
            else:
                dicRawData["isExactPass"] = False
                dicRawData["isExistPass"] = False
            logging.info("selector test result: %s"%dicRawData["name"])
            logging.info("exact pass: %r"%dicRawData["isExactPass"])
            logging.info("exist pass: %r"%dicRawData["isExistPass"])
            lstDicTestResultRawData.append(dicRawData)
        return lstDicTestResultRawData
    
    #本地 html 檔案解析
    def localHtmlFileParse(self, strBasedir=None, strSuffixes=None, isIterable=False, isResetIteration=False):
        dicLocalHtmlFilePattern = self.cmSelector.getLocalHtmlFilePatternDic()
        if not strBasedir:
            strBasedir = dicLocalHtmlFilePattern.get("strBasedir", None)
        if not strSuffixes:
            strSuffixes = dicLocalHtmlFilePattern.get("strSuffixes", None)
        lstStrHtmlFilePath = self.cmUtility.getFilePathListWithSuffixes(strBasedir=strBasedir, strSuffixes=strSuffixes)
        #檢查是否啟動分段功能
        if isIterable: #有分段
            if isResetIteration: #重設 從第一段開始
                self.intIterateStartIndex = 0
            else: #接續下一段
                pass
            #縮小範圍為本段
            lstStrHtmlFilePath = lstStrHtmlFilePath[self.intIterateStartIndex:self.intIterateStartIndex+self.intMaxHtmlFilePerIteration]
        else: #沒分段
            pass
        lstDicPageRawData = []
        for strHtmlFilePath in lstStrHtmlFilePath:
            #讀取 html 檔案
            with open(strHtmlFilePath, "r") as htmlFile:
                strPageSource = htmlFile.read()
                root = Selector(text=strPageSource)
            #讀取 css 規則
            lstDicCssSelector = self.cmSelector.getCssSelectorList()
            dicRawData = {}
            for dicCssSelector in lstDicCssSelector:
                #解析 html
                lstStrAns = root.css(dicCssSelector["cssRule"]).extract()
                dicRawData[dicCssSelector["name"]] = lstStrAns
            #解析 html 其他 meta-data 資訊
            dicRawData["meta-data-html-filepath"] = strHtmlFilePath
            dicRawData["meta-data-crawl-datetime"] = self.cmUtility.getCtimeOfFile(strFilePath=strHtmlFilePath)
            lstDicPageRawData.append(dicRawData)
        #輸出 raw_data.json
        strJsonFilePath = "raw_data.json"
        self.cmUtility.writeObjectToJsonFile(dicData=lstDicPageRawData, strJsonFilePath=strJsonFilePath)
        #檢查是否啟動分段功能
        if isIterable:
            #下一段
            self.intIterateStartIndex = self.intIterateStartIndex+self.intMaxHtmlFilePerIteration
        else:
            pass
        #回傳
        return lstDicPageRawData
    