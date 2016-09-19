import datalib

from datalib import (encode,decode,combiParse,unParse
                         ,JSONDict,JSONSimpleHandler)
from collections import OrderedDict
import json

import pytest

def test_myTest():
    pass

# the testing code
if __name__ == '__main__':
    indebug = True

    class PageEmulator(object):
        def write(self, pstr):
            print (pstr.replace('<br>', '\n'))

    class Fred:
        def __init__(self,a,b):
            self.a=a
            self.b=b


    @decode.from_object(JSONSimpleHandler)
    class DataModel2(JSONDict):
      pass


    @encode.to_object()
    class OutExample:
      @encode.handler
      def handler(self):
        print('called handler')
        return {"a":1}

    @encode.to_object()
    @decode.from_object()
    class DataModel(object):
        def __init__(self, id=0, value=7,**kwargs):
            #print('kwargs',kwargs)
            self.id = id
            self.value = value
        def __repr__(self):
            return '<DM id:{id} val:{value}>'.format(**self.__dict__)
    foo=DataModel(1,'silly')
    cord= OrderedDict([('aa',1),('bb',2),('cc',3),('dd',4)])
    data = {'a':5.6  ,'b':DataModel(5, foo)
            ,'c':cord}
    print('dat',data['c'])
    dumdat=encode.dumper(data)
    print('dumper',dumdat)
    d2=decode.loader(dumdat)
    print('load',d2)
    print('combiP',combiParse(dumdat))

    print('handler',unParse(OutExample()))
    dumdat=encode.dumper(OutExample())
    print('dumper handler',dumdat)


    #splitDash tests
    b="a=123&b=456-789&d=abc-def"
    a=combiParse(b,splitDash=True)
    print(a)
    rawdata=unParse({'a':5.6,'b':{'c':1}
                ,'c':[DataModel(5, [foo])]
                ,'d':cord
                     })
    data=combiParse(rawdata)
    print('rawdat',rawdata,data)
    formdata= unParse(data,indent=4)
    print ('data\n',formdata)

    moddata=formdata.replace('DataModel','DataModel2')

    print(combiParse(formdata))
    modparsed= combiParse(moddata) #,no__type__=True)
    print(modparsed)



    theReq = PageEmulator()

    try:
        with open('parse.txt') as parseFile:
            testmsg = parseFile.read()
    except IOError:
        print ("file parse.txt not found, using internal test\n")
        testmsg = ("tt=os&stb=8061&pn=61411541240&"
              "txnref=3181&jnr=1-01e9b7d74bd9bde1&"
            "appver=1.1.15&delMode=3&pick=0&sp=3.0193632410-&"
            "sect0=ord-isq&isq=0&ico=cCappucino&n=1&sz=0&fl=0"
            "&add=&req=&price=300&du=1")
    #print ("input text to parse")
    a = combiParse(testmsg)
    #print ('a is', a, "\n\n  objwalks\n", objWalk(a), \
    # '\n\njson \n', unParse(a, indent=4))

    #import urllib
    ur=unParse(a)
    #print ('json', ur, '\nurl', urlparselib.urlencode({'json':ur}))

    b=combiParse('{"rc": "0", "stn": "Ju\u003Dra at Rozelle1", "fav": "", "stf": "tDUEN", "stb": "8061", "tag": "wap"} ')


    print ('\n uparse b', unParse(b))

    #necho(a)
