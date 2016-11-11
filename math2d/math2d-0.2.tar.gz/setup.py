from distutils.core import setup
from distutils.command.install_data import install_data

setup (
    name = 'math2d', 
    version = '0.2',
    description = '2D mathematics package for Python.',
    author = 'Morten Lind',
    author_email = 'morten@lind.dyndns.dk',
    url = 'http://git.automatics.dyndns.dk/?p=pymath2d.git',
    packages = ['math2d'],
    provides = ['math2d'],
    classifiers = [
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering',
    ],
    license = 'GNU General Public License v3'
)
