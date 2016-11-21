"""This is nester.py includes a function to print list in list,
    use "for" to repeat"""
def print_lol(the_list,intent=False,level):
    """print the data,every element gets a line"""
        for each_item in the_list:
            if isinstance(each_item,list):
                print_lol(each_item,intent,level+1)
                else:
                    if intent:
                for tab_stop in range(level):
                    print("\t" *level,end='')
                        print(each_item)
