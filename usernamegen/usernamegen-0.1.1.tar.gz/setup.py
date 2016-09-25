from setuptools import setup
from usernamegen import __version__

try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except(IOError, ImportError):
    long_description = open('README.md').read()

setup(
    name='usernamegen',
    packages=['usernamegen', 'usernamegen.Formatter'],
    scripts=['bin/markov', 'bin/username'],
    version=__version__,
    description='Genrate usernames with a Markov chain based on a wordlist',
    long_description=long_description,
    author='Chris Landa',
    author_email='stylesuxx@gmail.com',
    url='https://github.com/stylesuxx/usernamegen/',
    download_url=('https://github.com/stylesuxx/usernamegen/tarball/%s' %
                  (__version__)),
    license='MIT',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Internet :: WWW/HTTP',
    ],)
