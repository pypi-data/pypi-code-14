from setuptools import setup, find_packages

def format(input, start = 0):
	result = ''
	indent = False
	count = 0

	with open(input, 'r') as file:
		for line in file:
			if count > start:
				if line[:1] == '\t' and not indent:
					indent = True
					result += '::\n\n'

				if line[:1].isalnum() and indent:
					indent = False

				result += line.replace('> ', '\t')
			count += 1

	return result

blurb = ('d3cryp7.py is a Python module for image analysis and recognition '
	'designed to decode, decrypt and understand the contents of an image.\n'
)

setup(
	name = 'd3cryp7.py',
	version = '0.2.0',
	author = 'Justin Willis',
	author_email = 'sirJustin.Willis@gmail.com',
	packages = find_packages(),
	include_package_data = True,
	zip_safe = False,
	url = 'https://bitbucket.org/bkvaluemeal/d3cryp7.py',
	license = 'ISC License',
	description = 'A Python module for image analysis and recognition',
	long_description = blurb + format('README.md', 3),
	entry_points = {
		'console_scripts': [
			'd3cryp7 = d3cryp7.__main__:main'
		]
	},
	classifiers = [
		'Development Status :: 1 - Planning',
		'Environment :: Web Environment',
		'Framework :: Flask',
		'Intended Audience :: Developers',
		'License :: OSI Approved :: ISC License (ISCL)',
		'Operating System :: OS Independent',
		'Programming Language :: Python :: 3',
		'Topic :: Scientific/Engineering :: Image Recognition'
	],
	keywords = 'image analysis',
	install_requires = [
		'flask',
		'flask_bootstrap',
		'flask_restful',
		'requests'
	]
)
