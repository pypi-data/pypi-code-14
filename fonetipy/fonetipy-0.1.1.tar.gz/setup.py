# -*- coding: utf-8 -*-
from setuptools import setup

setup(
    name='fonetipy',
    version='0.1.1',
    url='https://github.com/arthur-alves/fonetipy',
    license='MIT License',
    author='Arthur Alves',
    author_email='arthur.4lves@gmail.com',
    keywords='buscabr fonetipy fonetico',
    description=u'BuscarBr Python Algorithm',
    packages=['fonetipy'],
    install_requires=["Unidecode==0.04.19", "argparse==1.2.1", "wsgiref==0.1.2"],
)
