import sys
import setuptools

description = 'Websockets for python 3 (RFC 6455)'

py_version = sys.version_info[:2]
if py_version < (3, 4):
    raise Exception("asyncws requires Python >= 3.4")

setuptools.setup(
    name='asyncws',
    version=0.1,
    maintainer='Brecht Baeten',
    maintainer_email='brecht.baeten@gmail.com',
    url='https://github.com/BrechtBa/asyncws',
    description=description,
    long_description=description,
    download_url='',
    packages=['asyncws'],
    platforms='all',
    license='MIT'
)
