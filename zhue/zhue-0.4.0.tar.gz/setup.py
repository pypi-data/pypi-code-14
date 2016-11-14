from setuptools import find_packages, setup


setup(
    name='zhue',
    version='0.4.0',
    license='GPL3',
    description='Python SDK for Philips Hue devices',
    long_description=open('README.rst').read(),
    author='Philipp Schmitt',
    author_email='philipp@schmitt.co',
    url='https://github.com/pschmitt/zhue',
    packages=find_packages(),
    install_requires=['requests', 'netdisco', 'simplejson']
)
