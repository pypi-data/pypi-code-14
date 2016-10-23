from pyil.enum.modifiable import divide as __div
from pyil.enum.variable import auto_process


def pmap(func, iter, process=auto_process):
    """Equal to map function but with real
    threading in it."""
    from .thread import IsoThread as itd
    process = auto_process(len(iter))
    iter = __div(iter, process)
    temp2=0

    def temp(l,fun):
        return list(map(fun, l))

    for i in iter:
        temp1=itd(temp, 'mappingProcess ' + str(temp2), (i,func))
        temp1.start()
        temp2+=1
    itd.join()
    for i in itd.threads:
        for j in i:
            yield j

