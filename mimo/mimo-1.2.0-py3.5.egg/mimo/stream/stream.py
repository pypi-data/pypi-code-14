from mimo.io.io_set import IOSet


class Stream:

    __slots__ = ('state', 'ins', 'outs', 'name', 'fn')

    IN = []
    OUT = []

    def __init__(self, ins=None, outs=None, *, fn=None, name=None, state=None):
        """
        Initialise a stream. Streams can be sub-classed to alter the behaviour or customised directly.
        If sub-classing a stream, the class members `IN` and `OUT` define the names of the input and output entities.
        Overriding the `run` function will determine what the stream does and the name of the class determines the name
        of the stream.
        If creating a stream directly, the parameters `ins` and `outs` define the names of the input and output
        entities. The `fn` parameter is a function that will determine what the stream does. This function takes a set
        of inputs, a set of outputs and the state of the stream as a dictionary. The `name` parameter determines the
        name of the stream.

        :param ins: names of input entities
        :param outs: names of output entities
        :param name: name of the stream
        :param fn: run function
        """
        self.ins = self.IN if ins is None else ins
        self.outs = self.OUT if outs is None else outs
        self.fn = fn
        self.name = name if name is not None else \
            fn.__name__ if fn is not None else \
            type(self).__name__
        self.state = {} if state is None else state

    def run(self, ins, outs):
        """
        The main method to over-ride when implementing custom streams. This can also be over-ridden by providing the
        'fn' parameter when creating a new stream.

        :param ins: io set of input connections
        :type ins: IOSet
        :param outs: io set of output connections
        :type outs: IOSet
        :return: True if stream is did not finish running (eg. was suspended because output was full)
        :rtype: bool
        """
        return self.fn(ins, outs, self.state)
