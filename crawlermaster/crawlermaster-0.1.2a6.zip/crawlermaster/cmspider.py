# -*- coding: utf-8 -*-
"""
Copyright (C) 2015, MuChu Hsu
Contributed by Muchu Hsu (muchu1983@gmail.com)
This file is part of BSD license

<https://opensource.org/licenses/BSD-3-Clause>
"""
import logging
import tempfile
import os
import time
import pkg_resources
from selenium import webdriver
from crawlermaster.utility import Utility

class SeleniumSpider:
    #建構子
    def __init__(self):
        self.utility = Utility()
        self.driver = None
    
    #取得 selenium driver 物件
    def getDriver(self):
        chromeDriverExeFilePath = pkg_resources.resource_filename("crawlermaster.resource", "chromedriver.exe")
        driver = webdriver.Chrome(chromeDriverExeFilePath)
        return driver
        
    #初始化 selenium driver 物件
    def initDriver(self):
        if self.driver is None:
            self.driver = self.getDriver()
        
    #終止 selenium driver 物件
    def quitDriver(self):
        self.driver.quit()
        self.driver = None
        
    #儲存 temp.html 並讀取內容
    def saveUrlToTempFileAndReadContent(self, strUrl=None, lstDicPreAction=[]):
        #開始 URL 網頁
        self.driver.get(strUrl)
        #執行前置動作
        for dicPreAction in lstDicPreAction:
            for actionKey in dicPreAction.keys():
                if actionKey == "click":
                    self.driver.find_element_by_css_selector(dicPreAction[actionKey]).click()
                    time.sleep(5)
        #儲存 html
        strTempHtmlFilePath = tempfile.NamedTemporaryFile(prefix="cmTempPage", suffix=".html", delete=False).name
        self.utility.overwriteSaveAs(strFilePath=strTempHtmlFilePath, unicodeData=self.driver.page_source)
        #讀取內容
        strPageSource = None
        with open(strTempHtmlFilePath, "r") as tempHtmlFile:
            strPageSource = tempHtmlFile.read()
        os.remove(strTempHtmlFilePath)
        return strPageSource
        
class CmSpider:
    #建構子
    def __init__(self):
        self.spider = SeleniumSpider()
        
    def spiderTempUrlPage(self, strUrl=None, lstDicPreAction=[]):
        self.spider.initDriver()
        strPageSource = self.spider.saveUrlToTempFileAndReadContent(strUrl=strUrl, lstDicPreAction=lstDicPreAction)
        self.spider.quitDriver()
        return strPageSource