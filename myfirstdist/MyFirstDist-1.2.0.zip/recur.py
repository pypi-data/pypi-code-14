''' This is a module called "recur.py".
It provides one function called printAllArray.'''
def printAllArray(a_list,level=0):

    for each_item in a_list:

        if isinstance(each_item,list):
            #Recursion is required here....
            printAllArray(each_item,level+1)

        else:
            for each_tab in range(level):
                print("\t",end='')
            print(each_item)
                
