import sys

''' This is a module called "recur.py".
It provides one function called printAllArray.'''
def printAllArray(a_list,indent=False,level=0,fh=sys.stdout):

    for each_item in a_list:

        if isinstance(each_item,list):
            #Recursion is required here....
            printAllArray(each_item,indent,level+1,fh)

        else:
            if indent:
                for each_tab in range(level):
                    print("\t",end='',file=fh)
            print(each_item,file=fh)
                
