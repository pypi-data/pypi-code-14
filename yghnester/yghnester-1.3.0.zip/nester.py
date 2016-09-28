def print_lol(the_list,indent=False,level=0):
	for each_item in the_list:
		if isinstance(each_item,list):
			print_lol(each_item,indent,level+1)
		else:
                        if indent:
                                for tab_stop in range(level):
                                        print"\t",
			print(each_item)

'''
def print_lol(the_list,level=0):
	for each_item in the_list:
		if isinstance(each_item,list):
			print_lol(each_item,level+1)
		else:
			for tab_stop in range(level):
				print"\t",
			print(each_item)
'''



"""This is the 'nester.py' module and it provides one function called print_lol() which prints lists that may or may not include nested lists."""
'''
def print_lol(the_list):
	for each_item in the_list:
		if isinstance(each_item,list):
			print_lol(each_item)
		else:
			print(each_item)
'''
