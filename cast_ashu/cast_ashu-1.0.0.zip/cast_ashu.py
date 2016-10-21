''' Creating the test module.'''

def print_recur(the_list):
    for i in the_list:
        if isinstance(i, list):
            print_recur(i)
        else:
            print(i)
            
