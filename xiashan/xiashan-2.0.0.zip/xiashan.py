# -*- coding:utf-8 -*-
def print_lol(the_list,indent = False,leve = 0):
    for each_item in the_list:
        if isinstance(each_item,list):
            print_lol(each_item,indent,leve+1)
        else:
            if indent:
                for tab_stop in range(leve):
                    print "\t",
                    print ''
            print each_item
