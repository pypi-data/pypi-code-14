
"""copyright robin liu 2016
This module is free for you to use"""

def print_lol(the_list, level):
	for each_item in the_list:
		if isinstance(each_item, list):
			print_lol(each_item, level+1)
		else:
			for tab_stop in range(level):
				print("\t", end='')
			print(each_item)
                
