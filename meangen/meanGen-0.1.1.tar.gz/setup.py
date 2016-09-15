import re
from setuptools import setup, find_packages

with open("README.rst", "rb") as f:
	long_descr = f.read().decode("utf-8")

setup(
	name = "meanGen",
	packages = find_packages(),
	package_data={'': ['*.html', '*.css', '*.js', '*.json']},
	entry_points = {
 			"console_scripts": ["meanGen = src.meanGen:main"]
		},
	version = "0.1.1",
	description = "",
	long_description = long_descr,
	author = "Oscar Vazquez",
	author_email = "ovazquez@codingdojo.com",
	url = "https://github.com/oscarvazquez/angularSkeleton"
)