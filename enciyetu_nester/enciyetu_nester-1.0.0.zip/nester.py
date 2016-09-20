"""this is the 'nest.py' module and it provide a function called printlist().
the function can print lists that may or may not include the nested lists. 
"""
def printlist(currlist, level = 0):
    for each_item in currlist:
        if isinstance(each_item, list):
            printlist(each_item, level + 1)
        else:
            for i in range(level):
                print("   ", end = "")
            print(each_item)
