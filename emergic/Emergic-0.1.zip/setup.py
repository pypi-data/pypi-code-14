# http://python-packaging.readthedocs.io/en/latest/minimal.html

from setuptools import setup

setup(name='Emergic',
    version='0.1',
    description='Emergic Network',
    long_description='The Emergic Network architecture',
    keywords='computational architecture cognitive neural model',
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',
        'Environment :: Win32 (MS Windows)',
        'Framework :: IDLE',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
    ],
    url='https://github.com/dpleibovitz/Emergic',
    author='David Pierre Leibovitz',
    author_email='dpleibovitz@ieee.org',
    license='GPLv3',
    packages=['Emergic'],
    zip_safe=False)
