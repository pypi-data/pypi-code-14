from datetime import datetime
import re


class ParseException(Exception):
	pass


class ParameterNotFoundException(Exception):
	pass


class GroupNotFoundException(Exception):
	pass


class LandsatMetadataParser:
	GROUP_START = "GROUP = "
	GROUP_END = "END_GROUP = "
	ASSIGN_CHAR = " = "
	FILE_END = "END"

	def __init__(self):
		self._groups = {}

	def read(self, filename):
		with open(filename, mode='rU') as handle:
			self._read(handle)

	def _read(self, handle):
		currentgroup = []
		lineno = 0
		while True:
			line = handle.readline()
			lineno += 1

			if not line:
				break

			line = line.strip()

			if line == '':
				continue

			if line.startswith(LandsatMetadataParser.GROUP_START):
				groupname = line.split(LandsatMetadataParser.GROUP_START)[-1]
				self._newgroup(currentgroup, groupname)
				currentgroup.append(groupname)
			elif line.startswith(LandsatMetadataParser.GROUP_END):
				groupname = line.split(LandsatMetadataParser.GROUP_END)[-1]
				if groupname == currentgroup[-1]:  # valid end group
					currentgroup.pop()
				else:
					raise ParseException("Invalid group end at line %s." % lineno)
			elif LandsatMetadataParser.ASSIGN_CHAR in line:  # key, value assignment
				if len(currentgroup) > 0:
					key, value = line.split(LandsatMetadataParser.ASSIGN_CHAR, 1)
					self._new_parameter(currentgroup, key, value)
				else:
					raise ParseException("Can't assign parameters outside group at line %s." % lineno)
			elif line == LandsatMetadataParser.FILE_END:
				if len(currentgroup) > 0:
					raise ParseException("Invalid END at line %s: not all groups were closed." % lineno)
				break

	def get(self, group, parameter):
		group = self._get_group(group)
		if not parameter in group:
			raise ParameterNotFoundException("Parameter %s not set." % parameter)
		return group[parameter]

	def getstring(self, group, parameter):
		value = self.get(group, parameter)
		if value.startswith('"') and value[0] == value[-1]:
			return value[1:-1]
		raise TypeError("%s is not a string." % parameter)

	def getint(self, group, parameter):
		value = self.get(group, parameter)
		if re.match(r"^-?\d+$", value):
			return int(value)
		raise TypeError("%s is not an int." % parameter)

	def getfloat(self, group, parameter):
		value = self.get(group, parameter)
		if re.match(r"^\-?\d+\.\d+(E[+-]?\d\d+)?$", value):
			return float(value)
		raise TypeError("%s is not a float." % parameter)

	def getdate(self, group, parameter):
		value = self.get(group, parameter)
		if re.match(r"^\d{4}(-\d{2}){2}$", value):
			return datetime.strptime(value, "%Y-%m-%d").date()
		raise TypeError("%s is not a date." % parameter)

	def getdatetime(self, group, parameter):
		value = self.get(group, parameter)
		if re.match(r"^\d{4}(-\d{2}){2}T\d{2}(:\d{2}){2}Z$", value):
			return datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ")
		raise TypeError("%s is not a datetime." % parameter)

	def items(self, group):
		group = self._get_group(group)
		return [(a, group[a]) for a in group if not type(group[a]) == dict]

	def _new_parameter(self, currentgroup, key, value):
		group = self._get_group(currentgroup)
		if key in group:
			raise ParseException("Parameter %s already defined." % key)
		group[key] = value

	def _newgroup(self, currentgroup, groupname):
		group = self._get_group(currentgroup)
		if groupname in group:
			raise ParseException("Group %s already defined." % groupname)
		group[groupname] = {}

	def _get_group(self, currentgroup):
		if not type(currentgroup) == list:
			raise TypeError("Group is not a list.")
		group = self._groups
		for g in currentgroup:
			if g not in group:
				raise GroupNotFoundException("Group %s not defined." % g)
			if type(group[g]) != dict:
				raise Exception("Group %s defined as parameter." % g)
			group = group[g]
		return group
