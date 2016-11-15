# -*- coding: utf-8 -*-
from distutils.core import setup

setup(name = 'uiautomation',
      version = '1.0.1',
      description = 'Python UIAutomation for Windows',
      license = 'MIT',
      author = 'yinkaisheng',
      author_email = 'yinkaisheng@foxmail.com',
      url = 'https://github.com/yinkaisheng/Python-UIAutomation-for-Windows',
      platforms = 'Windows Only',
      py_modules = ['uiautomation'],
      data_files = ['AutomationClientX86.dll', 'AutomationClientX64.dll'],
      long_description = 'Python UIAutomation for Windows. Supports py2, py3, x86, x64',
      )

