""" This is my hello world.  It prints a every item in a list if passed a list"""
def print_lol(the_list, level=0):
    """ It iterates through a list of lists and recursively calls it self until all items are printed"""
    for x in (the_list):
        if isinstance(x, list):
            print_lol(x, level+1)
        else:
            for tab_stop in range(level):
                print("\t", end=' ')
            print(x)
                        

