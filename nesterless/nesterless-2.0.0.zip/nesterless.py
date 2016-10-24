"""这是zc_nester.py模块，提供了一个print_lol()的函数，
用来打印列表，可以根据自己需要对嵌套列表进行缩进"""
def print_lol(the_list,indent=False,level=0):
        """这个函数有个位置参数，the_list，可以是任何朋友Python列表，
列表各个项会递归的打印到屏幕上，各占一行；indent可选参数控制缩进，Fasle
默认嵌套列表不缩进；level可选参数提供固定迭代次数方法，实现不同层级的缩进"""
	for each_item in the_list:
		if isinstance(each_item,list):
			print_lol(each_item,indent,level+1)
		else:
			if indent:
				for tab_stop in range(level):
					print('\t',end='')
			print(each_item)
