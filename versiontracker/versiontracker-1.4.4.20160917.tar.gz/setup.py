import os.path
from setuptools import find_packages, setup

_folder_path = os.path.dirname(__file__)
_version_path = os.path.join(_folder_path, 'versiontracker', '_version.py')
with open(_version_path) as f:
    exec(f.read())
version = __version__
git_url = 'https://gitlab.com/gallaecio/versiontracker'
with open(os.path.join(_folder_path, 'requirements.txt')) as f:
    requirements = f.read().splitlines()

setup(
    name='versiontracker',
    version=version,
    description="Web scrapping software to keep track of the latest stable "
                "version of different software.",
    url='http://version-tracker.rtfd.io/',
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
    packages=find_packages('.'),
    install_requires=requirements,
    package_data={
        'versiontracker': ['data.json'],
    },
    entry_points={
          'console_scripts': [
              'versiontracker = versiontracker.__main__:_main'
          ]
      },
)
