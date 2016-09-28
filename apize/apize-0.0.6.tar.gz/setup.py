from setuptools import setup

setup(name='apize',
	version = '0.0.6',
	author = 'herrersystem',
	author_email = 'anton.millescamps@evhunter.fr',
	
	url = "http://github.com/herrersystem/apize",
	keywords = 'apize',
	description = 'Write API client (quickly and simply)',
	license = 'MIT',
	packages = ['apize'],
	install_requires = ['requests'],
	
	classifiers=[
		'Development Status :: 4 - Beta',
		'License :: OSI Approved :: MIT License',
		'Programming Language :: Python :: 3',
		'Programming Language :: Python :: 3.4',
		'Programming Language :: Python :: 3.5',
	],
)
