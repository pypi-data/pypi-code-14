
from log import logger as logging

GREEN='\033[1;32;40m'
RED='\033[1;31;40m'
END='\033[0m'

def text_green(s):
    return "{}{}{}".format(GREEN,s,END)

def text_red(s):
    return '{}{}{}'.format(RED,s,END)

def print_success():
    s = text_green("cloudmanager  update success!!!")
    print(s)

def print_fail():
    s = text_red("cloudmanager  update fail!!!")
    print(s)

if __name__ == '__main__':
    print_success()
    print_fail()
