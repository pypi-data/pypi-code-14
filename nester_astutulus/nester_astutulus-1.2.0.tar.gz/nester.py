"""Reccursive list printer"""

# Optional argument; default value is zero.
def list_printer(input_list, tab_depth = 0):

    for each_item in input_list:
        if isinstance(each_item, list):
            list_printer(each_item, tab_depth * 2)
        else:
            print ('*', end='')
            for each_tab in range(tab_depth):
                print("\t", end='')
            print(each_item)
