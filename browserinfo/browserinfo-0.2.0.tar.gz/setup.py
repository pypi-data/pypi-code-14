from setuptools import setup

from browserinfo import __version__, __repository__

try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except(IOError, ImportError):
    long_description = open('README.md').read()

setup(
    name='browserinfo',
    packages=['browserinfo'],
    version=__version__,
    description='API wrapper for browser-info.net - retrieve UA strings',
    long_description=long_description,
    author='Chris Landa',
    author_email='stylesuxx@gmail.com',
    url=__repository__,
    download_url=('https://github.com/stylesuxx/browserinfo/tarball/%s' %
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
