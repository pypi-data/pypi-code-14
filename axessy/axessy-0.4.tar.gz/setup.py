import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='axessy',
    version='0.4',
    packages=find_packages(),
    include_package_data=True,
    install_requires=['pytz', 'requests'],
    license='GPL',  
    description='A simple packet to read and parse messages from AXESS TMC X3 devices.',
    long_description=README,
    url='https://github.com/OpenInfoporto/axessy',
    author='Infoporto La Spezia Srl',
    author_email='',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',  
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5'
    ],
) 
