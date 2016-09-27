"""This module provides a function to print a list element by element"""
def print_list(i):
	for j in i:
		if(isinstance(j,list)):
			
			print_list(k)
		else:
			print j