from distutils.core import setup
setup(
		name = 'instantcricket',
		packages = ['instantcricket'],
		version = '0.6',
		description = 'get instant cricket score from cricbuzz as notifications',
		author = 'Hirendra Thakur',
		author_email = 'hirendrathakur1993@gmail.com',
		url = 'https://github.com/hirendrathakur/instantcricket',
		download_url = 'https://github.com/hirendrathakur/instantcricket/tarball/0.6',
		keywords = [],
		license = 'MIT',
		scripts = ['bin/instantcricket'],
		install_requires = ['bs4'],
		classifiers = [],
		include_package_data=True
		)