#!/usr/bin/env python

# Project skeleton maintained at https://github.com/jaraco/skeleton

import io
import sys

import setuptools

with io.open('README.rst', encoding='utf-8') as readme:
	long_description = readme.read()

needs_pytest = {'pytest', 'test'}.intersection(sys.argv)
pytest_runner = ['pytest_runner'] if needs_pytest else []
needs_sphinx = {'release', 'build_sphinx', 'upload_docs'}.intersection(sys.argv)
sphinx = ['sphinx', 'rst.linker'] if needs_sphinx else []
needs_wheel = {'release', 'bdist_wheel'}.intersection(sys.argv)
wheel = ['wheel'] if needs_wheel else []

name = 'pmxbot'
description = 'IRC bot - full featured, yet extensible and customizable'

setup_params = dict(
	name=name,
	use_scm_version=True,
	author="YouGov, Plc.",
	author_email="dev@yougov.com",
	maintainer="Jason R. Coombs",
	maintainer_email="jaraco@jaraco.com",
	description=description or name,
	long_description=long_description,
	url="https://github.com/yougov/" + name,
	packages=setuptools.find_packages(),
	include_package_data=True,
	namespace_packages=name.split('.')[:-1],
	install_requires=[
		"irc>=15.0,<16dev",
		"requests",
		"pyyaml",
		"feedparser",
		"pytz",
		"beautifulsoup4",
		"jaraco.compat>=1.0.3",
		"backports.method_request",
		"wordnik-py3",
		"more_itertools",
		"jaraco.timing",
		"tempora",
		"jaraco.collections>=1.5",
		"jaraco.itertools",
		"jaraco.context",
		"jaraco.classes",
		"jaraco.functools",
		"inflect",

		# for viewer
		"cherrypy>=3.2.3",
		"jinja2",
	],
	extras_require={
	},
	setup_requires=[
		'setuptools_scm>=1.9',
	] + pytest_runner + sphinx + wheel,
	tests_require=[
		'pytest>=2.8',
		'pymongo>=3',
		'jaraco.test>=2.0.4',
		'more_itertools',
	],
	classifiers=[
		"Development Status :: 5 - Production/Stable",
		"License :: OSI Approved :: MIT License",
		"Programming Language :: Python :: 3",
		"Topic :: Communications :: Chat :: Internet Relay Chat",
		"Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
	],
	entry_points={
		'console_scripts': [
			'pmxbot=pmxbot.core:run',
			'pmxbotweb=pmxbot.web.viewer:run',
		],
		'pmxbot_handlers': [
			'pmxbot logging = pmxbot.logging:Logger.initialize',
			'pmxbot karma = pmxbot.karma:Karma.initialize',
			'pmxbot quotes = pmxbot.quotes:Quotes.initialize',
			'pmxbot core commands = pmxbot.commands',
			'pmxbot notifier = pmxbot.notify:Notify.init',
			'pmxbot rolls = pmxbot.rolls:ParticipantLogger.initialize',
			'pmxbot config = pmxbot.config_',
			'pmxbot system commands = pmxbot.system',
			'pmxbot say something = pmxbot.saysomething:FastSayer.init_in_thread',
		],
	},
)
if __name__ == '__main__':
	setuptools.setup(**setup_params)
