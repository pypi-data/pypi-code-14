from distutils.core import setup

setup(
    name = 'act_python',
    version = '0.1.0',
    description = 'A Python package example',
    author = 'Yifei',
    author_email = 'liuyifei0226@gmail.com',
    url = 'https://github.com/liuyifei0226/act_python-py', 
    py_modules=['act_python'],
    install_requires=[
        # list of this package dependencies
    ],
    entry_points='''
        [console_scripts]
        act_python=act_python:myfunc
    ''',
)