"""
这是oytm.py模块，提供了print_list函数
print_list函数的作用是递归打印列表项
"""
def print_list (the_list,indent=False,level=0):
    """
    打印列表项,可选择是否缩进，以及缩进行数
    :param the_list:
    :param indent:
    :param level:
    :return:
    """
    for item in the_list:
        if(isinstance(item,list)):
            print_list(item,indent,level+1)
        else:
            if indent:
                for level_num in range(level):
                    print("\t",end='')
            print(item)


