'''this is a way to print long_levels_list
    hehe'''
def print_list(the_list,indent=False,level=0):
    for each_item in the_list:
        if isinstance(each_item,list):
            print_list(each_item,indent,level+1)
        else:
            if indent:
                for tab_Zstop in range(level):
                    print ('\t')
            print each_item
