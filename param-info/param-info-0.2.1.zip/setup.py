# Copyright (C) 2016 Napuzba [kobi@napuzba.com]
# Licensed under MIT license [http://openreq.source.org/licenses/MIT]

from setuptools import setup

description = 'A python package for parsing parameters.'

long_description = '''
=====
About
=====

A python package for parsing parameters

*****
Usage
*****

>>> from param_info import *
>>> params = ParamList()
>>> params.add( ParamInfoInt("a1",7,min=5) )
>>> params.add( ParamInfoVal("a2",['aa','bb','cc']) )
>>> params.add( ParamInfoStr("a3",' hallo ') )
>>> def doSomething(param,values):
...    if params.validate(values):
...        # Do something with values
...        for name,param in params.params.items():
...            print( '{0} ==> {1}'.format(name,param.value))
...    else:
...        # Handle errors
...        for name,param in params.errors.items():
...            print( 'Error. {0} ==> {1}'.format(name,param.errorText))
>>> doSomething(params,{'a1':3})
Error. a1 ==> a1=3 should be integer >= 5
Error. a2 ==> a2 is required
>>> doSomething(params,{'a1':8,'a2':'bb'})
a1 ==> 8
a2 ==> bb
a3 ==> hallo
>>> doSomething(params,{'a2':'zz'})
Error. a2 ==> a2=zz should be one of ['aa', 'bb', 'cc']
>>> doSomething(params,{'a2':'aa','a3':'hola'})
a1 ==> 7
a2 ==> aa
a3 ==> hola

'''

setup(
  name             = 'param-info',
  packages         = ['param_info'],
  install_requires = [
    
  ],
  version          = '0.2.1',
  author           = 'napuzba',
  author_email     = 'kobi@napuzba.com',
  url              = 'https://github.com/napuzba/param-info.git',
  download_url     = 'https://github.com/napuzba/param-info/releases',
  description      = description,
  long_description = long_description,
  license          = 'MIT',
  keywords         = ['validate'],
  classifiers      = [
    'Topic :: Software Development :: Libraries :: Python Modules',

    'Programming Language :: Python :: 3',
    'Operating System :: OS Independent',
    'License :: OSI Approved :: MIT License',

    'Development Status :: 3 - Alpha'
  ],
)
