""" This is the “nester.py" module, and it provides one 
function called print_lol() which prints lists that may 
or may not include nested lists """


def print_lol(the_list, space_number):
	
	""" This function takes a positional argument called “the_list", 
	which is any Python list (of, possibly, nested lists). Each data 
	item in the provided list is (recursively) printed to the screen 
	on its own line """
	
	for each_item in the_list:
		if isinstance(each_item, list):
			print_lol(each_item, space_number+1)
		else:
			for i in range(space_number):
				print("\t", end='')
			print(each_item)
			
			
list1 = [3, 4, 5,[3,4]]
print_lol(list1, 0)
