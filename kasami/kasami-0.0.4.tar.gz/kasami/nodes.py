from .productions import Production, SymbolProduction, TerminalProduction


class Node(Production):
    pass

    def format(self, depth):
        raise NotImplementedError()


class TerminalNode(Node, TerminalProduction):
    pass

    def format(self, depth=0):
        return "\t" * depth + str(self)

    def __iter__(self):
        yield TerminalProduction(self.source, self.produces)


class SymbolNode(Node, SymbolProduction):
    def __init__(self, source, targets):
        for target in targets:
            if not isinstance(target, Node):
                raise ValueError(
                    "target {0} should be a Node, but got {1} instead"
                    .format(repr(target), type(target)))

        Node.__init__(self, source, targets)

    def __repr__(self):
        return "{0}({1}, {2})".format(
            self.__class__.__name__, repr(self.source), repr(self.produces))

    def __iter__(self):
        yield SymbolProduction(self.source,
                               tuple(t.source for t in self.produces))

        for target in self.produces:
            yield from iter(target)

    def format(self, depth=0):
        return ("\t" * depth + "(" + self.source + "\n" +
                "\n".join(t.format(depth + 1) for t in self.produces) + "\n" +
                "\t" * depth + ")")
