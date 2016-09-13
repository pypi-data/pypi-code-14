#!/usr/local/bin/python
# -*- coding:utf-8 -*-
"""    
    2015/10/14  WeiYanfeng
    公共函数 包
"""
from WyfPublicFuncs import GetCurrentTime,GetUnixTimeStr,GetUnixTimeLocal,GetLocalTime,GetYYYYMMDDhhnnss,\
    GetCurrentTimeMS,GetCurrentTimeMSs,GetTimeInteger,GetTimeIntMS

from WyfPublicFuncs import PrintInline,PrintNewline,PrintTimeMsg,PrintMsTimeMsg,PrintAndSleep,\
    LoopPrintSleep,PrettyPrintObj,PrettyPrintStr,printCmdString,printHexString,IsUtf8String

from WyfPublicFuncs import GetRandomInteger,ConvertStringToInt32,GetCodeFmString,crc32,md5,md5file

from WyfPublicFuncs import GetSrcParentPath,GetCriticalMsgLog,CAppendLogBase,WyfAppendToFile

from WyfPublicFuncs import RequestsHttpGet,RequestsHttpPost
from WyfPublicFuncs import CatchExcepExitTuple,CatchExcepExitParam

from WyfPublicFuncs import ClassForAttachAttr
from WyfPublicFuncs import GetSystemPlatform

from CSendSMTPMail import CSendSMTPMail
from CSendCustomMsgWX import CSendCustomMsgWX

from CSerialJson import CSerialJson

from SimpleShiftEncDec import SimpleShiftEncode,SimpleShiftDecode

from WyfSupplyFuncs import get_total_size
from WyfQueueThread import StartThreadDoSomething, CThreadCacheByQueue, CThreadDiscardDeal

from JsonRpcFuncs import GetRedisClient
from CAutoConnectRedis import CAutoConnectRedis

if __name__ == '__main__':
    pass