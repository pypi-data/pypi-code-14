from pyil.enum.modifiable import divide as __div
import dill as __dill
from pyil.enum.variable import auto_process
import abc
@abc.abstractmethod
def pmap(func,iter,process=auto_process):
    """Not implemented yet, don't use."""
    from .thread import IsoThread as itd
    from .._coll import random_word
    process=auto_process(len(iter))
    iter=__div(iter, process)
    temp1="temp"+random_word(9,word_only=True)+'.func'
    __dill.dump(func,temp1)
    def temp(l:list):
        import dill
        mfunc=dill.load(temp1)
        return list(map(mfunc,l))
    for i in iter:
        temp2=itd(temp,i)
        temp2.start()
    itd.join()



