#coding=utf-8
'''
这是pester.py模块，提供了一个名为print_lol()的函数
用来打印列表，其中包含或不包含嵌套列表。并且会以缩
进的方式进行打印。'''
def print_lol(the_list,level=0):
    for each_item in the_list:
        if isinstance(each_item,list):
            print_lol(each_item,level+1)
        else:
            for tab_stop in range(level):
                print('\t',end='')
            print(each_item)

if __name__ == '__main__':
    testlist=[1,2,3,[4,5,6,[7,8,9]]]
    print_lol(testlist)