def print_list(list_name,tab_num):
        for each_item in list_name:
                if isinstance(each_item,list):
                        print_list(each_item,tab_num+1)
                else:
                        for num in range(tab_num):
                                print("\t",end="")
                        print(each_item)
