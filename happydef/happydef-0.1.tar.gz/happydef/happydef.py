#this is a ellefirst.py molucule,offer a print_lol tool,the tool is to print list,one of the list have inside list.
def print_lol(the_list):
#the tool have a location index,called "the_list",this is a python list. so the list can print one the screen,and each data have a unique line
	for each_one in the_list:
		if isinstance(each_one,list):
			print_lol(each_one)
		else:
			print(each_one)



			
