from setuptools import setup, find_packages

setup(
	name = 'easyscrape',
	version = '0.13',
	packages = find_packages(),
	install_requires=[
		'scrapy',
	],
	entry_points={
		'console_scripts': ['easyscrape=easyscrape.easy_scrape']
	},

	# metadata
	author = 'Wayne Chew',
	author_email = 'xpheal@gmail.com',
	description = 'Easy to use web scraper',
	license = 'GPL',
	url = 'https://github.com/xpheal/DataScience',
)