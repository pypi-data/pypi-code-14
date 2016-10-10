#this function prints elements of a nested or normal list
"""This function takes in a list as input"""
def print_me(alist,level=0):
    for i in alist:
        if isinstance(i, list):
            # This is where yhe recursion occurs

                print_me(i,level+1)
        else:
            for i2 in range(level):
                print("\t",end="")
            print(i)



