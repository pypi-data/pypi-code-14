import os as __os
import sys as __sys

from .shared.__coll import simplify_str as convert_string
from .enum.variable import false, true


def search_file(name, *path, **option):
    """Search the given file name(re pattern) in the given path, if path
    is none, will search in C:\\(It will search in the order
    you let it to). If enable list_all, it will return a
    tuple containing all result."""
    from .shared.__coll import compare
    if len(path) == 0:
        path = 'C:\\'
    ci, topdown, list_all = false, true, false
    size = __sys.maxsize
    for key, value in option.items():  # Get options.
        if key == 'caseI':
            ci = option['caseI']
        elif key == 'topdown':
            topdown = option['topdown']
        elif key == 'list_all':
            list_all = option['list_all']
        elif key == 'size':
            size = option['size']
        else:
            raise KeyError('No such option.')
    temp = []
    for ci in path:
        for current_folder, subfolder, subfile in __os.walk(ci, topdown=topdown):
            for fname in subfile:
                if compare(fname, name, i=ci):
                    if list_all and __os.path.getsize(__os.path.join(current_folder, fname)) / 1024 <= size:
                        temp.append(__os.path.abspath(__os.path.join(current_folder, fname)))
                    elif __os.path.getsize(__os.path.join(current_folder, fname)) / 1024 <= size:
                        return __os.path.abspath(__os.path.join(current_folder, fname))
    if len(temp) > 0:
        return tuple(temp)
    return None


def search_folder(name, *path, **option):
    """Search the given folder name(re pattern) in the given path, if path
    is none, will search in C:\\(It will search in the order
    you let it to). If enable list_all, it will return a
    tuple containing all result."""
    from .shared.__coll import compare
    if len(path) == 0:
        path = 'C:\\'
    ci, topdown, list_all, empty = false, true, false, false
    size = __sys.maxsize
    for key, value in option.items():
        if key == 'caseI':
            ci = option['caseI']
        elif key == 'topdown':
            topdown = option['topdown']
        elif key == 'list_all':
            list_all = option['list_all']
        elif key == 'size':
            size = option['size']
        elif key == 'ignore_empty_folder':
            empty = option['ignore_empty_folder']
        else:
            raise KeyError('No such option.')
    temp = []
    for ci in path:
        for current_folder, subfolder, subfile in __os.walk(ci, topdown=topdown):
            for fname in subfolder:
                if compare(fname, name, i=ci):
                    if empty == false:
                        if list_all and __os.path.getsize(__os.path.join(current_folder, fname)) / 1024 <= size:
                            temp.append(__os.path.abspath(__os.path.join(current_folder, fname)))
                        elif __os.path.getsize(__os.path.join(current_folder, fname)) / 1024 <= size:
                            return __os.path.abspath(__os.path.join(current_folder, fname))
                    else:
                        if __os.listdir(__os.path.join(current_folder, fname)) == '':
                            continue
                        if list_all and __os.path.getsize(__os.path.join(current_folder, fname)) / 1024 <= size:
                            temp.append(__os.path.abspath(__os.path.join(current_folder, fname)))
                        elif __os.path.getsize(__os.path.join(current_folder, fname)) / 1024 <= size:
                            return __os.path.abspath(__os.path.join(current_folder, fname))
    if len(temp) > 0:
        return tuple(temp)
    return None


def parselist(string: str, caseI=False, file=False):
    """Parse a string into list: '[1,2,3]'>-[1,2,3].
    If their is some problem with the string containing
    the list, it would probably give an incorrect result."""
    if file:
        from .shared.__coll import random_word
        import importlib
        temp="tempList"+random_word(4,True)
        with open(temp+".py",'w')as f:
            print("templ=", string, file=f)
        try:
            mod=importlib.import_module(temp)
        except SyntaxError:
            raise SyntaxError("Something is wrong with the list you are using.")
        else:
            temp1=mod.templ
            __os.unlink(temp+'.py')
            return temp1

    from .shared.__coll import switch_bool

    string = string[1:-1] + ','
    in_quote, reading = false, false
    part = ''
    final = []

    for i in string:  # Loop through the string to extract information.
        if in_quote == false and i == ']':
            part += i
            part = (parselist(part))#Call itself again to handle that list
            reading = false

        elif (in_quote == false and i == '[') or reading == true:
            reading = true
            part += i
            continue
        elif i == "'"or i=='"':
            try:
                if i[string.index(i) + 1] == ',' or i[string.index(i) - 1] == ',':
                    in_quote = switch_bool(in_quote)
            except IndexError:
                pass

        elif i == ',' and in_quote == false:
            final.append(part)
            part = ''

        elif in_quote:
            part += i
        else:
            part = convert_string(i, casei=caseI).simplify()

    return final
