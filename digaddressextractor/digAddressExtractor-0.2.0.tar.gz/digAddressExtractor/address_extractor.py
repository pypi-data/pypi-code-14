import json
import sys
import re
from sets import Set
import time




"""
Keywords: contains list of all the addresses type that we want to use for processing.
"""

keywords=["avenue","blvd","boulevard","pkwy","parkway","st","street","rd","road","drive","lane","alley","ave"]

phonePattern = re.compile(r'(\d{3})\D*(\d{3})\D*(\d{4})')

def cleanAddress(text_string,level):
    if level>0:
        #Slicing from 'location' word in found adddress
        pos=text_string.find('location')
        if pos >-1:
            text_string=text_string[pos+len('location'):]

    if level>1:
        #Slicing from phone number reference word in found adddress to end
        m=phonePattern.search(text_string)
        if m!=None:
            pos=m.span()[1]
            text_string=text_string[pos:]

    if level>2:
        #Cleaning if maps URL present
        if text_string.find('maps.google.com') >-1 or text_string.find('=')>-1:
            pos=text_string.rfind('=')
            if pos >-1:
                text_string=text_string[pos+1:].replace('+',' ')
    return text_string.strip()

def getNum(text,start,dist):
    end=start+1
    flag=0
    while start >0 and end-start <=dist and text[start]!='\r' and text[start]!='\n':
        if text[start].isdigit() and (start-1==0 or text[start-1]==" " or text[start-1]=="\n" or text[start-1]==">" or text[start-1]==")"):
            flag=1
            break;
        start=start-1
    return flag,start

def getNumNext(text,end,dist):
    start=end
    flag=0
    count=0
    while end <len(text)-2 and end-start <=dist and text[start]!='\r' and text[start]!='\n':
        if text[end].isdigit():
            count+=1
        if count==5 and text[end+1].isdigit() and (end+1==len(text)-2 or text[end+1]==" " or text[end+1]=="\n" or text[end+1]=="<"):
            flag=1
            break;
        end=end+1
    return flag,end+1

def getSpace(text,start):
    while start >0:
        if text[start-1]==" ":
            break;
        start=start-1
    return start

def extractAddress(text,p,type1,addresses):
    end=-1
    m=p.search(text.lower())
    if m!=None:
        end=m.span()[0]+len(type1)+1
    if end !=-1:
        flag=1
        flag,bkStart=getNum(text,end-(len(type1)+1),50)
        if flag==0:
            start=getSpace(text,end-(len(type1)+2))
        elif flag==1:
            flag,start=getNum(text,bkStart-1,10)
            #print (flag, text[start:end])
            if flag==0:
                start=bkStart
        flag,newEnd=getNumNext(text,end,25)
        if flag:
            end=newEnd
        addresses.add(cleanAddress(text[start:end].lower(),3))
        m=p.search(text.lower(),end)
        if m!=None:
            addresses=extractAddress(text[end:],p,type1,addresses)
        return addresses
    return addresses
#extractAddress("<BR />=?=?=  Table Shower available  =?=?=<br><br>?=Let us make you stress free one day at a time=?<br><br>=?= PUENTE Spa=?= <br><br>TEL:  626-338-8809  <br><br>  1832 Puente Ave. Baldwin Park, CA. 91706  <br><br>Clean Shower Included With Session<br><br>we always hiring beautiful ladies<br><br> Open- 9:00 AM to 9:30 PM<br>  </div>")


"""
Input: Text String
Output: Json object containing input text string with list of associated present addresses

Uses default keywords embedded in script file
"""
def getAddressFromString(text_string):
    # temp={}
    #temp["input"]=text_string
    addresses=Set()
    for each_keyword in keywords:
        p = re.compile(r'\b%s\b' % each_keyword.lower(), re.I)
        m=p.search(text_string.lower())
        if m!=None:
            extractAddress(text_string,p,each_keyword,addresses)
    #temp["address"]=list(addresses)
    return addresses

"""
Input: Text String and keyword python list ex: ["ave","street"] etc.
Output: Json object containing input text string with list of associated present addresses

Uses keywords list passed as an parameter
"""
def getAddressFromStringType(text_string,keywords):
    temp={}
    temp["input"]=text_string
    addresses=Set()
    for each_keyword in keywords:
        p = re.compile(r'\b%s\b' % each_keyword.lower(), re.I)
        m=p.search(text_string.lower())
        if m!=None:
            extractAddress(text_string,p,each_keyword,addresses)
    temp["address"]=list(addresses)
    return temp


import copy 
import types
from digExtractor.extractor import Extractor

class AddressExtractor(Extractor):

    def __init__(self):
        self.renamed_input_fields = ['text']  # ? renamed_input_fields

    def extract(self, doc):
        if 'text' in doc:
            return getAddressFromStringType(doc['text'], keywords)
        return None
        
    def get_metadata(self):
        return copy.copy(self.metadata)

    def set_metadata(self, metadata):
        self.metadata = metadata
        return self

    def get_renamed_input_fields(self):
        return self.renamed_input_fields
