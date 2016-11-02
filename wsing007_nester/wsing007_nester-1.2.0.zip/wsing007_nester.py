"""递归打印列表"""
def print_lol(the_list,level=0):
#如果item为列表，就递归其中的item。
        for each_item in the_list:
            if isinstance(each_item,list):
                print_lol(each_item,level+1)
            else:
                for tab_stop in range(level):
                    print("\t",end='')
                print(each_item)
