''' Creating the test module.'''
''' This function takes a positional argument. Each data item in the provided list
recursively printed to the screen.  A second argument called 'level' is used to insert
tab-stops when a nested list is encountered'''
''' print("\t", end = ' ') is used to obtain tab space on the screen '''

def print_recur(the_list, indent = False, level=0, file= sys.stdout):
    for i in the_list:
        if isinstance(i, list):
            print_recur(i, indent, level+1)
        else:
            if indent:
                for j in range(level):
                    print("\t", end ='', file = fh)  
                print(i, file = fh)        
        
