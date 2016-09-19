import struct, math

class Distribution(object):
    def __init__(self, *args, **kwargs):
        """Parse through and return a distributon object to call later. """
        # NOTE: Any distribution input space should be [0,1]. Scale after.
        supported = ["normal", "custom"]
        self.args=args
        self.kwargs=kwargs
        if len(args) > 0:
            if isinstance(args[0], basestring):
                self.name = args[0]
            elif callable(args[0]):
                self.name = "passed_in"
                self.fcn = args[0]
            else:
                self.name = "custom"
        else:
            self.name = "custom"
        # add dimensionality if requested.
        if 'dimensionality' in kwargs:
            # NOTE: n dimensional distributions should accept n-long lists
            self.dimensionality = self.kwargs['dimensionality']
        else:
            self.dimensionality = 1
        # call the proper construction function
        getattr(Distribution, self.name)(self)

    @staticmethod
    def passed_in(self):
        """We already have the function, just go on."""
        pass

    def __call__(self,  point):
        """Allow for the distribution to be called."""
        return self.fcn(point)

    @staticmethod
    def custom(self):
        """Take in a custom function, supplied by the user."""
        if ("dist" in self.kwargs):
            if callable(self.kwargs["dist"]):
                self.fcn = self.kwargs["dist"]
            else:
                raise ValueError("Did not find distribtion type " +
                                 self.kwargs["dist"]) # TODO fix
        else:
            raise ValueError("No Distrubiton passed")
