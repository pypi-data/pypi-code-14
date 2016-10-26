#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

from sys import argv
from CryDeer.controller import Controller


def main():
    controller = Controller()
    if len(argv) > 1:
        if argv[1] == "n" or argv[1] == "new":
            if len(argv) == 2:
                print("请输入单号")
            else:
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
        print("//TODO: complete help")

    parser = ArgumentParser(description="Youdao Console Version")
    parser.add_argument('-f', '--full',
                        action="store_true",
                        default=False,
                        help="print full web reference, only the first 3 "
                             "results will be printed without this flag.")
    parser.add_argument('-s', '--simple',
                        action="store_true",
                        default=False,
                        help="only show explainations. "
                             "argument \"-f\" will not take effect.")
    parser.add_argument('-S', '--speech',
                        action="store_true",
                        default=False,
                        help="print URL to speech audio.")
    parser.add_argument('-x', '--selection',
                        action="store_true",
                        default=False,
                        help="show explaination of current selection.")
    parser.add_argument('--color',
                        choices=['always', 'auto', 'never'],
                        default='auto',
                        help="colorize the output. "
                             "Default to 'auto' or can be 'never' or 'always'.")
    parser.add_argument('words',
                        nargs='*',
                        help="words to lookup, or quoted sentences to translate.")

    options = parser.parse_args()

if __name__ == "__main__":
    main()
