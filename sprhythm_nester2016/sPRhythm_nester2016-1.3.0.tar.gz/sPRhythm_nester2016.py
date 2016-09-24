"""This is a function used to deal with nested list"""
def print_lol(the_list,indent=False,level=0):
        """This is used to print every data of a list in each line"""
        for each_file in the_list:
                if isinstance (each_file, list):
                        print_lol(each_file,indent,level+1)
                else:
                        if indent:
                                for tab in range(level):
                                        print("\t",end='')
                        print(each_file)
			
