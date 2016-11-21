'''this is a way to print long_levels_list
    hehe'''
import sys
def print_list(the_list,indent=False,level=0,fh=sys.stdout):
    for each_item in the_list:
        if isinstance(each_item,list):
            print_list(each_item,indent,level+1,fh)
        else:
            if indent:
                for tab_Zstop in range(level):
                    print ('\t',fh)
            print each_item,fh
