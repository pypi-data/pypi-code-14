''' 模块安装文件  '''
from distutils.core import setup

setup(
    name = 'nester_zzh', #想要命名的对应模块名称，随意
    version = '1.2.1',
    py_modules = ['nester'], #要打包哪些，.py文件，不要加后缀.py。
    author = 'zhengzhihan',
    author_email = '21414474@qq.com',
    url = 'http://localhost',
    description = '这是hfpyhon第二章中的发布文件',
    )
