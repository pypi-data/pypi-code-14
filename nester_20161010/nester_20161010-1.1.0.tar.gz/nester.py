# -*- coding:UTF-8 -*-


def print_lol(the_list, indent=False, level=0):

    for item in the_list:
        if isinstance(item, list):
            print_lol(item, indent, level + 1)
        else:
            if indent:
                for tal_stop in range(level):
                    print('\t', end='')
            print(item)


def test(_str):
    if isinstance(_str, str):
        print(_str)
    else:
        print(str(_str))
