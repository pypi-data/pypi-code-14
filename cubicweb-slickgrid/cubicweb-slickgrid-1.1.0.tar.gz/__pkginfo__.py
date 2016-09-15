# pylint: disable=W0622
"""cubicweb-slickgrid application packaging information"""

import os.path as _osp

modname = 'slickgrid'
distname = 'cubicweb-slickgrid'

numversion = (1, 1, 0)
version = '.'.join(str(num) for num in numversion)

license = 'LGPL'
author = 'LOGILAB S.A. (Paris, FRANCE)'
author_email = 'contact@logilab.fr'
description = 'Table view rendered using the SlickGrid_ javascript librairy.'
web = 'http://www.cubicweb.org/project/%s' % distname

__depends__ = {'cubicweb': '>= 3.19.4'}
__recommends__ = {}

classifiers = [
    'Environment :: Web Environment',
    'Framework :: CubicWeb',
    'Programming Language :: Python',
    'Programming Language :: JavaScript',
    ]

from os import listdir as _listdir
from os.path import join, isdir
from glob import glob

THIS_CUBE_DIR = join('share', 'cubicweb', 'cubes', modname)


def listdir(dirpath):
    return [join(dirpath, fname) for fname in _listdir(dirpath)
            if fname[0] != '.' and not fname.endswith('.pyc')
            and not fname.endswith('~')
            and not isdir(join(dirpath, fname))]

data_files = [
    # common files
    [THIS_CUBE_DIR, [fname for fname in glob('*.py') if fname != 'setup.py']],
    ]
# check for possible extended cube layout
for dname in ('entities', 'views', 'sobjects', 'hooks', 'schema',
              'data', 'wdoc', 'i18n', 'migration', _osp.join('data', 'jQuery'),
              _osp.join('data', 'SlickGrid'),
              _osp.join('data', 'SlickGrid', 'controls'),
              _osp.join('data', 'SlickGrid', 'css'),
              _osp.join('data', 'SlickGrid', 'css', 'smoothness'),
              _osp.join('data', 'SlickGrid', 'css', 'smoothness', 'images'),
              _osp.join('data', 'SlickGrid', 'images'),
              _osp.join('data', 'SlickGrid', 'lib'),
              _osp.join('data', 'SlickGrid', 'plugins')):
    if isdir(dname):
        data_files.append([join(THIS_CUBE_DIR, dname), listdir(dname)])
# Note: here, you'll need to add subdirectories if you want
# them to be included in the debian package
