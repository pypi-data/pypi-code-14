# 项目：标准库函数
# 模块：时间模块
# 作者：黄涛
# License:GPL
# Email:huangtao.sh@icloud.com
# 创建：2015-09-17 13:24
# 修改：2016-03-12 18:53
# 修改：2016-9-6 增加 ONEDAY,ONESECOND

import datetime as dt
import time as _time
from .regex import R

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

'''
def datetime(*args,**kwargs):
    tzinfo=kwargs.get('tzinfo',LOCAL)
    if len(args)==1:
        d=args[0]
        if isinstance(d,(dt.datetime,dt.time)):

            如果是datetime或time类型，检查是否有tzinfo信息，
            如无，则设为LOCAL，否则直接返回

            if not d.tzinfo:
                d=d.replace(tzinfo=tzinfo)
            return d
        elif isinstance(d,str):
            将字符串转换为datetime类型
            args=[int(x) for x in re.findall('\d+',d)]
            return dt.datetime(*args,tzinfo=tzinfo)
        elif isinstance(d,(int,float)):
            将整数或浮点数转换成日期类型
            如果小于100000，则按Excel的格式转换；
            否则按unix timestamp 来转换
            from xlrd.xldate import xldate_as_datetime
            if d<100000:
                dd=xldate_as_datetime(d,None).replace(tzinfo=tzinfo)
            else:
                dd=dt.datetime.fromtimestamp(d,tzinfo)
            return dd
    else:
        kwargs['tzinfo']=tzinfo
        return dt.datetime(*args,**kwargs)

    '''
class datetime(dt.datetime):
    '''日期类，支持从字符串转换'''
    def __new__(cls,*args,**kwargs):
        tzinfo=kwargs.get('tzinfo',LOCAL)
        if len(args)==1:
            d=args[0]
            if isinstance(d,datetime):
                return d
            elif isinstance(d,(dt.datetime,dt.time)):
                '''
                如果是DATETIME或TIME类型，检查是否有TZINFO信息，
                如无，则设为LOCAL，否则直接返回
                '''
                args=list(d.timetuple()[:6])
                args.append(d.microsecond)
                if d.tzinfo:
                    tzinfo=d.tzinfo
            elif isinstance(d,str):
                '''将字符串转换为DATETIME类型'''
                args=[int(x) for x in R/'\d+'/d]
            elif isinstance(d,(int,float)):
                '''将整数或浮点数转换成日期类型
                如果小于100000，则按EXCEL的格式转换；
                否则按UNIX TIMESTAMP 来转换'''
                if d<100000:
                    from xlrd.xldate import xldate_as_datetime
                    dd=cls(xldate_as_datetime(d,None))
                else:
                    dd=cls.fromtimestamp(d)
                return dd
        kwargs['tzinfo']=tzinfo
        if len(args)>7:
            args=args[:7]
        return dt.datetime.__new__(cls,*args,**kwargs)

    def add(self,years=0,months=0,**kw):
        '''增加日期，返回一个新的日期实例'''
        year,month=self.timetuple()[:2]
        year,month=divmod((year+years)*12+month+months-1,12)
        try:
            date=self.replace(year=year,month=month+1)
        except:
            # 加上年或月之后，如果没有对应的日，则以最后一天为准
            date=self.replace(year=year,month=month+2,day=1)-1
        return date+dt.timedelta(**kw)
        
    def __add__(self,days):
        '''增加日期，支持整数型'''
        if isinstance(days,int):
            days=dt.timedelta(days=days)
        return datetime(super().__add__(days))

    def __sub__(self,days):
        '''减少日期，支持整数类型'''
        if isinstance(days,(dt.datetime,dt.time)):
            return super().__sub__(days)
        return self.__add__(-days)

    @property
    def first_day_of_month(self):
        '''当月第一天'''
        return self.replace(day=1)

    @property
    def last_day_of_month(self):
        '''当月最后一天'''
        return self.add(months=1).first_day_of_month-1

    @property
    def is_weekend(self):
        '''是否为周末'''
        return self.weekday() in (5,6)

    @property
    def quartor(self):
        '''当前的季度，从1开始'''
        return (self.month-1) // 3 +1

    @property
    def squartor(self):
        '''当前季节的字符串'''
        return '%s-%s'%(self.year,self.quartor)
    
    def format(self,fmt):
        '''格式化'''
        return self.strftime(fmt)

    def iter(self,days,fmt=None):
        '''遍历日期，如果days 为整数，则遍历days 指定的天数,
        若days 为非整数，则days 应为终止的日期,
        fmt 为返回格式：如为字符串，则格式化日期；若为可调用对象，则调用该日期'''
        _convert=lambda x:x
        if isinstance(fmt,str):
            _convert=lambda x:x.strftime(fmt)
        elif callable(fmt):
            _convert=fmt
        if isinstance(days,int):
            end_day=self+days
        else:
            end_day=datetime(days)
        while self<end_day:
            yield _convert(self)
            self+=1

def date_add(dt,*args,**kw):
    '''日期及时间的加减,
    支持的参数有：years,months,days,hours,minutes,seconds'''
    return datetime(dt).add(*args,**kw)

def now(tz=LOCAL):
    return datetime(dt.datetime.now(tz))
