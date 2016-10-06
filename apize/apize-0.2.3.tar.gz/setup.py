from setuptools import setup


setup(
	name = 'apize',
	version = '0.2.3',
	author = 'herrersystem',
	author_email = 'anton.millescamps@evhunter.fr',
	url = 'http://github.com/herrersystem/apize',
	keywords = 'apize api client',
	description = 'Write quickly and easily to API clients',
	license = 'GNU General Public License (GPL)',
	packages = ['apize'],
	install_requires = ['requests'],
	
	classifiers=[
		'Development Status :: 5 - Production/Stable',
		'Intended Audience :: Developers',
		'License :: OSI Approved :: GNU General Public License (GPL)',
		'Topic :: Software Development',
		'Topic :: Software Development :: Libraries', 
		'Programming Language :: Python',
		'Programming Language :: Python :: 3',
		'Programming Language :: Python :: 3.4',
		'Programming Language :: Python :: 3.5',
	],
)
