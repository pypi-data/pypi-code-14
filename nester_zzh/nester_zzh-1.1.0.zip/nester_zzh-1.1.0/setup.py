''' 模块安装文件  '''
from distutils.core import setup

setup(
    name = 'nester_zzh', #这个是最终打包的文件名
    version = '1.1.0',
    py_modules = ['nester.py'], #要打包哪些，.py文件
    author = 'zhengzhihan',
    author_email = '21414474@qq.com',
    url = 'http://localhost',
    description = '这是hfpyhon第二章中的发布文件',
    )
