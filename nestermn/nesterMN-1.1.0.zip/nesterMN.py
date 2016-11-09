"""This is a python mode for print list"""
"""这是“nesterMN.py”模块，提供了一个名为print_list（）的函数，这个函数
的作用是打印列表，其中有可能包含（也可能不包含）嵌套列表"""


def print_list(the_list,tabNum):
    for eachItem in the_list:
        if isinstance(eachItem,list):
            print_list(eachItem,tabNum+1)
        else:
            for num in range(tabNum):
                print("\t", end='')
            print(eachItem)

