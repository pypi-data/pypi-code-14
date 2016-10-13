#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

from sys import argv
from .controller import Controller


def main():
    controller = Controller()
    if len(argv) > 1:
        if argv[1] == "n" or argv[1] == "new":
            if len(argv) >= 4:
                controller.new_item(argv[2], argv[3])
            else:
                controller.new_item(argv[2])
        elif argv[1] == "l" or argv[1] == "list":
            if len(argv) == 3:
                controller.show_info(argv[2])
            else:
                controller.list()
        elif argv[1] == "u" or argv[1] == "update":
            controller.update_all()
        elif argv[1] == "d" or argv[1] == "delete":
            if len(argv) == 3:
                controller.delete_item(argv[2])
            else:
                print("命令错误")
        else:
            print("命令错误")
    else:
        print("233")

if __name__ == "__main__":
    main()
