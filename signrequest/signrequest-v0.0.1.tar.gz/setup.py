from setuptools import setup

VERSION = '0.0.1'

try:
    import pypandoc
    description = pypandoc.convert('README.md', 'rst', format='markdown')
    print 'Converted README.md to rst'
except (IOError, ImportError):
    description = open('README.md').read()

setup(
    name='signrequest',
    license='MIT',
    version=VERSION,
    url='https://github.com/ivansabik/signrequest-python-client',
    download_url='https://github.com/ivansabik/signrequest-python-client/tarball/0.0.1',
    author='Ivan Rodriguez',
    author_email='ivan@britecore.com',
    description='Unofficial client for SignRequest API',
    long_description=description,
    packages=['SignRequest'],
    install_requires=['requests']
)
