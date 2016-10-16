"""Reccursive list printer"""

# arg1: a python list[]
# arg2: default is no indenting (optional set True for indenting)
# arg3: default is depth of 0 (Optional set depth to greater value)

def list_printer(input_list, is_indented = False, tab_depth = 0):

    for each_item in input_list:
        if isinstance(each_item, list):
            list_printer(each_item, is_indented, tab_depth + 1)
        else:
            print ('* ', end='')
            if is_indented:
                for each_tab in range(tab_depth):
                    print("\t", end='')
            print(each_item)
