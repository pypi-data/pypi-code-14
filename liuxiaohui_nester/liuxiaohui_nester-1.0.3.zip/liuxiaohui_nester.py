#coding=utf-8
'''
这是pester.py模块，提供了一个名为print_lol()的函数
用来打印列表，其中包含或不包含嵌套列表。并且会以缩
进的方式进行打印。增加参数indent决定是否使用缩进功
能，默认为关闭缩进。'''
def print_lol(the_list,indent=False,level=0):
    for each_item in the_list:
        if isinstance(each_item,list):
            print_lol(each_item,indent,level+1)
        else:
            if indent:
                for tab_stop in range(level):
                    print('\t',end='')
            print(each_item)

if __name__ == '__main__':
    testlist=['John','Eric','Lee',['Cleese','Idle','Basic',['Palin','Jeson','Leader']]]
    print_lol(testlist,True)