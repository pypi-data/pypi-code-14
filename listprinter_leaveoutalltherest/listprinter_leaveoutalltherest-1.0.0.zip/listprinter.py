"""
comment 1
"""
def printList(L):
    """
    :param L:
    :return:
    """
    for x in L:
        if isinstance(x,list):
            printList(x)
        else:
            print(x)


