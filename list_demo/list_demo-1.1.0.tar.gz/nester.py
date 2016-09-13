'''This is the "nester.py" moudle and it provides one function call print_lol()
   which print lists that may or may not include nester lists'''
def print_lol(the_list, level):
    '''This funciton takes one postitinal argrment call "the list",which
       is any Python list (of - possibly - nested lists). Each data item
       in the provided list is (recursively) print to the screen on it's
       own line.'''
    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item, level+1)
        else:
            for tab_stop in range(level):
                print('\t', end='') 
            print(each_item)
