# -*- coding: utf-8 -*-
from setuptools import setup, Extension

setup(
    name='automodel',

    version='0.5.4',

    # url='https://bitbucket.org/jlalmeidaf/automodel-server-with-hmmer',
    license='',
    author='João Luiz de Almeida Filho, Jorge Hernandez Fernandez',
    author_email='joaoluiz.af@gmail.com',
    keywords='protein modeling modeller automodel',
    description=u'Client of service for structure protein prediction',
    packages=['automodelexception', 'manual', 'MiniServer', 'model', 'modellingfiles', 'modellingstep', 'network', 'options', 'pdb', 'tests', 'window'],
    install_requires=['rpyc'],
    # package_data={'pdb': ['pdb_95.pir, pdb_95.bin']},
    include_package_data=True,
    scripts=['automodel.py']
)
