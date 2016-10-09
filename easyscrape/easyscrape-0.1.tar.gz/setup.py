from setuptools import setup

setup(
	name='easyscrape',
	version='0.1',
	py_modules=['easyscrape'],
	install_requires=[],
	entry_points={
		'console_scripts': ['easyscrape=easyscrape.easyscrape:test']
	}
)