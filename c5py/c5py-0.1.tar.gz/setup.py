import sys
from setuptools import setup, find_packages

setup(
    name="c5py",
    version='0.1',
    description=("Analysis and visualization tools for the Augmented "
                 "Reality-based Corpus (ARbC). This corpus has been "
                 "created in the research project 'Alignment in AR-based "
                 "cooperation' which was a part of the Collaborative Research "
                 "Centre 'Alignment in Communication' (CRC 673) under the "
                 "project code C5."),
    maintainer='Alexander Neumann',
    maintainer_email='alneuman@techfak.uni-bielefeld.de',
    url='http://wwwhomes.uni-bielefeld.de/sfb-673/',
    packages=find_packages(exclude=['tests', 'test_*', 'archive']),
    # install_requires=['PyQt4', 'cv', 'numpy'],
    license='MIT',
    download_url='https://github.com/aleneum/c5py/archive/0.1.tar.gz',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Development Status :: 3 - Alpha',
        'Topic :: Multimedia :: Sound/Audio :: Analysis',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Scientific/Engineering :: Human Machine Interfaces',
        'Topic :: Scientific/Engineering :: Visualization'
    ],
    entry_points={
      'console_scripts': [
          'c5sync = c5.tools.sync.startup:startApp'
      ]
    },
)
