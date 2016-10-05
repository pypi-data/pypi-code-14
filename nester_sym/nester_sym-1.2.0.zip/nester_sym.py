# coding = utf-8
"""
这是"nester.py"模块，提供了一个名为print_lol()的函数，这个函数的作用是遍历list,其中
可能包含嵌套列表
"""


def print_lol(the_list, indent=False, level=0):
    for each_item in the_list:
        if isinstance(each_item, list):  # 如果有嵌套list，则调用自己
            print_lol(each_item, indent, level + 1)
        else:
            if indent:
                print("\t" * level, end='')
            print(each_item)
