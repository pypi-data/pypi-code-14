def method(arr,flag=False,num=0):
	for a in arr:
		if isinstance(a,list):
			method(a,flag,num+1)
		else:
			if flag:
				for c in range(num):
					print('\t',end='')
			print (a)