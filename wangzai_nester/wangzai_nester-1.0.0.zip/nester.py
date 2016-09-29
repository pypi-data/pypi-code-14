def print_lol(the_list):
    for each_item in the_list:
        if isinstance(each_item,list):
            print_lol(each_item)
        else:
            print(each_item)
moives=["holly","shit",["are","you","crazy?",["yes I do"]],"just kidding!"]
