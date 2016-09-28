#
from __future__ import (absolute_import, division,
                        print_function) #, unicode_literals)
import decimal
from  objdict import objDict
#import objDict

from objdict.objDict import (json,loads, dumps,#encode, #"decode", #,jsParse,unParse
                        ObjectEncoderAll,ObjectEncoderStd,
                         ObjDict)
from objdict.dualUrlJson import combiParse,unParse,jsParse

from collections import OrderedDict
#import json
from bson.objectid import ObjectId  #used to test including ObjectId
import pytest

from datetime import datetime,date

# class Fred:
#     def __init__(self,a,b):
#         self.a=a
#         self.b=b


@objDict.from_json()
class DataModel2(ObjDict):
  pass


@objDict.to_json()
class OutExample:
  #@objdict.handler
  def handler(self):
    print('called handler')
    return {"a":1}

@objDict.to_json()
@objDict.from_json()
class DataModel(object):
    def __init__(self, id=0, value=7,**kwargs):
        #print('kwargs',kwargs)
        self.id = id
        self.value = value
    def __repr__(self):
        return '<DM id:{id} val:{value}>'.format(**self.__dict__)

@pytest.fixture
def datamodel():
    return DataModel()

@pytest.fixture
def tobj():
    return ObjDict(a=5,b=3)

@objDict.to_json()
@ObjDict.from_json()
class SubClassWithInit(ObjDict):
    def __init__(self,a=None,b=None,**kwargs):
        """ sublcassed from objdict, so json by default would
        send all data to first parm, to use this init
        require __from_json_ """
        super(SubClassWithInit,self).__init__()
        self.a=a
        self.b=b
        self.c=kwargs
    @classmethod
    def __from_json__(cls,odict):
        """ __from_json__ to match own init method"""
        return cls(odict.pop('a'),odict.pop('b'),**odict)

@pytest.fixture
def ordlist():
    return [('a',1),('b',2),('c',3)]

class TestObjDict:
    def test_attrib(self,tobj):
        #tobj=ObjDict(a=5,b=3)
        assert tobj.a==5

    def test_set_type(self,tobj):
        # _set_type defaults to false but can be set to true
        assert tobj._set_type == False
        tobj._set_type = True
        assert tobj._set_type == True

    def test_dictv(self,tobj):
        #check intial dictionay value
        assert tobj['a']==5

    def test_addatrrib(self,tobj):
        #add new attribute and check access by dictionary
        tobj.c=10
        assert tobj['c']==10

    #@pytest.mark.xfail
    def test_add_hidden_atrrib(self,tobj):
        with pytest.raises(KeyError):
            tobj._c=10
            assert tobj['_c']==10

    def test_addtodict(self,tobj):
        tobj['c'] = 10
        assert tobj.c ==10
        assert tobj['c']== 10 #did we break std ?

    def test_initlist(self,ordlist):
        o=ObjDict(ordlist)
        assert list(o.keys())==['a','b','c']

    def test_initsequence(self):
        tobj=SubClassWithInit(a=1,b=2)
        tobj.c=3
        tobj.d=4
        tobj.f=5
        tobj.e=6
        assert list(tobj.keys())==['a','b','c','d','f','e']

    def test_init_errorjson(self):
        with pytest.raises(ObjDict.JsonDecodeError):
            a = ObjDict('{"a"=1,"b"=2}') #= in place of :

    def test_init_json(self):
        a = ObjDict('{"a":1,"b":2}')
        assert list(a.keys())== ["a","b"]

    #def test_init_fromObjDict(self,tobj):


@objDict.to_json()
@objDict.from_json()
class SampleClass:
    def __init__(self,a=None,b=None):
        self.a=a
        self.b=b

class SubClass(ObjDict):
    pass

@objDict.from_json()
class SubSimpleClass(ObjDict):
    def __init__(self,*args,**kwargs):
        #manual ordering plus default
        print('argslook',args)
        super(SubSimpleClass,self).__init__(*args,**kwargs)
class RawClass:
    pass
@pytest.fixture
def sample_text():
    return """
    {
    "zeroth":{ "type": "justdict","a":1,"b":2},
    "first":{ "__type__": "SampleClass","a":1,"b":2},
    "second":{ "__type__": "Test2","a":1,"b":2},
    "third": {"__type__": "RawClass"},
    "forth": { "a":1,"b":2,"__type__": "SubSimpleClass"},
    "fifth": {"__type__": "SubClassWithInit", "a":1,"b":2,"c":3}
    }
    """
@pytest.fixture
def parsed_text(sample_text):
    return combiParse(sample_text)

