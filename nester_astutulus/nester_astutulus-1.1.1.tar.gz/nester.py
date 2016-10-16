"""Reccursive list printer"""
def list_printer(input_list):
    for each_item in input_list:
        if isinstance(each_item, list):
            list_printer(each_item)
        else:
            print(each_item)


def indented_list_printer(input_list, tab_depth):
    for each_item in input_list:
        if isinstance(each_item, list):
            indented_list_printer(each_item, tab_depth+1)
        else:
            print ('*', end='')
            for each_tab in range(tab_depth):
                print("\t", end='')
            print(each_item)
