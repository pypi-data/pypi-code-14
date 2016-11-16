#!/usr/bin/env python
#encoding=utf-8

#  Copyright (c) 2010 Franz Allan Valencia See
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.


"""Setup script for Robot's DatabaseLibrary distributions"""

from distutils.core import setup

import setuptools
import sys
import os

src_path = os.path.join(os.path.dirname(__file__), 'src')
sys.path.insert(0, src_path)

__version_file_path__ = os.path.join(src_path, 'DatabaseLibrary', 'VERSION')
__version__ = open(__version_file_path__, 'r').read().strip()

DESCRIPTION = """
由于原作者许久未更新版本了，因此我做了一点临时修改，目前最新版本0.8.7

0.8.1：修复了#1 sqlite3在windows下使用绝对路径的问题。
0.8.4：修复了pip安装的报错。
0.8.7：修复了pip安装的报错，增加描述文件。

原作者的pypi上版本只到0.6，因此pip安装的时候也只能下载到0.6的版本，
联系了作者没有响应，因此我自己也在pypi上创建了一个新的库，pypi地址：

https://pypi.python.org/pypi/robotframework-databaseslibrary

github地址：
https://github.com/qitaos/Robotframework-Database-Library/

github请在release页面下载最新的版本。

软件版权仍然属于原作者，我只是在原有database后面加了个s，方便大家用pip安装。

安装方法：

pip install robotframework-databaseslibrary

Installation :

pip install robotframework-databaseslibrary

原作者的databaselibrary地址： https://pypi.python.org/pypi/robotframework-databaseslibrary

Database Library contains utilities meant for Robot Framework’s usage. This can allow you to query your database after an action has been made to verify the results. This is compatible* with any Database API Specification 2.0 module.
"""[1:-1]

def main():
    setup(name         = 'robotframework-databaseslibrary',
          version      = __version__,
          description  = 'Database utility library for Robot Framework',
          long_description = DESCRIPTION,
          author       = 'qitaos',
          author_email = 'qitaos@gmail.com',
          url          = 'https://github.com/qitaos/Robotframework-Database-Library/',
          package_dir  = { '' : 'src'},
          packages     = ['DatabaseLibrary'],
          package_data = {'DatabaseLibrary': ['VERSION']},
          requires     = ['robotframework']
          )
        

if __name__ == "__main__":
    main()
