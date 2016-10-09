#!/usr/bin/python
#encoding:utf8

"""
@author:Arco Lu
@contact:
@file: nester.py
@time: 08/10/2016 11:16 PM
"""

def print_lol(the_list):
    for each_item in the_list:
        if isinstance(each_item,list):
            print_lol(each_item)
        else:
            print(each_item)

# print_lol(the_list)

if __name__ == '__print_lol__':
    print_lol()
