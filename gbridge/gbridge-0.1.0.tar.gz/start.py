#!/usr/bin/env python
import sys
import argparse


def parse_config(str):

	def parse_token(line):
		if '{' in line:
			return ('start',)
		elif '}' in line:
			return ('end',)
		elif '=' in line:
			parts = line.split('=', 2)
			return ('pair', parts[0], parts[1])
		else:
			return ('ignore',)

	configs = []
	current_conf = None

	lines = str.replace('\t', '').split('\n')

	for line in lines:
		token = parse_token(line)
		if token[0] == 'start':
			current_conf = {}
		elif token[0] == 'end':
			configs.append(current_conf)
		elif token[0] == 'pair':
			current_conf[token[1]] = token[2]

	return configs


def find_ip_by_name(configs, name):
	for conf in configs:
		if name in conf['name']:
			return conf['ip_address']

	return ''


def print_all_interfaces(configs):
	for conf in configs:
		print '{0}: {1}'.format(conf['name'], conf['ip_address'])


def notify_error(err):
	sys.stderr.write('{0}\n'.format(err))
	sys.exit(1)


def main():
	parser = argparse.ArgumentParser(prog='gbridge')

	parser.add_argument('interface', default='', nargs='?', help='interface name (or substring of it)')
	parser.add_argument('-a', '--all', help='show all interfaces', action='store_true')

	args = parser.parse_args()

	if not args.all and args.interface == '':
		notify_error('must specify interace name, see help [-h]')

	try:
		with open('/private/var/db/dhcpd_leases', 'rb') as f:
			raw_interface_config = f.read()
	except:
		notify_error('unable to read macos bridge leases file (/private/var/db/dhcpd_leases)')

	try:
		all_interfaces = parse_config(raw_interface_config)
	except:
		notify_error('unable to parse macos bridge leases file')

	if args.all:
		print_all_interfaces(all_interfaces)
	else:
		print find_ip_by_name(all_interfaces, args.interface)


if __name__ == '__main__':
	main()
