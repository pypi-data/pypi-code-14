from pyil.enum.modifiable import divide as _div
from pyil.enum.variable import auto_process


class PMap:
    def __init__(self, func, iterable, process=auto_process):
        """Returns a PMap object. The usage is similar to the
        map function and does the same work except that this
        one is multi-threaded."""
        from .thread import IsoThread as itd
        if str(type(process))=="class <'function'>":
            process = process(len(iterable))
            iterable = _div(iterable, process)
        else:
            iterable=_div(iterable,process)
        temp2 = 0

        def temp(l, fun):
            return list(map(fun, l))

        for i in iterable:
            temp1 = itd(temp, 'mappingProcess ' + str(temp2), (i, func))
            temp1.start()
            temp2 += 1
        itd.join()
        self.__cur = -1

    def __iter__(self):
        return self

    def next(self):
        from .thread import IsoThread as itd
        temp = 0
        for i in itd.threads:
            for j in i.result:
                if temp == self.__cur + 1:
                    self.__cur += 1
                    return j
                temp += 1
        raise StopIteration()

    def __next__(self):
        from .thread import IsoThread as itd
        for i in range(len([j for i in itd.threads for j in i])):
            self.__cur+=1
            if i==self.__cur:
                return range(len([j for i in itd.threads for j in i]))[i]
        raise StopIteration()
