import shutil
import os

from distutils.command.clean import clean
from setuptools import setup, find_packages


class CleanCommand(clean):
    """Post-installation for installation mode."""
    def run(self):
        path = os.path.dirname(__file__)
        shutil.rmtree(os.path.join(path, 'dist'), ignore_errors=True)
        shutil.rmtree(os.path.join(path, 'build'), ignore_errors=True)
        shutil.rmtree(
            os.path.join(path, 'subways.egg-info'), ignore_errors=True
        )


setup(
    name='subways',
    version='0.1.0.dev7',
    packages=find_packages(),
    url='https://github.com/midoriiro/subways/',
    license=open('LICENSE').read(),
    author='midoriiro',
    author_email='contact@smartsoftwa.re',
    maintainer='midoriiro',
    maintainer_email='contact@smartsoftwa.re',
    description='A Python module that’s provide some basic utilities.',
    long_description=open('README.rst').read(),
    tests_require=['tox'],
    install_requires=[],
    cmdclass={
        'clean': CleanCommand,
    },
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'License :: OSI Approved',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Software Development :: Libraries'
    ],
)
