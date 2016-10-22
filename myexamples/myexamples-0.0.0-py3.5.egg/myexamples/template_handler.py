#!/usr/bin/env python

import pkgutil


def load_content(package, resource):
	return pkgutil.get_data(package, resource)

if __name__ == '__main__':
	content = load_content('myexamples', 'templates/simple.tmpl')
	print(content)
