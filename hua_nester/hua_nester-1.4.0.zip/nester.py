ccc=[11]
def print_lol(ccc,indent=False,level=0):
    for x in ccc:
       if isinstance(x,list):
          print_lol(x,indent,level)
       else:
           if indent:
            for tab_stop in range(level):
                print("\t",end="")
            
           print(x)
    
 
