from __future__ import print_function

import os
import platform
import re
import sys
from codecs import open
from os import path
from subprocess import Popen, PIPE
from textwrap import dedent

SUPPORTED_PYTHON_VERSIONS = [(2,7), (3,4), (3,5)]

def long_description():
    here = path.abspath(path.dirname(__file__))
    with open(path.join(here,'README.rst'), encoding='utf-8') as f:
        return f.read()

def read_version():
    here = path.abspath(path.dirname(__file__))
    with open(path.join(here,'tecplot','version.py'), encoding='utf-8') as f:
        m = re.search(r"version = '(.*?)'",f.read(),re.M)
        return m.group(1)

def write_coveragerc(filename):
    fmt = dedent("""\
        [report]
        # Regexes for lines to exclude from consideration
        exclude_lines =
            pragma: no cover
        {pyver}
        {system}
            if 0:
            if False:
            if __name__ == .__main__.:

        omit =
            tecplot/tecutil/constant.py
            tecplot/tecutil/sv.py
            tecplot/tecutil/tecutil.py
    """)

    opts = {}

    version = sys.version_info[:2]
    assert version in SUPPORTED_PYTHON_VERSIONS

    opts['pyver'] = ''
    verops = ['<=?', '[<>]', '>=?']
    for v in SUPPORTED_PYTHON_VERSIONS:
        if v == version:
            verops.pop(0)
        opts['pyver'] += """\
    if sys\.version_info {op} \({0}
    if sys\.version_info {op} \({0},{1}
""".format(*v, op=verops[0])
        if v == version:
            verops.pop(0)

    lin = '[Ll]inux'
    win = '[Ww]indows'
    mac = '[Dd]arwin'
    if platform.system() == 'Windows':
        target = win
        others = (lin,mac)
    elif platform.system() == 'Darwin':
        target = mac
        others = (win,lin)
    else: #if platform.system() == 'Linux':
        target = lin
        others = (win,mac)

    opts['system'] = """\
    if platform\.system.*(?!{0})

    def.*{1}.*(?!{0})
    def.*(?!{0}).*{1}
    def.*{2}.*(?!{0})
    def.*(?!{0}).*{2}
""".format(target,*others)

    with open(filename, 'w') as fout:
        fout.write(fmt.format(**opts))

def install_requires():
    req = ['six']
    if sys.version_info < (3,0):
        req.append('future')
        req.append('contextlib2')
    if sys.version_info < (3,4):
        req.append('enum34')
    return req

def test_requires():
    req = ['coverage']
    if sys.version_info < (3,3):
        req.append('mock')
    return req

def extra_requires():
    return ['numpy', 'ipython', 'pillow']

def doc_requires():
    req = ['sphinx', 'sphinxcontrib-napoleon']
    if sys.version_info < (3,3):
        req.append('mock')
    return req

def setup_opts():
    from setuptools import find_packages
    opts = dict(
        name='pytecplot',
        version=read_version(),
        description='A python interface to Tecplot 360 EX',
        long_description=long_description(),
        #url='http://www.tecplot.com/pytecplot',
        url='http://www.tecplot.com/docs/pytecplot',
        author='Tecplot, Inc.',
        author_email='support@tecplot.com',
        #license='',
        classifiers=[
            # Development Status
            #   1 - Planning
            #   2 - Pre-Alpha
            #   3 - Alpha
            #   4 - Beta
            #   5 - Production/Stable
            'Development Status :: 3 - Alpha',
            'Intended Audience :: Developers',
            'Intended Audience :: Education',
            'Intended Audience :: End Users/Desktop',
            'Intended Audience :: Science/Research',
            'Natural Language :: English',
            'Operating System :: OS Independent',
            'Topic :: Education',
            'Topic :: Multimedia :: Graphics :: 3D Rendering',
            'Topic :: Multimedia :: Graphics :: Presentation',
            'Topic :: Multimedia :: Graphics :: Viewers',
            'Topic :: Scientific/Engineering',
            'Topic :: Scientific/Engineering :: Information Analysis',
            'Topic :: Scientific/Engineering :: Mathematics',
            'Topic :: Scientific/Engineering :: Physics',
            'Topic :: Scientific/Engineering :: Visualization',
            'Topic :: Software Development :: Libraries',
            'Topic :: Software Development :: Libraries :: Python Modules',
            'License :: Other/Proprietary License',
            'Programming Language :: Python',
            'Programming Language :: Python :: 2',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
        ],
        keywords= [
            'tecplot',
            'cfd',
            'data analysis',
            'scientific',
            'scientific computing',
            'statistics',
            'visualization',
        ],
        packages=find_packages(),
        install_requires=install_requires(),
        extras_require={
            'extras' : extra_requires(),
            'doc' : doc_requires(),
            'test' : test_requires(),
            'all' : extra_requires() + doc_requires() + test_requires(),
        },
    )
    return opts

if __name__ == '__main__':
    import struct

    version = sys.version_info[:2]
    if version not in SUPPORTED_PYTHON_VERSIONS:
        err = 'PyTecplot only supports python versions: '
        err += ', '.join(['.'.join(v) for v in SUPPORTED_PYTHON_VERSIONS])
        raise Exception(err)

    pointer_size = struct.calcsize('P')
    if pointer_size != 8:
        err = 'ERRROR: {} bit architecture detected.\n'.format(pointer_size*8)
        err += 'PyTecplot must be used with a 64-bit version of Python.'
        raise Exception(err)

    try:
        write_coveragerc('.coveragerc')
    except OSError:
        log.info(dedent('''\
            Could not write .coveragerc file.
            Do you have write permissions?
        '''))

    from setuptools import setup
    setup(**setup_opts())
