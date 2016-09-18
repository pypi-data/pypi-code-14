import struct, math
"""
ConteMarlo
A "Monte-Carlo-Like" tester.
-Ryan Birmingham

The concept is simple (and probably already done better): detailed Monte-Carlo
but without the randomness.

Currently only works in 1d, but I want to generalize once I Get 1d working well.
I also want to construct tests first, so I know I don't break things.

Classes:
    Resolver - A generator for the next distribution value pair
    Distribution - A distribution, samplable at [0,1]
"""
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



class Distribution(Object):
    def __init__(name, *args, **kwargs):
        """Parse through and return a distributon object to call later. """
        # NOTE: Any distribution input space should be [0,1]. Scale after.
        supported = ["normal", "custom"]
        self.args=args
        self.kwargs=kwargs
        if name.lower() in supported:
            self.name=name
        else if isinstance(args[0], basestring):
            self.name = args[0]
        else if callable(args[0]):
            self.name = "passed_in"
            self.fcn = args[0]
        else:
            self.name = "custom"
        # add dimensionality if requested.
        if self.kwargs['dimensionality']:
            # NOTE: a n dimensional distribution should accept a n-long list
            self.dimensionality = self.kwargs['dimensionality']
        else:
            self.dimensionality = 1
        # call the proper construction function
        getattr(Distribution, self.name)()

    def passed_in(self):
        """We already have the function, just go on."""
        pass

    def __call__(self,  point):
        """Allow for the distribution to be called."""
        return self.fcn(point)

    def custom(self):
        """Take in a custom function, supplied by the user."""
        if callable(self.kwargs["dist"]):
            self.fcn = self.kwargs["dist"]
        else if callable(self.kwargs["distribution"]):
            self.fcn = self.kwargs["distribution"]
        else if callable(self.kwargs["fcn"]):
            self.fcn = self.kwargs["fcn"]
        else:
            raise ValueError("Did not find distribtion type " +
                             self.kwargs["distribution"]) # TODO fix
