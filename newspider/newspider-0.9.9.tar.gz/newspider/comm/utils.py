# -*- coding: utf-8 -*-
class Utils:

    @classmethod
    def tag_of_object(cls, obj):
        tag = str(obj.__class__).split('.')[-1]
        return tag

    @classmethod
    def md5(cls,str):
        import md5
        m1 = md5.new()
        m1.update(str)
        return m1.hexdigest()

    @classmethod
    def get_attr_in_class(cls,className, attr,default):
        try:
            res = eval("%s.%s" %(className, attr))
            return res
        except Exception,e:
            return default

    @classmethod
    def conv2utf8(cls,content,from_encodeing="GBK"):
        return content.decode(from_encodeing,errors='ingore')#.encode('utf-8')
