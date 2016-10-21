def print_lol(the_list,indent=False,level=0,dist=sys.stdout):
	for item in the_list:
		if isinstance(item,list):
			print_lol(item,indent,level+1,dist)
		else:
			if indent==True:
				for tab_stop in range(level):
					print('\t',end='',file=dist)
			print(item,file=dist)

