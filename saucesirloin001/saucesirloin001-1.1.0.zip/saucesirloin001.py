'''this module includes a fuction that is used to print list,and inserted lists are also useful'''

def print_lol(alist,level):
    for i in alist:
        if (isinstance(i,list)):
            print_lol(i,level+1)
        else:
            for j in range(level):
                print(" ")
            print i

            
