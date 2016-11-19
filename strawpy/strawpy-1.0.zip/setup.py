from setuptools import setup

__version__ = '1.0'

setup(
    name='strawpy',
    version=__version__,

    packages=['strawpy'],

    description='Strawpy is a python wrapper for the strawpoll API.',
    author='Eric Dalrymple',
    author_email='ericjdalrymple@gmail.com',
    url='https://github.com/EricDalrymple91/strawpy',
    download_url='https://github.com/EricDalrymple91/strawpy/tarball/0.1',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing',
        'Topic :: Multimedia :: Graphics :: Capture',
        'Topic :: Multimedia :: Graphics :: Editors',
        'Topic :: Multimedia :: Graphics :: Presentation',
        'Topic :: Multimedia :: Graphics :: Viewers',
        'Topic :: Games/Entertainment'
    ],
    license='MIT',
    install_requires=[
        'requests'
    ],
 )
