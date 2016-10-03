from setuptools import setup, find_packages

setup(
    name='confipy',
    version='0.0.1',
    packages=find_packages(),
    url='https://github.com/mansenfranzen/confipy',
    license='MIT',
    author='Franz Woellert',
    author_email='franz.woellert@gmail.com',
    description='A convenient config file reader.',
    install_requires=['PyYAML'],
    download_url = 'https://github.com/mansenfranzen/confipy/tarball/0.0.1',
    keywords = ['config', 'yaml']
)
