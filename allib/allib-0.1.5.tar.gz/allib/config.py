from __future__ import absolute_import
import copy
try:
	import configparser
except ImportError:
	import ConfigParser as configparser


class ConfigError(Exception):
	pass


def configparser_to_dict(config, defaults=None, types=None):
	'''
	Transform a configparser object into a dictionary.
	'''
	confdict = copy.deepcopy(defaults) if defaults else {}

	for section in config.sections():
		confdict[section] = {}
		for item, value in config.items(section):
			valid_type = None
			if types and section in types and item in types[section]:
				valid_type = types[section][item]

			value_l = value.lower()
			if value_l == 'false':
				value = False
			elif value_l == 'true':
				value = True
			elif value_l == 'null' or value_l == 'none':
				value = None
			elif valid_type is int or valid_type is float:
				try:
					value = valid_type(value)
				except ValueError:
					pass

			if valid_type is list:
				value = [v.strip() for v in str(value).split(',')]
			elif valid_type is dict:
				pairs = [v.strip().split(':') for v in str(value).split(',')]
				value = {}
				for key, value in pairs:
					value[key.strip()] = value.strip()
			elif valid_type is str and isinstance(value, unicode):
				valid_type = unicode

			if valid_type is not None and not isinstance(value, valid_type):
				msg = 'Invalid configuration value for {}:{} - expected {}, got {}'.format(
					section, item, valid_type, type(value))
				raise ConfigError(msg)

			confdict[section][item] = value

	return confdict


def get_config(args, default_location, defaults=None, types=None):
	'''
	args: An object returned from argparse.ArgumentParser.parse_args()
	default_location: Path to config file if not specified in `args`
	defaults: Either a dictionary of default configuration values, or a function
	  that will be invoked as `defaults(config, args)` after the initial
	  dictionary has been constructed.
	types: A dictionary of types to validate the config against.
	'''
	path = args.config or default_location
	config = configparser.ConfigParser()
	files = config.read(path)
	if not files:
		msg = 'Could not find a config file at path %r' % path
		if not args.config:
			msg += '. Specify one with the -c/--config command line option.'
		raise ConfigError(msg)

	confdict = configparser_to_dict(
		config,
		defaults if isinstance(defaults, dict) else None,
		types,
	)

	if 'logging' not in confdict:
		confdict['logging'] = {}
	if 'log_level' in args and args.log_level:
		confdict['logging']['level'] = args.log_level
	if 'log_file' in args and args.log_file:
		confdict['logging']['file'] = args.log_file

	if callable(defaults):
		defaults(confdict, args)

	return confdict
