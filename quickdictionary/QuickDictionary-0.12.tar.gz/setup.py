from distutils.core import setup
setup(
		name = 'QuickDictionary',
		packages = ['QuickDictionary'],
		version = '0.12',
		description = 'just copy the word for to know its meaning,must be connected to internet',
		author = 'Hirendra Thakur',
		author_email = 'hirendrathakur1993@gmail.com',
		url = 'https://github.com/hirendrathakur/quickDictionary',
		download_url = 'https://github.com/hirendrathakur/quickDictionary/tarball/0.12',
		keywords = ['dictionary','quick','search','copy'],
		license = 'MIT',
		scripts = ['bin/quickdictionary'],
		install_requires = ['pyperclip','bs4'],
		classifiers = [],
		)
