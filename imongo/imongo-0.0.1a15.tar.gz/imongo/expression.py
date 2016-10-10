# 项目：数据库库函数
# 模块：查询模块
# 作者：黄涛
# License:GPL
# Email:huangtao.sh@icloud.com
# 创建：2016-05-06
# 修订：2016-10-06

from mongoengine import *
from .paginate import Pagination
from functools import partial

__all__='Q','P','Aggregation'

def _func(self,_type,func,value=None):
    if _type==1:
        value=value or "$%s"%(self._name)
        if func=='count':
            func,value='sum',1
        return {self._name:{'$%s'%(func):value}}
    else:
        return Q(**{'%s__%s'%(self._name,func):value})

FUNCTION_LIST={'push':1,  # 聚合函数
       'addToSet':1,
       'first':1,
       'sum':1,
       'avg':1,
       'last':1,
       'max':1,
       'min':1,
       'count':1,
       # 以下为查询条件 
       'contains':2,
       'icontains':2,
       'startswith':2,
       'istartswith':2,
       'endswith':2,
       'iendswith':2,
       'nin':2,
       'match':2,
       'elemMatch':2,
       'exact':2,
       'iexact':2,
       'size':2,
       'all':2,
       # 'exists':2, 专用函数实现，主要用于设置默认参数
       'mod':2}

class _P(type):
    def __getattr__(self,name):
        return P(name)

    __getitem__=__getattr__
    
class P(metaclass=_P):
    '''查询条件字段类，返回一个统计条件或Q实例'''
    def __init__(self,name):
        self._name=name  # 字段名称
        self._neg=False  # 是否带负号

    def __repr__(self):
        return 'P(name="%s")'%(self._name)

    def __neg__(self):
        self._neg=not self._neg  # 加负号
        return self
            
    def __getattr__(self,name):
        type_=FUNCTION_LIST.get(name,None)
        if type_:
            return partial(_func,self,type_,name)
        else:
            raise Exception('功能%s不存在！'%(name))
        
    def __lt__(self,value):
        '''小于指定数值'''
        return _func(self,2,'lt',value)

    def __gt__(self,value):
        '''大于指定数值'''
        return _func(self,2,'gt',value)

    def __le__(self,value):
        '''小于或等于指定数值'''
        return _func(self,2,'lte',value)

    def __ge__(self,value):
        '''大于或等于指定数值'''
        return _func(self,2,'gte',value)

    def __eq__(self,value):
        '''等于指定数值'''
        return Q(**{self._name:value})

    def __ne__(self,value):
        '''不等于指定数值'''
        return _func(self,2,'ne',value)
    
    def between(self,min,max,flag=3):
        '''在两个数值之间
        flag:
        0-不包括头尾
        1-包括头不包括尾
        2-不包括头包括尾
        3-包括头和尾
        '''
        l_op='gt' if flag in (0,2) else 'gte'
        r_op='lt' if flag in (0,1) else 'lte'
        return Q(**{'%s__%s'%(self._name,l_op):min}) & \
          Q(**{'%s__%s'%(self._name,r_op):max})

    def in_(self,value):
        '''在列表中'''
        return _func(self,2,'in',value)

    def regex(self,value):
        '''正则表达式匹配'''
        return Q(__raw__={self._name:{'$regex':value}})

    def exists(self,val=True):
        val=1 if val else 0
        return Q(__raw__={self._name:{'$exists':val}})

class Aggregation:
    def __init__(self,document,pipeline=None,**kw):
        if issubclass(document,Document):
            self.collection=document._get_collection()
        else:
            self.collection=document.collection()
        self.pipeline=pipeline or []
        self.kw=kw or {}

    def all(self):
        '''返回所有值'''
        return [i for i in self]
        
    def __iter__(self):
        '''迭代返回所有值'''
        return self.collection.aggregate(self.pipeline,**self.kw)

    __call__=__iter__
    
    def paginate(self, page, per_page=20, error_out=True):
        """Returns `per_page` items from page `page`.  By default it will
        abort with 404 if no items were found and the page was larger than
        1.  This behavor can be disabled by setting `error_out` to `False`.

        Returns an :class:`Pagination` object.
        """
        if error_out and page < 1:
            abort(404)
        pipeline=self.pipeline.copy()
        pipeline.append({'$skip':(page-1)*per_page})
        items=[i for i in \
               self.collection.aggregate(pipeline,**self.kw)]
        total=(page-1)*per_page+len(items)
        items=items[:per_page]
        if not items and page != 1 and error_out:
            abort(404)
   
        # No need to count if we're on the first page and there are fewer
        # items than we expected.
        return Pagination(self, page, per_page, total, items)

    def project(self,*args,**kw):
        '''过滤字段'''
        for arg in args:
            if isinstance(arg,P):
                kw[arg._name]=not arg._neg
            elif isinstance(arg,str):
                if arg.statswith('-'):
                    kw[arg[1:]]=False
                else:
                    kw[arg]=True
        self.pipeline.append({'$project':kw})
        return self

    def match(self,kw):
        '''条件过滤'''
        if hasattr(kw,'to_query'):
            kw=kw.to_query(None)
        self.pipeline.append({'$match':kw})
        return self

    def unwind(self,projection):
        '''打开列表字段'''
        if isinstance(projection,P):
            projection=projection._name
        if not projection.startswith('$'):
            projection='$%s'%(projection)
        self.pipeline.append({'$unwind':projection})
        return self
    
    def group(self,*args):
        '''聚合字段'''
        _id={}
        kw={}
        for project in args:
            if isinstance(project,P):
                _id.update({project._name:"$%s"%(project._name)})
            else:
                kw.update(project)
        kw['_id']=_id.popitem()[-1] if len(_id)==1 else _id
        self.pipeline.append({'$group':kw})
        return self

    def sort(self,*args,**kw):
        '''对字段进行排序'''
        for arg in args:
            kw[arg._name]=-1 if arg._neg else 1
        self.pipeline.append({'$sort':kw})
        return self

    def skip(self,num):
        '''跳过记录'''
        self.pipeline.append({'$skip':num})
        return self

    def limit(self,num):
        '''限制输出记录'''
        self.pipeline.append({'$limit':num})
        return self

    def export(self,filename,sheetname='sheet1',range_="A1",columns=None,\
               mapper=None):
        '''导出数据'''
        pass
        
        
               

