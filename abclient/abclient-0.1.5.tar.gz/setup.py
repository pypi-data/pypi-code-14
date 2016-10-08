# Copyright (c) 2016 Shanghai EISOO Information Technology Corp.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the Licensemport setuptools

from setuptools import setup, find_packages

packages = find_packages(exclude=['contrib', 'docs', 'tests*'])
requires=[]

with open('README.rst', 'r') as f:
    readme = f.read()

setup(
    name='abclient',
    version='0.1.5',
    description='Python client library for EISOO AnyBackup API',
    long_description=readme,
    author='EISOO',
    author_email='li.chunyu@eisoo.com',
    url='https://global.eisoo.com/',
    packages=packages,
    include_package_data=True,
    install_requires=requires,
    license='Apache 2.0',
    zip_safe=False,
    classifiers=(
        'Development Status :: 4 - Beta',
        'Environment :: OpenStack',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4'
    ),
)
