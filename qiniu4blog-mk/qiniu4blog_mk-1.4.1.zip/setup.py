#encoding:utf-8
from setuptools import setup, find_packages
import sys, os

version = '1.4.1'

setup(name='qiniu4blog_mk',
      version=version,
      description="写博客用的七牛图床",
      long_description="""The author of the origin version of this package is wzyuliyang, the current version is modified by mirsking""",
      classifiers=[],
      keywords='python qiniu',
      author='wzyuliyang, mirsking',
      author_email='wzyuliyang911@gmail.com, mirsking@gmail.com',
      url='https://github.com/wzyuliyang/qiniu4blog, https://github.com/mirsking/qiniu4blog',
      license='MIT License',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
        'qiniu',
		'pyperclip',
        'watchdog',
      ],
      entry_points={
        'console_scripts':[
            'qiniu4blog = qiniu4blog.qiniu4blog:main'
        ]
      },
)