class TestInstanceJson:
    def test_with_types(self,parsed_text):
        t= parsed_text
        assert isinstance(t['zeroth'],ObjDict)
        assert t['zeroth']._set_type==False
        print('type',type(t['second']),type(t['first']),SampleClass)
        #assert False
        assert isinstance(t['first'],SampleClass)
        assert t.first.a == 1
        assert isinstance(t['second'],ObjDict)
        assert t.second.a == 1
        assert t['second']._set_type==True

        # now test class name is preserved
        assert t['second'].__class__.__name__ == "Test2"
        assert t['third'].__class__.__name__ == "RawClass"
        assert t.forth.a == 1
        print('5 keys',list(t['fifth'].keys()))
        assert t.fifth.a == 1
        assert list(t['fifth'].keys()) == ["a","b","c"]
        assert t['fifth'].c =={'c':3} #at some time want something to keep


    def test_with_autotypes_order(self,parsed_text):
        t= parsed_text
        print('for',t['forth'].keys())
        assert t['forth'].keys() != ["__type__","b","a",]#["a","b","__type__"]

    @pytest.mark.xfail
    def test_name_collide(self,sample_text):
        """ instanced classes do not match existing classes if the
          existing class is not decorated to expect to be used for json data
         """
        t=jsParse(sample_text)
        print('raw',type(t['third']),RawClass)
        assert isinstance(t['third'],RawClass)


@pytest.fixture
def complexObj():
    foo=DataModel(1,'silly')
    cord= ObjDict([('aa',1),('bb',2),('cc',3),('dd',4)])
    data = {'a':5.6  ,'b':DataModel(5, foo)
            ,'c':cord}
    return data

@pytest.fixture
def complexObjDict(complexObj):
    return ObjDict(complexObj)

class TestToJson:
    def test_odict(self,complexObj):
        print('dat',complexObj['c'])
        dumdat=objDict.dumps(complexObj)
        print('dumper',dumdat)
        d2=loads(dumdat,object_pairs_hook=ObjDict)
        print('load',d2)
        out=jsParse(dumdat)
        assert list(out['c'].keys()) ==['aa','bb','cc','dd']
    #def test_with_types(self,sample_text)

    def test_Decimal(self):
        testobj=ObjDict(d=decimal.Decimal(5.1))
        dumpdat=unParse(testobj) #objDict.dumper(t)
        assert '"d": 5.1' in dumpdat

    def test_datetime(self):
        testobj=ObjDict(dt=datetime(2016,9,5,8,15),d=date(2015,2,5) )
        dumpdat=unParse(testobj) #objDict.dumper(t)
        assert '"d": "2015-02-05"' in dumpdat
        assert '"dt": "2016-09-05 08:15:00"' in dumpdat

    def test_ObjDict(self,ordlist):
        o=ObjDict(ordlist)
        s=SubClass(ordlist)
        print ('pro',unParse(o),unParse(s))
        assert unParse(o)=='{"a": 1, "b": 2, "c": 3}'
        s_un=unParse(s)
        #unParse(Fred(1,2))
        assert '__type__' in s_un and 'SubClass' in s_un

    def test_UnParseObjID(self):
        tdata={'a':5,'b':ObjectId()}
        assert '_ObjectId' in unParse(tdata)

class TestInstance__json__:
    """ test both loading and dumping from within """
    def test_instance(self,sample_text):
        a=ObjDict(sample_text)
        assert a['zeroth']['a']== 1

    def test_tojson(self,complexObjDict):
        text=complexObjDict.__json__()
        assert '<bound method' not in text
        assert '"__type__": "DataModel"' in text
        assert '"value": "silly"' in text

    def test_strtojson(self,complexObjDict):
        text=complexObjDict.__json__()
        assert text == str(complexObjDict)


class XYZ(ObjDict):
    __keys__ ="x y z"

class TestNameTuple:
    def test_instance(self):
        xyz=XYZ(1,2,3)
        assert xyz.y == 2

    def test_instance_singleton(self):
        abc=ObjDict(1,2,3,__keys__="a b c")
        assert abc.b == 2
        assert abc.__keys__ == ["a","b","c"]

@pytest.fixture
def dashstr():
    return "a=123&b=456-789&c=abc-def-"

class TestSplitDash:

    def test_withsplit_true(self,dashstr):
        a=combiParse(dashstr,splitDash=True)
        print(a)
        assert isinstance(a['a'],str)
        assert isinstance(a['b'],list)
        assert len(a['b'])==2
        assert len(a['c'])==2

    def test_withsplit_none(self,dashstr):
        """default is splitDash=None"""
        a=combiParse(dashstr)
        print(a)
        assert isinstance(a['a'],str)
        assert isinstance(a['b'],str)
        assert isinstance(a['c'],list)
        assert len(a['c'])==2
    def test_withsplit_False(self,dashstr):
        a=combiParse(dashstr,splitDash=False)
        print(a)
        assert isinstance(a['a'],str)
        assert isinstance(a['b'],str)
        assert isinstance(a['c'],str)

class TestCombiParse:
    def test_url_data(self):
        pass

class TestUnParse:
    def test_unparse_url(self):
        pass
