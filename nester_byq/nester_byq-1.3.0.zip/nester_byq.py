'''
这是nester.py模块，里面包含 print_lol 函数，
这个函数的作用是打印列表，其中有可能含有嵌套列表
'''
''' 版本1.0.0
def print_lol(the_list):
	for each_tv in the_list:
		if isinstance(each_tv,list):
			print_lol(each_tv)
		else:
			print(each_tv)

tvshow = ["langyabang",2015,43,["huge",["liutao","wangkai","feiliu"]]]
print_lol(tvshow)
'''

'''# 版本1.1.0
def print_lol(the_list,level=0):
	for each_item in the_list:
		if isinstance(each_item,list):
			print_lol(each_item,level+1)
		else:
			for tab_stop in range(level):
				print("\t",end='')
			print(each_item)

cast = ["hangzhou","shanghai","wuhan",["xiamen","hainan",["haikou","sanya"]]]
print_lol(cast,0)
'''
def print_lol(the_list,indent=False,level=0):
	for each_item in the_list:
		if isinstance(each_item,list):
			print_lol(each_item,indent,level+1)
		else:
			if indent:
				for tab_stop in range(level):
					print("\t",end='')
			print(each_item)

cast = ["hangzhou","shanghai","wuhan",["xiamen","hainan",["haikou","sanya"]]]
print_lol(cast)