# -*- coding: utf-8 -*-
#"""
#Created on Wed May 20 22:58:41 2015

#@author: sherif
#"""

import urllib.request
import os.path
import hashlib
import re
from html.parser import HTMLParser
import pickle

class HTMLreader(HTMLParser):
#this class reads html doc to extract all non-script non-css non-links text
# and a list of tuples (key, value) = (linkname, href)

    def __init__(self):
        super(HTMLreader, self).__init__()
        self.links = []
        self.text =""
        self._isInAnchorTag = False
        self._attrsInAnchor = None 
        self._dataInAnchor = ""
        self._currentTag = None
        self.count = 0
        
    def reset(self):
        super(HTMLreader, self).reset()
        self.links = []
        self.text =""
        self._isInAnchorTag = False
        self._attrsInAnchor= None
        self._dataInAnchor = ""
        self._currentTag = None
        self.count = 0
        
    def handle_starttag(self, tag, attrs):
        self._currentTag = tag
        if(tag == 'a'):
            self.count +=1
            self._attrsInAnchor = attrs
            self._isInAnchorTag = True
        elif(tag == "br"):
                self.text +='\n'
                
    def handle_endtag(self, tag):
        if(self._isInAnchorTag and tag == 'a'):
            name = re.sub('\s+',' ',self._dataInAnchor.lower())
            self._attrsInAnchor =  dict(self._attrsInAnchor)
            if('href' in self._attrsInAnchor.keys()):
                href = self._attrsInAnchor['href'] #found linkname for hyperlink
                self.links+=[(name, href)]
            self._isInAnchorTag = False
            self._intagAttrs = None
            self._dataInAnchor = ""
        elif tag=='tr':
            self.text +='\n'
        #print("Encountered an end tag :", tag)

    def handle_data(self, data):
        if(not data.isspace() ):
            if(self._isInAnchorTag):
                self._dataInAnchor+=" "+data.lstrip().rstrip()
            elif(self._currentTag!="script" and self._currentTag!="style"):
                self.text=self.text.rstrip(" ")+" "+data.lower()
        #print("Encountered some data  :", data)


def getHTML(URL):
    if URL == 'http://' or URL.isspace():
        return None
    try:
        Headers = dict()
        Headers["User-Agent"] = "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.81\
        Safari/537.36"
        req = urllib.request.Request(URL, headers = Headers)
        Handler = urllib.request.urlopen(req, timeout=10)
        d = Handler.read().decode()
        Handler.close()
        return d
    except Exception as e:
        print(str(e))
        return None

