# -*- coding: utf-8 -*-
"""
Copyright (C) 2015, MuChu Hsu
Contributed by Muchu Hsu (muchu1983@gmail.com)
This file is part of BSD license

<https://opensource.org/licenses/BSD-3-Clause>
"""
import logging
import sys
import os
from crawlermaster.cmparser import CmParser
from crawlermaster.utility import Utility

def entry_point():
    #logging 層級設定
    logging.basicConfig(level=logging.INFO)
    #讀取 css list
    if len(sys.argv) < 2:
        logging.error("useage: crawlermaster some_csslist.json")
        sys.exit()
    strCssJsonFilePath = sys.argv[1]
    if not os.path.exists(strCssJsonFilePath):
        logging.error("file %s not exists"%strCssJsonFilePath)
        sys.exit()
    #執行 css 測試
    logging.info("start test csslist: %s"%strCssJsonFilePath)
    cmParser = CmParser(strCssJsonFilePath=strCssJsonFilePath)
    cmUtility = Utility()
    lstDicTestResultRawData = cmParser.selectorTestParse()
    #寫入測試結果
    strJsonFilePath = "csslist_test_result.json"
    logging.info("write test result: %s"%strJsonFilePath)
    cmUtility.writeObjectToJsonFile(dicData=lstDicTestResultRawData, strJsonFilePath=strJsonFilePath)
    
if __name__ == "__main__":
    entry_point()