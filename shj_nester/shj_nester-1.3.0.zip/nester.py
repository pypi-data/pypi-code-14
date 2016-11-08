"""这是一个遍历列表的函数"""
def print_lol(the_list,indeut=False,level=0):
	for each_item in the_list:
		if isinstance (each_item,list):
			print_lol(each_item,indeut,level+1)
		else:
                        ifindent:
			for tab_stop in range(level):
				print("\t",end='')
			print(each_item)
