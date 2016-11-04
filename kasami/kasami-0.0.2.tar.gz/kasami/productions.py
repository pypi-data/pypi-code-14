class Production:
    __slots__ = ['source', 'produces']

    def __init__(self, source, produces):
        self.source = str(source)
        self.produces = produces

    def __repr__(self):
        return "{0}({1}, {2})".format(
            self.__class__.__name__, repr(self.source), repr(self.produces))

    def __eq__(self, other):
        return self.source == other.source and \
               self.produces == other.produces

    def __hash__(self):
        return hash((self.source, self.produces))


class TerminalProduction(Production):

    def __init__(self, source, literal):
        super().__init__(source, str(literal))

    def __str__(self):
        return "({0} {1})".format(self.source, repr(self.produces))


class SymbolProduction(Production):

    def __init__(self, source, targets):
        super().__init__(source, tuple(str(target) for target in targets))

    def __str__(self):
        return "({0} {1})".format(
            self.source, " ".join(str(t) for t in self.produces))
