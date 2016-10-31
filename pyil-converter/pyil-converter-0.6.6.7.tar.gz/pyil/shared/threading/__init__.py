from pyil.enum.modifiable import divide as _div
from pyil.enum.variable import auto_process


def pmap(func, iterable, process=auto_process) -> iter:
    """Returns a PMap object. The usage is similar to the
    map function and does the same work except that this
    one is multi-threaded."""
    from .thread import IsoThread as itd
    if str(type(process)) == "class <'function'>":
        process = process(len(iterable))
        iterable = _div(iterable, process)
    else:
        iterable = _div(iterable, process)
    temp2 = 0

    def temp(l, fun):
        return list(map(fun, l))

    for i in iterable:
        temp1 = itd(temp, 'mappingProcess ' + str(temp2), (i, func))
        temp1.start()
        temp2 += 1
    itd.join()
    temp = (j for i in itd.threads for j in i.result)
    itd.clean_all()
    return temp

def pfilter(func, iterable:iter, true_only=False):
    """Uses pmap() to filter the result, same as
    the built-in filter function."""
    for i in pmap(func,iterable):
        if true_only:
            if i is True:
                yield i
        else:
            if i is not False:
                yield i


