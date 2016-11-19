from distutils.core import setup

def readme():
	with open('README.md') as f:
		return f.read()

setup(
	name = 'getCDFs',
	py_modules = ['getCDFs'],
	version = '1.11',
	description = 'This will check for cdfs on your computer. If they don\'t exist, or there\'s an updated version on the server, it will download from the server. It will then load the cdfs using spacepy.pycdf, and place them into a dictionary.',
	long_description=readme(),
	author = 'Ross Cohen',
	author_email = 'rjc55@njit.edu',
	url = 'https://github.com/BossColo/getCDFs',
	download_url = 'https://github.com/BossColo/getCDFs/tarball/1.6',
	keywords = ['Python', 'spacepy', 'RBSP'],
	license='MIT',
	packages=['getCDFs'],
	install_requires=['spacepy', 'bs4'],
	package_data={'getCDFs': ['*.ini']},
	classifiers = [],
	zip_safe=False
)