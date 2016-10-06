#!/usr/bin/env python

import os
import sys
import uuid
from pip.req import parse_requirements
from codecs import open


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

packages = [
    'kafka_log_handler',
]

install_requirements = parse_requirements('requirements.txt', None, None, None, uuid.uuid1())
requirements = [str(ir.req) for ir in install_requirements]

with open('README.rst', 'r', 'utf-8') as f:
    readme = f.read()

setup(
    name='kafka_log_handler',
    version=1.2,
    description='Simple python logging handler for forwarding logs to a kafka server.',
    long_description=readme + '\n\n',
    maintainer="Damien Kilgannon",
    maintainer_email="kilgannon.damien@gmail.com",
    author='Damien Kilgannon',
    author_email='kilgannon.damien@gmail.com',
    url='https://github.com/damienkilgannon/kafka-log-handler.git',
    packages=packages,
    package_data={'': ['LICENSE.txt', 'README.rst']},
    include_package_data=True,
    install_requires=requirements,
    license='Apache 2.0',
    zip_safe=False,
    keywords=['python', 'logging', 'handler', 'example', 'kafka', 'logs', 'logstash', 'formatter'],
    classifiers=(
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
    ),
)
