#输出一切列表
def print_lol(the_list,level):
	for each_item in the_list:
		if isinstance(each_item,list):
			print_lol(each_item,level+1)
		else:
                        for tab_stop in range(level):
                                print("\t",nd='')
                        print(each_item)

		     

			
