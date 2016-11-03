import os

from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='piqq',
    version='0.0.5',
    packages=['piqq', 'piqq.exceptions'],
    long_description=read('README.md'),
    url='https://git.hellotan.ru/jar3b/piqq',
    license='MIT',
    author='jar3b',
    author_email='hellotan@live.ru',
    description='PIQQ - The OOP-based add-on for aioamqp library',
    install_requires=[
        'aioamqp==0.8.2'
    ]
)
