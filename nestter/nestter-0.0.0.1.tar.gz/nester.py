
"""copyright robin liu 2016
This module is free for you to use"""

def print_lol(the_list):
        """iterate a list and recusively drill into child-list"""
        for each_item in the_list:
                if isinstance(each_item, list):
                        print_lol(each_item)
                else:
                        print(each_item)
                
