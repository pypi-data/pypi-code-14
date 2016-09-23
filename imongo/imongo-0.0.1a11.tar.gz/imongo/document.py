# 项目：数据库模型
# 模块：文档
# 作者：黄涛
# License:GPL
# Email:huangtao.sh@icloud.com
# 创建：2016-05-07 09:13
# 修订：2013-08-05 11:08

import bson
import mongoengine
from mongoengine import *
from orange import classproperty, Path, LOCAL, datetime

from .expression import *
from .paginate import Pagination


def abort(*args,**kwargs):
    import flask
    flask.abort(*args,**kwargs)

def _split(data,step=10000):
    length=len(data)
    i=0
    for i in range(step,length,step):
        yield data[i-step:i]
    else:
        yield data[i:]

class Document(mongoengine.Document):
    '''文档的基类'''
    meta={'abstract':True}
    _textfmt=''    # 文本格式
    _htmlfmt=''    # 超文本格式
    _load_mapper=None  # 导入数据时的表头，主要用于跳过标题行
    _load_header=None  # 导入数据时的表头，主要用于跳过标题行，
                       # 可以是一个字段，也可以是多个字段，必须为list或
                       # tuple或str
    
    @classmethod
    def load_files(cls,*files,clear=False,dup_check=True,**kw):
        '''通过文件批量导入数据
        files: 导入文件清单
        clear：清理原表中的数据，默认为不清理
        dup_check：重复导入检查，默认为检查
        kw：其他参数
        '''
        from .loadcheck import LoadFile
        if dup_check and clear:
            # 如果检查重复为真，则检查文件
            files=LoadFile.check(cls.__name__,*files)
        if clear:
            # 导入前清理数据
            cls.drop_collection()
        for filename in files:
            # 处理文件
            filename = Path(filename)
            kw['filename']=filename
            ext = filename.lsuffix
            if ext=='.del':
                cls.load_data([d for d in filename], **kw)
            elif ext in ('.txt','.csv'):
                cls.load_txtfile(**kw)
            elif ext.startswith('.xls'):
                for index, sheetname, data in filename.iter_sheets():
                    if data:
                        cls.load_sheet(data=data,sheetname=sheetname,
                                       index=index,**kw)
        if dup_check and clear:
            LoadFile.save(cls.__name__,*files)
            
    @classmethod
    def load_sheet(cls,data,sheetname,index,**kw):
        # 逐表处理excel文件
        cls.load_data(data,**kw)
        
    @classmethod
    def load_txtfile(cls,filename,sep=',',**kw):
        # 处理文本文件
        data = [d.split(sep) for d in filename.lines]
        cls.load_data(data,**kw)

    @classproperty
    def _fields_without_id(cls):
        # 查询除id以外的字段名
        fields=list(cls._fields_ordered)
        if 'id' in fields:
            fields.remove('id')
        return fields

    @classmethod
    def _check_row(cls,row):
        return row
    
    @classmethod
    def _batch_insert(cls,data):
        cls._get_collection().insert_many(data)
    
    @classmethod
    def load_data(cls,data,fields=None,mapper=None,quote=None,
                  header=None,**kw):
        # 批量导入数据
        def extract_str(x):
            if isinstance(x,str)and x.startswith(quote)and \
              x.endswith(quote):
                x=x[1:-1].strip()
            return x
        mapper=mapper or cls._load_mapper
        header=header or cls._load_header
        if isinstance(header,str):
            header=(header,)
        fields=fields or cls._fields_without_id
        if(not header)and isinstance(mapper,dict):
            header=[x for x in mapper.values()if isinstance(x,str)]

        if header:
            for i,row in enumerate(data):
                if all(x in row for x in header):
                    break
            if isinstance(mapper,dict):
                new_mapper={x:row.index(y) for x,
                            y in mapper.items() if isinstance(y,str)}
                mapper.update(new_mapper)
                mapper=[mapper[x] for x in fields]
            data=data[i+1:]
        datas=[]
        fields=[cls._translate_field_name(x) for x in fields]
        field_count =len(mapper) if mapper else len(fields)
        def add(row):
            d = cls._check_row(row)
            if d:
                datas.append(dict(zip(fields, d)))
        if mapper:
            [add([row[x] for x in mapper]) for row in data\
             if len(row)>=field_count]
        else:
            [add(row) for row in data if len(row)>=field_count]
        if datas:
            cls._batch_insert(datas)
    
    @property
    def _text(self):
        # 返回本实例的文本格式
        return self._textfmt.format(self=self)

    def __str__(self):
        # 返回本实例的文本格式
        return self._text if self._textfmt else super().__str__()
    
    @property
    def _html(self):
        # 返回本实例的超文本格式
        return self._htmlfmt.format(self=self)
    
    @classproperty
    def aggregation(cls):
        return Aggregation(cls)

def paginate(query, page, per_page=20, error_out=True):
    """Returns `per_page` items from page `page`.  By default it will
    abort with 404 if no items were found and the page was larger than
    1.  This behavor can be disabled by setting `error_out` to `False`.

    Returns an :class:`Pagination` object.
    """
    if error_out and page < 1:
        abort(404)

    total=query.count()
    items=query[(page-1)*per_page:min(total+1,(page)*per_page)]
    if not items and page != 1 and error_out:
        abort(404)
    
    # No need to count if we're on the first page and there are fewer
    # items than we expected.
    return Pagination(query, page, per_page, total, items)

# 为Document默认的QuerySet增加分页功能

# 为FixedOffset增加__repr__功能

def __repr__(self):
    '''FixedOffset的文本形式'''
    offset=self._FixedOffset__offset.total_seconds()//60
    if offset:
        return "UTC%+i:%02i"%(divmod(offset,60))
    else:
        return "UTC"

bson.tz_util.FixedOffset.__repr__=__repr__
mongoengine.QuerySet.paginate=paginate

def _first_or_404(self):
    '''查找第一条记录，否则返回404异常'''
    return self.first() or abort(404)

QuerySet.first_or_404=_first_or_404

class DateTimeField(DateTimeField):
    '''对DateTimeField字段进行修改，赋值时确保带时区，读取时转换为本地时区'''
    def __get__(self,instance,_type):
        value=super().__get__(instance,_type)
        return value.astimezone(LOCAL)

    def __set__(self,instance,value):
        return super().__set__(instance,datetime(value))


