import copy
import re

from .shared._coll import NoAssignedValueError
from .shared._coll import cli as _cli
from .file import *


def action(arguments: list):
    if len(arguments) < 2:
        print('''Usage: <name of your original file> <name of your destination file
        without extension> <the file extension of the file you are converting to>
        [next element token, use comma to split] [next line
        token, use comma to split]''')
        raise NoAssignedValueError('No value was passed.')
    argv = copy.copy(arguments)
    argv.split(' ')
    make_decision(argv, len(argv))


def which_type(obj, string: str):
    dotRe = re.compile(r'\.')
    dotRe.sub('', string)
    string = string.lower()
    temp = {'xlsx':            obj.convert_to_xlsx,
            'csv':             obj.convert_to_csv,
            'dat':             obj.convert_to_binary_file,
            'json':            obj.convert_to_json,
            'keywordnotfound': _cli(string)
            }
    return temp.get(string, temp['keywordnotfound'])


def make_decision(option, howmany):
    if howmany == 5:
        with TextFile(option[0], option[1], next_ele_token=option[3], next_line_token=option[4]) as f:
            which_type(f, option[2])()
    elif howmany == 4:
        with TextFile(option[0], option[1], next_ele_token=option[3]) as f:
            which_type(f, option[2])()
    elif howmany == 3:
        with TextFile(option[0], option[1]) as f:
            which_type(f, option[2])()
