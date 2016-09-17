import os

from ._collection import simplify_str
import os as _os

true = True
false = False


def search(name, *path, **option):
    '''Search the given file name in the given path, if path
    is none, will search in C:\\(It will search in the order
    you let it to). If enable list_all, it will return a
    generator containing all result.'''
    from ._collection import compare
    if len(path) == 0:
        path = 'C:\\'
    I, topDown, list_all = false, true, false
    for key, value in option.items():
        if key == 'caseI':
            I = option['caseI']
        elif key == 'topdown':
            topDown = option['topdown']
        elif key == 'list_all':
            list_all = option[list_all]
    for i in path:
        for current_folder, subfolder, subfile in os.walk(i, topdown=topDown):
            for fname in subfile:
                if compare(fname, name, i=I):
                    if list_all:
                        yield _os.path.abspath(os.path.join(current_folder, fname))
                    else:
                        return _os.path.abspath(os.path.join(current_folder, fname))
    return None


def parselist(src: str, caseI=True):
    '''Parse a string into list: '[1,2,3]'>-[1,2,3].
    If their is some problem with the string containing
    the list, it would probably give an incorrect result.'''
    from ._collection import switch_bool

    src = src[1:-1] + ','
    in_quote, reading = false, false
    part = ''
    final = []

    for i in src:
        if in_quote == false and i == ']':
            part += i
            part = (parselist(part))
            reading = false

        elif (in_quote == false and i == '[') or reading == true:
            reading = true
            part += i
            continue
        elif i == '\'':
            try:
                if i[src.index(i) + 1] == ',' or i[src.index(i) - 1] == ',':
                    in_quote = switch_bool(in_quote)
            except IndexError:
                pass

        elif i == ',' and in_quote == false:
            final.append(part)
            part = ''

        elif in_quote:
            part += i

    return final


print(search('a.tXt.txt', caseI=True))
