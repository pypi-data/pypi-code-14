"""
andrototal-cli
---------------
local_worker
"""
from setuptools import find_packages, setup


with open('README.rst', 'r') as f:
    long_description = f.read()

EXCLUDE_FROM_PACKAGES = ['docs._build','docs._template', 'docs._static']

setup(
    name='andrototal-cli',
    version='1.69',
    license='GPL',
	author='andrototal-org',
    description='local_worker package',
	url='https://github.com/andrototal-org/andrototal-cli/',
	download_url='http://github.com/andrototal-org/andrototal-cli/tarball/master/#egg=andrototal-cli-1.0',
    long_description=long_description,
    packages=find_packages(exclude=EXCLUDE_FROM_PACKAGES),
 	entry_points = {
   	     "console_scripts": ['andrototal-cli = local_worker.scan_cli:main']
        },
	install_requires = ['adapters','andropilot'],
	dependency_links = ['https://github.com/andrototal-org/andropilot/tarball/master/#egg=andropilot-1.0',
						'https://github.com/andrototal-org/andrototal_adapters/tarball/master/#egg=adapters-1.0'],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.3',
        'Programming Language :: Python :: 2.4',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],
)
