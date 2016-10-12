#coding:utf-8
"""打印嵌套列表-递归"""
def print_lol(the_list):
        for i in the_list:
                if isinstance(i,list):
                        print_lol(i)
                else:
                        print(i)