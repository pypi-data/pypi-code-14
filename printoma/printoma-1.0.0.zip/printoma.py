def print_everything (nested_list):
    for each_item in nested_list:
        if isinstance (each_item, list):
             print_everything (each_item)  
        else:
            print (each_item)
            
                   
            
