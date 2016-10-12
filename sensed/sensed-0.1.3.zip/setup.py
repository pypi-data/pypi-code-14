import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

try:
    long_description = read('docs/README.rst')
except:
    long_description = 'A sensor network server and client library.'

scripts = ['scripts/sensed', 'scripts/senselog']
if os.name == 'nt':
    scripts.append('scripts/sensed.bat')
    scripts.append('scripts/senselog.bat')

with open('requirements.txt') as r:
    requirements=r.read().rstrip().split('\n')

setup(
    name='sensed',
    version='0.1.3',
    author='R. Cody Maden',
    author_email='signedlongint@gmail.com',
    description='A sensor network server and client library.',
    license='MIT',
    keywords='sensor network sensed',
    url='http://github.com/sli/sensed',
    download_url='https://github.com/sli/sensed/releases/tag/v0.1.3',
    packages=['sensed', ],
    scripts=scripts,
    install_requires=requirements,
    long_description=long_description,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Networking'
    ]
)
