''' This is a module called "recur.py".
It provides one function called printAllArray.'''
def printAllArray(a_list):

    for each_item in a_list:

        if isinstance(each_item,list):
            #Recursion is required here....
            printAllArray(each_item)

        else:

            print(each_item)
                
