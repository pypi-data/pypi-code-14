import os
import sys

from setuptools import find_packages, setup


PYTHON3 = sys.version_info > (3, )
HERE = os.path.abspath(os.path.dirname(__file__))


def readme():
    with open(os.path.join(HERE, 'README.md')) as f:
        return f.read()


def get_version():
    with open(os.path.join(HERE, 'pygenerator/__init__.py'), 'r') as f:
        content = ''.join(f.readlines())
    env = {}
    if PYTHON3:
        exec(content, env, env)
    else:
        compiled = compile(content, 'get_version', 'single')
        eval(compiled, env, env)
    return env['__version__']


setup(
    name='pygenerator',
    description='Utilities to generate Python projects',
    version=get_version(),
    long_description=readme(),
    platforms=['any'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
    ],
    keywords='',
    url='https://github.com/rgs1/pygenerator',
    author='rgs',
    author_email='rgs@itevenworks.net',
    license='apache',
    packages=find_packages(),
    test_suite='pygenerator.tests',
    scripts=[
        'bin/pygenerator',
    ],
    install_requires=[],
    tests_require=[
        'nose'
    ],
    extras_require={
        'test': [],
    },
    include_package_data=True,
    zip_safe=False
)
