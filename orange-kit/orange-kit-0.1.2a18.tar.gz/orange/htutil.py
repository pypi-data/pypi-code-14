# 项目：标准库函数
# 模块：运行库
# 作者：黄涛
# License:GPL
# Email:huangtao.sh@icloud.com
# 创建：2016-04-13 20:46

import os

class classproperty:
    '''类属性，用法：
    class A:
        @classproperty
        def name(cls):
              return cls.__name__

    A.name
    A().name
    '''
    def __init__(self,getter):
        self.getter=getter

    def __get__(self,instance,kclass):
        return self.getter(kclass)
                    
def read_shell(cmd):
    '''
    执行系统命令，并将执行命令的结果通过管道读取。
    '''
    with os.popen(cmd)as fn:
        k=fn.read()
    return k.splitlines()

def write_shell(cmd,lines):
    '''
    执行系统命令，将指定的文通过管道向该程序输入。
    '''
    with os.popen(cmd,'w') as fn:
        if isinstance(lines,str):
            fn.write(lines)
        elif type(lines)in(tuple,list):
            [fn.write('%s\n'%(x))for x in lines]

def exec_shell(cmd):
    '''
    执行系统命令。
    '''
    return os.system(cmd)

def wlen(s):
    '''
    用于统计字符串的显示宽度，一个汉字或双字节的标点占两个位，
    单字节的字符占一个字节。
    '''
    return sum([2 if ord(x)>127 else 1 for x in s])
        
        
def __get_des():
    from .pyDes import des,PAD_PKCS5
    return des(key='huangtao',padmode=PAD_PKCS5)

def encrypt(pwd):
    '''
    可逆加密程序。
    '''
    b=__get_des().encrypt(pwd)
    return "".join(['%02X'%(x)for x in b])

def decrypt(code):
    '''
    解密程序。
    '''
    b=__get_des().decrypt(bytes.fromhex(code))
    return b.decode('utf8')

def get_py(s):
    '''
    获取拼音字母。
    '''
    from pypinyin import pinyin
    return ''.join([x[0] for x in pinyin(s,style=4)])

