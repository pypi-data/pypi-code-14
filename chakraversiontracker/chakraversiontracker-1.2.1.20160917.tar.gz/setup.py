# coding=utf-8

import os.path
from setuptools import setup

_folder_path = os.path.dirname(__file__)
_version_path = os.path.join(_folder_path, 'chakraversiontracker',
                             '_version.py')
with open(_version_path) as f:
    exec(f.read())
version = __version__
git_url = 'https://gitlab.com/gallaecio/chakraversiontracker'
with open(os.path.join(_folder_path, 'requirements.txt')) as f:
    requirements = f.read().splitlines()

setup(
    name='chakraversiontracker',
    version=__version__,
    description="Software to detect packages in rolling repositories of "
                "Chakra that are out of date.",
    url='http://chakra-version-tracker.rtfd.io/',
    download_url='{}/repository/archive.tar.gz?ref=v{}'.format(
        git_url, version),
    author="Adrián Chaves (Gallaecio)",
    author_email='adriyetichaves@gmail.com',
    license='AGPLv3+',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Affero General Public License v3 or '
            'later (AGPLv3+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: System :: Archiving :: Packaging',
    ],
    packages=['chakraversiontracker'],
    install_requires=requirements,
    package_data={
        'chakraversiontracker': [
            'data.json',
            'templates/packages.cli',
            'templates/packages.txt',
            'templates/repositories.cli',
            'templates/repositories.txt',
        ],
    },
    entry_points={
          'console_scripts': [
              'chakraversiontracker = chakraversiontracker.__main__:_main'
          ]
      },
)
