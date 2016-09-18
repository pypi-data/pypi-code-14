import struct, math
from Distribution import Distribution

class Resolver(Object):
    def __init__(self, distribution, *args, **kwargs):
        """Parse through resolver inputs, and prepare for generator."""
        # check if is existing Distribution, else, make it once
        raise FutureWarning ("ConteMarlo is not Finished or tested.") # TODO
        if isinstance(distribution, Distribution):
            self.distribution = distribution
        else if callable(distribution):
            #  give it a "passed in" function
            self.distribution = Distribution(distribution)
        else:
            raise TypeError("Distribution passed is not callable.")
        self.layer = 1
        # set to one less than addressable int ln_2(max(INT) ) on system.
        if kwargs["high"]:
            self.high = kwargs["high"]
        else:
            self.high = (struct.calcsize("P") * 8)-1)
        # check dimensionality
        if self.distribution.dimensionality > 1:
            self.dimensionality = self.distribution.dimensionality

    def next(self, safe=True):
        """A generator to return the next [x,f(x)] pair from distribution."""
        # disallow anyone to flood their memory in safe mode
        while (self.position <= self.high or not safe):
            a = 2.0 ** math.ceil((math.log((self.position + 1), 2)))
            b = (2.0 * (a - self.position - 1) + 1) / a
            yield [a, self.distribution(a)]
        raise Warning("You have reached the end of safe mofe for next. " +
                      "Consider using next(unsafe=False) if you're not" +
                      " addresing all results in memory")

class Resolver_md(Resolver):
    def __init__(self, distribution, dimensionality, *args, **kwargs):
        """Multidimensional version of resolver."""
        # The normal resolver has init taken care of
        Resolver.__init__(self, distribution, *args, **kwargs):
        self.dimensionality = dimensionality

    def next(self, safe=True):
        """a n dimensional version of next_1d, with more gaps"""
        # make a n-len list of generators
        gen_list [0]*self.dimensionality
        # make a n-len list of positions (to pass to dist)
        tmp_in_list = [0]*self.dimensionality
        # start with getting the generators initalized.
        for i in range(1,self.dimensionality)
            # get a generator for each dimension
            gen_list[i]=Resolver.next
            tmp_in_list[i] = next(gen_list[i])
            # yield first result of 1/2 all
        yield [tmp_in_list,self.distribution(tmp_in_list)]
        # disallow anyone to flood their memory in safe mode
        while (self.position <= self.high or not safe):
            # which generator should we update?
            a = 2.0 ** math.ceil((math.log((self.position + 1), 2)))
            n = a % self.dimensionality
            tmp_in_list[n] = gen_list[n]
            # yield the new value pair
            yield [tmp_in_list,self.distribution(tmp_in_list)]
        raise Warning("You have reached the end of safe mofe for next. " +
                      "Consider using next(unsafe=False) if you're not" +
                      " addresing all results in memory")
