""" This module is written to output the data objects of a list. """
def print_lol(the_list):
        # This function print_lol accepts a list as an argument & displays all its data objects on screen.
	for all_items in the_list:
		if isinstance(all_items, list):
			print_lol(all_items)
		else:
			print(all_items)
