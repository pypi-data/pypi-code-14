'''注释1'''
def print_lol(the_list):
        '''注释2'''
        for each_item in the_list:
                if isinstance(each_item,list):
                        print_lol(each_item)
        else:
                print(the_list)
