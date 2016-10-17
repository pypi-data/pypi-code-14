#-*- encoding: UTF-8 -*-
from setuptools import setup, find_packages
"""
打包的用的setup必须引入，
"""
 
VERSION = '0.2'
 
setup(name='Koptool',
      version=VERSION,
      description="a tiny and smart cli player of douyutv,ximalayad,anmu based on Python",
      long_description='just enjoy',
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='python ksyun tools terminal',
      author='cjxcloud',
      author_email='cjxcloud@163.com',
      #url='https://github.com/cjx1994/utls/tree/master/ksyun.tools',
      license='MIT',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=True,
      install_requires=[
        'requests',
      ],
      entry_points={
        'console_scripts':[
            'koptool = ksyuntools.kop:execute'
        ]
      },
)
