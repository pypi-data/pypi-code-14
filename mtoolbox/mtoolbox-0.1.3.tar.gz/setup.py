#pylint: skip-file
from distutils.core import setup

import mtoolbox

version = mtoolbox.__version__
description = mtoolbox.__doc__.split('\n')[0]

setup(
    name = 'mtoolbox',
    packages = ['mtoolbox'],
    version = version,
    description = description,
    author = 'Maik Messerschmidt',
    author_email = 'maik.messerschmidt@gmx.net',
    url = 'https://github.com/messersm/mtoolbox',
    download_url = 'https://github.com/messersm/mtoolbox/tarball/%s' % version,
    keywords = ['mtoolbox'],
    classifiers = [
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
