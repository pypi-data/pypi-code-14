"""
这是oytm.py模块，提供了print_list函数
print_list函数的作用是递归打印列表项
"""
def print_list (the_list):
    """
    列表中的每个数据项递归的输出到屏幕
    :param the_list:
    :return:
    """
    for item in the_list:
        if(isinstance(item,list)):
            print_list(item)
        else:
            print(item)


