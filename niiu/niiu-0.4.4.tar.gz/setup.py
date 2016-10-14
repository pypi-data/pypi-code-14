from distutils.core import setup
from setuptools import find_packages

VERSION = '0.4.4'

setup(
	name = "niiu",
	packages = find_packages(),
	version = VERSION,
        classifiers = [
                "Programming Language :: Python",
            ],
	entry_points = {
		"console_scripts": [
			"niiu = niiu.niiu:main",
		],
	}
)
