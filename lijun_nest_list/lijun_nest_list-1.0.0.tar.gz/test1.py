
"""
这个模块主要是提供了一个打印嵌套列表的函数
__author__ = 'lijun'

"""

def print_lol(the_list):
    """

    :param the_list:
    :return:
    这是打印嵌套列表的函数
    """
    for each in the_list:
        if isinstance(each,list):
            print_lol(each)
        else:
            print(each)
