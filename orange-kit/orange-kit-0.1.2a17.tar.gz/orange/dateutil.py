# 项目：标准库函数
# 模块：时间模块
# 作者：黄涛
# License:GPL
# Email:huangtao.sh@icloud.com
# 创建：2015-09-17 13:24
# 修改：2016-03-12 18:53
# 修改：2016-9-6 增加 ONEDAY,ONESECOND

import datetime as dt
import re

__all__='UTC','LOCAL','now','datetime','FixedOffset','ONEDAY',\
        'ONESECOND','date_add'

ZERO = dt.timedelta(0)
ONEDAY = dt.timedelta(days=1)
ONESECOND = dt.timedelta(seconds=1)

# A class building tzinfo objects for fixed-offset time zones.
# Note that FixedOffset(0, "UTC") is a different way to build a
# UTC tzinfo object.

class FixedOffset(dt.tzinfo):
    """Fixed offset in minutes east from UTC."""

    def __init__(self, offset, name):
        self.__offset = dt.timedelta(minutes = offset)
        self.__name = name

    def utcoffset(self, dt):
        return self.__offset

    def tzname(self, dt):
        return self.__name

    def dst(self, dt):
        return ZERO

    def __repr__(self):
        timezone=self.__offset.total_seconds()//60
        return "UTC%+i:%02i"%(divmod(timezone,60)) if timezone else "UTC"
        

UTC=FixedOffset(0,'UTC')

# A class capturing the platform's idea of local time.

import time as _time

STDOFFSET = dt.timedelta(seconds = -_time.timezone)
if _time.daylight:
    DSTOFFSET = dt.timedelta(seconds = -_time.altzone)
else:
    DSTOFFSET = STDOFFSET

DSTDIFF = DSTOFFSET - STDOFFSET

class LocalTimezone(dt.tzinfo):

    def utcoffset(self, dt):
        if self._isdst(dt):
            return DSTOFFSET
        else:
            return STDOFFSET

    def dst(self, dt):
        if self._isdst(dt):
            return DSTDIFF
        else:
            return ZERO

    def tzname(self, dt):
        return _time.tzname[self._isdst(dt)]

    def _isdst(self, dt):
        tt = (dt.year, dt.month, dt.day,
              dt.hour, dt.minute, dt.second,
              dt.weekday(), 0, 0)
        stamp = _time.mktime(tt)
        tt = _time.localtime(stamp)
        return tt.tm_isdst > 0
    
    def __repr__(self):
        offset=STDOFFSET.total_seconds()//60
        return "UTC%+i:%02i"%(divmod(offset,60))

LOCAL = LocalTimezone()

def now(tz=LOCAL):
    return dt.datetime.now(tz)

def datetime(*args,**kwargs):
    tzinfo=kwargs.get('tzinfo',LOCAL)
    if len(args)==1:
        d=args[0]
        if isinstance(d,(dt.datetime,dt.time)):
            '''
            如果是datetime或time类型，检查是否有tzinfo信息，
            如无，则设为LOCAL，否则直接返回
            '''
            if not d.tzinfo:
                d=d.replace(tzinfo=tzinfo)
            return d
        elif isinstance(d,str):
            '''将字符串转换为datetime类型'''
            args=[int(x) for x in re.findall('\d+',d)]
            return dt.datetime(*args,tzinfo=tzinfo)
        elif isinstance(d,(int,float)):
            '''将整数或浮点数转换成日期类型
            如果小于100000，则按Excel的格式转换；
            否则按unix timestamp 来转换'''
            from xlrd.xldate import xldate_as_datetime
            if d<100000:
                dd=xldate_as_datetime(d,None).replace(tzinfo=tzinfo)
            else:
                dd=dt.datetime.fromtimestamp(d,tzinfo)
            return dd
    else:
        kwargs['tzinfo']=tzinfo
        return dt.datetime(*args,**kwargs)
        
def date_add(date,years=0,months=0,**kw):
    '''日期及时间的加减,
    支持的参数有：years,months,days,hours,minutes,seconds'''
    year,month=date.timetuple()[:2]
    year,month=divmod((year+years)*12+month+months-1,12)
    date=date.replace(year=year,month=month+1)
    return date+dt.timedelta(**kw)
