"""I want to try distutils my code"""
from distutils.core import setup

setup(
	name = 'nester_test_001',
	version = '1.0.0',
	py_modules = ['nester'],
	author = 'LYZ',
	author_email = 'Haha',
	url = 'http://www.headfirstlabs.com',
	description = 'A simple printer of nested lists',
)
