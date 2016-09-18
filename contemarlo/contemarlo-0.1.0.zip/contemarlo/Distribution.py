import struct, math

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
