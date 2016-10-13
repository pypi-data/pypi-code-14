"""
I JUST WANT TO MAKE SOME COMMENT
"""
def print_sth(l):
    for i in l:
        if isinstance(i, list):
            print_sth(i)
        else:
            print(i)

