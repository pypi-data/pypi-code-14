'''This is the "nester.py" moudle and it provides one function call print_lol()
   which print lists that may or may not include nester lists
   if you have print tab on every row,set indent use True
   level set how may tabs you want'''
def print_lol(the_list, indent=flase, level=0):
    '''This funciton takes one postitinal argrment call "the list",which
       is any Python list (of - possibly - nested lists). Each data item
       in the provided list is (recursively) print to the screen on it's
       own line.'''
    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item, indent, level+1)
        else:
            if indent:
                for tab_stop in range(level):
                    print('\t', end='') 
            print(each_item)
