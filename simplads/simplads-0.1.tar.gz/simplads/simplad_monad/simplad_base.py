import abc

class SimpladBase(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def unit(func):
        ''' takes a function, applies it to a value and returns
            a bound default value '''
        return

    @abc.abstractmethod
    def bind(func):
        ''' returns a function that that takes a
            (bound, higher_deltas)

            this function will do the following:

            deltas = something(higherDeltas)
            unbound = something(bound)
            unbound, deltas, bind = func(unbound)
            if bind is False return [unbound, deltas]
            delta, deltas = something(deltas)
            bound = something(delta, unbound)
            return BindArgs(bound=bound, deltas=deltas)
        '''
        return
