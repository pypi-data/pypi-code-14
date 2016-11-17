def print_list(list_name,add_tab=False,tab_num=0):
        for each_item in list_name:
                if isinstance(each_item,list):
                        print_list(each_item,add_tab,tab_num+1)
                else:
                        if add_tab:
                                for num in range(tab_num):
                                        print("\t",end="")
                        print(each_item)
