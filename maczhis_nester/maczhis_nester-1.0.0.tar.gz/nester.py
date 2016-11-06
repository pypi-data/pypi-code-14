# coding=utf-8
"""
This is a Test models about learning Python3
there is a function about print list
Anthor:maczhis@gmail.com
Time:2016-11-06 16:54
"""
def print_log(item):
    """
        this is test function for python3
    """
    for each_item in item:
        if isinstance(each_item, list):
            print_log(each_item)
        else:
            print(each_item)
