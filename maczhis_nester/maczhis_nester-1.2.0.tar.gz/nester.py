# coding=utf-8
"""
This is a Test models about learning Python3
there is a function about print list
Anthor:maczhis@gmail.com
Time:2016-11-06 18:54
"""


def print_log(item, indent=False, level=0):
    """
        this is test function for python3
        add new point about indent
    """
    for each_item in item:
        if isinstance(each_item, list):
            print_log(each_item, indent, level + 1)
        else:
            if indent:
                for tab_stop in range(level):
                    print("\t", end="")
            print(each_item)
