'''this is a way to print long_levels_list
    hehe'''
def print_list(the_list):
    for each_item in the_list:
        if isinstance(each_item,list):
            print_list(each_item)
        else:
            print each_item