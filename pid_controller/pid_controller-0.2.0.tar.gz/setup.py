import os
from setuptools import setup, find_packages

import pid_controller

CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))

def get_reqs(*fns):
    lst = []
    for fn in fns:
        for package in open(os.path.join(CURRENT_DIR, fn)).readlines():
            package = package.strip()
            if not package:
                continue
            lst.append(package.strip())
    return lst

def readme():
    with open('README.md') as f:
        return f.read()

setup(
    name='pid_controller',
    version=pid_controller.__version__,
    description='Simple PID controller implementation',
    long_description=readme(),
    url='http://github.com/chrisspen/pid_controller',
    author='Chris Spencer',
    author_email='chrisspen@gmail.com',
    license='BSD',
    packages=find_packages(),
    include_package_data=True,
    install_requires=get_reqs('pip-requirements.txt'),
    zip_safe=False)
