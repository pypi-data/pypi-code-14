# -*- coding: utf-8 -*-
"""
Copyright (C) 2015, MuChu Hsu
Contributed by Muchu Hsu (muchu1983@gmail.com)
This file is part of BSD license

<https://opensource.org/licenses/BSD-3-Clause>
"""
import logging
from crawlermaster.utility import Utility

class CmSelector:

    #建構子
    def __init__(self, strCssJsonFilePath=None):
        self.cmUtility = Utility()
        self.strCssJsonFilePath = strCssJsonFilePath
        
    def getCssSelectorList(self):
        dicCsslist = self.cmUtility.readObjectFromJsonFile(strJsonFilePath=self.strCssJsonFilePath)
        lstDicCssSelector = dicCsslist.get("csslist", [])
        return lstDicCssSelector
    
    def getConverterName(self):
        dicCsslist = self.cmUtility.readObjectFromJsonFile(strJsonFilePath=self.strCssJsonFilePath)
        strConverterName = dicCsslist.get("rawdata-converter-name", None)
        return strConverterName
    
    def getLocalHtmlFilePatternDic(self):
        dicCsslist = self.cmUtility.readObjectFromJsonFile(strJsonFilePath=self.strCssJsonFilePath)
        dicLocalHtmlFilePattern = dicCsslist.get("local-html-file-pattern", None)
        return dicLocalHtmlFilePattern