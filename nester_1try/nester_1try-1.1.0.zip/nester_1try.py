"""This is the "nester.py" module and it provides one function called print_lol()
   which prints lists that may or may not include nested lists."""

from __future__ import print_function
def print_lol(the_list, indent = False, level = 0, fd = sys.stdout):
	""" Prints a list of (possibly) nested lists.
	
	This function takes a positional argument called "the_list", which 
	is any Python list (of - possibly - nested lists). Each data item in the
	provided list is (recursively) printed to the screen or other position on it's own line.
	A second argument called "indent" controls whether or not indentation is
	shown on the display. This defaults to False: set it to True to switch on.
	A third argument called "level" (which defaults to 0) is used to insert
	tab-stops when a nested list is encountered.
	A forth argument called "fd" (which defaults to sys.stdout) controls the output position """
	
for each_item in the_list:
	if isinstance(each_item, list):
		print_lol(each_item, indent, level + 1, fd)
	else:
		if indent:
			for tab_stop in range(level):
				print("\t", end = '', file = fd)
		print(each_item, file = fd)
	