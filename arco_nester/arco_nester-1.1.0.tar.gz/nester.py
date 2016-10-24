#!/usr/bin/python
#encoding:utf8

"""
@author:Arco Lu
@contact:
@file: nester.py
@time: 08/10/2016 11:16 PM
"""

# cast=["The Holy Grail",1975,"The life of Brain",1979,"The meaning of life",1983,["work","to do","must","shall",[1,2,3,"we are"]]]


def print_lol(the_list,level):
    for each_item in the_list:
        if isinstance(each_item,list):
            print_lol(each_item,level+1)
        else:
            for tab_stop in range(level):
                print ("\t"),
            print(each_item)

# print_lol(cast,0)

"""0代表步长"""

if __name__ == '__print_lol__':
    print_lol()


