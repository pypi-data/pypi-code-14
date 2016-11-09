#! /usr/local/bin/python
#-*- coding:utf-8 -*-

"""
@author: weber.juche@gmail.com
@time: 2016/11/9 11:30

命令字实现封装基类

"""

import sys
import time

from weberFuncs import PrintTimeMsg,PrintMsTimeMsg,GetCurrentTime

gsCmdFuncPrefix = 'cmd_'     # WeiYF.20161109 约定函数服务前缀固定是 cmd_
gsClassPrefix = 'CHandleCmd' # 类前缀
gfSecondsWarn = 0.001     # 命令执行告警秒数阈值

def GetServiceNameFromClassName(sClassName):
    """
        从类名得到服务名
    """
    global gsClassPrefix
    sPrefix, sSep, sSuffix = sClassName.partition('_')
    if sSep == '_' and sPrefix == gsClassPrefix:
        return sSuffix
    return ''

def RegisterForHandleCmdService():
    """
        定义一个类装饰器，将使用该装饰器的类中的函数转为命令服务
    """
    global gsCmdFuncPrefix,gfSecondsWarn
    sPrefix = gsCmdFuncPrefix
    lenPrefix = len(sPrefix)
    def CallByName(cls, sName, *args, **kwargs):
        # PrintTimeMsg('%s in %s' % (sName,str(cls.dictCmdFunc.keys())))
        # WeiYF.20150814 经测试发现，类装饰器使用的是全局变量。需要添加服务名前缀避免冲突
        f = cls.dictCmdFunc.get(sName, None)
        if f:
            tmBeg = time.time()
            r = f(cls, *args, **kwargs)
            fSeconds = time.time()-tmBeg
            if fSeconds>gfSecondsWarn:
                PrintMsTimeMsg("Spent_%.2fs_CallByName(%s,%s,%s)Out=(%s...)" % (
                    fSeconds,sName,str(args),str(kwargs),str(r)[:20]) )
            return r
        else:
            # raise ValueError('Method "{}" has not been registered'.format(sName))
            return ['ES','404','Method "{}" has not been registered'.format(sName),'']

    def class_decorator(cls):
        if not hasattr(cls,'dictCmdFunc'): #WeiYF.20150813 解决继承问题
            cls.dictCmdFunc = {}
        sServiveName = GetServiceNameFromClassName(cls.__name__)  # cls.__name__[11:]
        for name, method in cls.__dict__.iteritems():
            if name.startswith(sPrefix):
                # print name, method.__name__, cls.__name__
                cls.dictCmdFunc[sServiveName+'.'+method.__name__[lenPrefix:]] = method
        setattr(cls, CallByName.__name__, CallByName)
        return cls
    return class_decorator

@RegisterForHandleCmdService()
class CHandleCmd_BaseService:
    """
        命令处理服务类，命名约定如下：
            类名固定采用 CHandleCmd_ 前缀，后面是服务名；
            服务函数固定采用 cmd_ 前缀，后面是命令字名；
    """
    def __init__(self):
        sClassName = self.__class__.__name__
        self.sServiveName = GetServiceNameFromClassName(sClassName)
        if self.sServiveName:
            PrintTimeMsg("CHandleCmd_BaseService.sServiveName=%s=!" % (self.sServiveName))
        else:
            PrintTimeMsg("CHandleCmd_BaseService.sClassName=%s=Error!EXIT!" % (sClassName))
            sys.exit(0)

    def __del__(self):
        pass

    def cmd_ListCmd(self, CmdIStr):
        lsCmd = sorted(self.dictCmdFunc.keys(),reverse=False)
        CmdOStr = ['OK','~'.join(lsCmd)]
        return CmdOStr

    def cmd_EchoCmd(self, CmdIStr):
        CmdOStr = ['OK',GetCurrentTime()]
        CmdOStr.extend(CmdIStr)
        return CmdOStr



@RegisterForHandleCmdService()
class CHandleCmd_BaseService1(CHandleCmd_BaseService):

    # def cmd_ListCmd(self, CmdIStr):
    #     return CHandleCmd_BaseService.cmd_ListCmd(self,CmdIStr)

    def cmd_JustForTest3(self,p):
        # do some stuff
        print "cmd_JustForTest3",p
        return "---------"+p

    def cmd_JustForTest(self,p):
        # do some stuff
        print "cmd_JustForTest",p
        return "---------"+p

    def cmd_JustForTest2(self,p):
        # do some stuff
        print "cmd_JustForTest2",p
        return "---------"+p

    def cmd_Echo(self, lsParam):
        lsRet = lsParam
        lsRet.append(str(self.args))
        return lsRet

    def cmd_EchoDict(self, dictParam):
        dictKV = dictParam
        dictKV['@Status'] = "000"
        # CmdOStr = ["000"]
        # for k,v in dictKV.items():
        #     CmdOStr.append('%s %s' % (k,v))
        return dictKV#CmdOStr

def TestCmdHandleBase():
    m = CHandleCmd_BaseService1()
    print m.CallByName('BaseService.JustForTest', '******')
    print m.CallByName('BaseService.JustForTest2', '******')
    print m.CallByName('BaseService.JustForTest3', '******')
    print m.CallByName('BaseService1.JustForTest3', '******')
    print m.CallByName('BaseService.ListCmd',[])
    print m.CallByName('BaseService.EchoCmd',(1,2,3,4))
    print m.CallByName('BaseService1.ListCmd', [])


#-------------------------------
if __name__ == '__main__':
    TestCmdHandleBase()
