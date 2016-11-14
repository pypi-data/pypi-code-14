def print_everything (nested_list, level=0):
    for each_item in nested_list:
        if isinstance (each_item, list):
             print_everything (each_item, level+1)  
        else:
            for each_numb in range(level):
                print ("\t", end='')
            print (each_item)
            
                   
            
