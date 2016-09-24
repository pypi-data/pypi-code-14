#coding = utf-8

#元数据相关
from distutils.core import setup

setup(
    name            = 'P40_learning_distribution',
    version         = '2.0.0',
    py_modules      = ['printList'],
    author          = 'heheda',
    url             = 'http://www.headfirstlabs.com',
    author_email    = 'echislin123@live.com',
    description     = 'a simple printer of nested lists',
    )

""" 2.0.0版本在print_lol() 函数基础上引入了新的indent 入口参数，
    用于指明是否需要缩进。 indent=True => 缩进，indent=False => 不缩进
    与之前版本保持兼容。"""
