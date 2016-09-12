from setuptools import setup
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst')) as f:
    long_description = f.read()
version = '1.0.3'

setup(
    name='nanonispy',
    version=version,
    description='Library to parse Nanonis files.',
    long_description=long_description,
    url='https://github.com/underchemist/nanonispy',
    download_url = 'https://github.com/underchemist/nanonispy/tarball/'+version,
    author='Yann-Sebastien Tremblay-Johnston',
    author_email='yanns.tremblay@gmail.com',
    license='MIT',
    platforms=['any'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Physics',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5'
    ],
    keywords='data science numpy binary file parse',
    packages=['nanonispy', 'nanonispy.tests'],
    package_data={'nanonispy': ['LICENSE', 'README.md'], },
    install_requires=['numpy', ],
    tests_require=['nose', 'coverage', ],
    include_package_data=True,
)
