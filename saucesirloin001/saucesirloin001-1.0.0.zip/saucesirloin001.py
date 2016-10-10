'''this module includes a fuction that is used to print list,and inserted lists are also useful'''

def print_lol(alist):
    for i in alist:
        if (isinstance(i,list)):
            print_lol(i)
        else:
            print i

            
