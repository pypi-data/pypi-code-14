from distutils.core import setup
from setuptools import find_packages

VERSION = '0.7.7'

setup(
	name = "niiu",
	packages = find_packages(),
	version = VERSION,
	entry_points = {
		"console_scripts": [
			"niiu.py = niiu.niiu:main",
		],
	}
)
