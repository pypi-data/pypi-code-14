#!/usr/bin/env python


import simplejson as json


def hex_decode(data):
	"""
	in: data - array of numbers [1,2,33,42,234]
	out: str - '0x1 0x02 0x21 0x2a 0xea'
	"""
	return ''.join(map('0x{:02X} '.format, data))


def handleReturn(ans):
	if len(ans) > 0:
		if len(ans) == 1 and ans[0] == chr(0x00):
			print('No returned packet')
		else:
			print('Returned packet[{}]'.format(len(ans)))
			print('array:', hex_decode(ans))
	else:
		print('No returned packet')


def prettyPrintPacket(ctrl_table):
	"""
	This will pretty print out a servo's registers
	"""
	print('---------------------------------------')
	print("{:.<29} {}".format('id', ctrl_table['id']))
	ctrl_table.pop('id')
	for key, value in ctrl_table.items():
		print("{:.<29} {}".format(key, value))


class JsonFile(object):
	"""
	Simple class to read/write json files.
	"""
	@staticmethod
	def read(fname):
		"""
		Reads a Json file
		in: file name
		out: length of file, dictionary
		"""
		try:
			with open(fname, 'r') as f:
				data = json.load(f)
			return data

		except IOError:
			raise Exception('Could not open {0!s} for reading'.format((fname)))

	@staticmethod
	def write(fname, data):
		"""
		Writes a Json file
		"""
		try:
			with open(fname, 'w') as f:
				json.dump(data, f)

		except IOError:
			raise Exception('Could not open {0!s} for writing'.format((fname)))
