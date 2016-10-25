'''print all the element of list'''

def printList(the_lol):
    for ele in the_lol:
        if isinstance(ele,list):
            printList(ele)
        else:
            print(ele)

