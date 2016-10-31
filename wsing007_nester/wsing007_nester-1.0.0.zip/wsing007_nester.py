"""递归打印列表"""
def print_lol(the_list):
#如果item为列表，就递归其中的item。
        for each_item in the_list:
            if isinstance(each_item,list):
                print_lol(each_item)
            else:
                print(each_item)
