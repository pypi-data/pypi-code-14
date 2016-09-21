
def print_lol(the_list, index = False, level=0):
	for each in the_list:
		if isinstance(each, list):
			print_lol(each, index, level + 1)
		else:
			if index:
	
				for tab_stop in range(level):
				print('\t', end = '')
			print(each)
