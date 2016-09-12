 #This is the “nester.py" module
def print_lol(the_list,indent=False,level=0):
        if not indent:
                level=0
        	#This function takes a positional argument called “the_list", which is any
#Python list (of, possibly, nested lists). Each data item in the provided list
#is (recursively) printed to the screen on its own line.
        for each_item in the_list:
                if isinstance(each_item, list):
                        print_lol(each_item, indent, level+1)
                else:
                        for tab_stop in range(0,level):
                                print("\t",end='')
                        print(each_item)

#this function will return boolean values of a given raw(string) input
def change_to_bool(a):
        if a in ['True','t','T','yes','y']:
                return True
        if a in ['False','n','N','F','no']:
                return False
