"""
这是oytm.py模块，提供了print_list函数
print_list函数的作用是递归打印列表项
"""
def print_list (the_list,level):
    """
    打印列表项(带缩进)
    :param the_list:
    :param level:
    :return:
    """
    for item in the_list:
        if(isinstance(item,list)):
            print_list(item,level+1)
        else:
            for level_num in range(level):
                print("\t",end='')
            print(item)


