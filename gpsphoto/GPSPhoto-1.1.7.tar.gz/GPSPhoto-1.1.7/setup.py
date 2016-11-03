import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='GPSPhoto',
    version='1.1.7',
    packages=find_packages(),
    include_package_data=True,
    license='GPL License',  # example license
    description='Returns, Modifies, or Removes GPS Data from Exif Data in photo. Requires ExifRead, piexif.',
    long_description=README,
    url='http://www.jessgwiii.wordpress.com',
    author='Jess Williams',
    author_email='stripes.denomino@gmail.com',
)
