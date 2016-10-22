"""This is nester.py """
def print_lol(the_list,level):
	"""some comment"""
	for each_item in the_list:
		if isinstance(each_item,list):
			print_lol(the_list,level++)
		else:
			for tab_stop in range(level):
				print("\t",end='')
			print(each_item),