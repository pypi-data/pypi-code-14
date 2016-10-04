#This is the "test3.py" module and it provides one function called print_list()
#which print the lists that may or may not include nested lists.
def print_list(list_name,indent=false,level=0):
	for each_item in list_name:
		if isinstance(each_item,list):
			print_list(each_item,true,level+1)
		else:
                        if indent:
                                for num in range(level):
                                        print("\t",end=' ')
			print(each_item)
