# -*- encoding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name='weblate-tools',
    version='0.1.0',
    keywords=('weblate', 'translate'),
    description=u'weblate文本处理工具',

    url='https://github.com/zhufree/WeblateTools',
    author='zhufree',
    author_email='zhufree2013@gmail.com',

    packages=find_packages(),
    include_package_data=True,
    install_requires=list(map(lambda x: x.replace('==', '>=') and x.rstrip('\n'), open("requirements.txt").readlines())),
)