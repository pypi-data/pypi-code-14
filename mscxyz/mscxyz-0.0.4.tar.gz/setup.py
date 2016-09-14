import os
from setuptools import setup

def read(fname):
	return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
	name = 'mscxyz',
	version = '0.0.4',
	author = 'Josef Friedrich',
	author_email = 'josef@friedrich.rocks',
	description = ('A command line tool to manipulate the XML based *.mscX and *.mscZ files of the notation software MuseScore.'),
	license = 'MIT',
	packages = ['mscxyz'],
	keywords = 'audio',
	url = 'https://github.com/Josef-Friedrich/mscxyz',
	install_requires = [
		'lxml', 'termcolor', 'tmep',
	],
	scripts = ['bin/mscx-manager'],
	long_description=read('README.rst'),
	classifiers = [
		'Development Status :: 3 - Alpha',
	],
	zip_safe=False,
)
