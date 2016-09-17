from distutils.core import setup

from browserinfo import __version__

setup(
    name='browserinfo',
    packages=['browserinfo'],
    version=__version__,
    description='API wrapper for browser-info.net',
    author='Chris Landa',
    author_email='stylesuxx@gmail.com',
    url='https://github.com/stylesuxx/browserinfo',
    download_url=('https://github.com/stylesuxx/browserinfo/tarball/%s' %
                  (__version__)),
    license='MIT')
