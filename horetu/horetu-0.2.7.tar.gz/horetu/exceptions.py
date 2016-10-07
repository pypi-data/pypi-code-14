class HoretuException(Exception):
    def __init__(self, message, section=None):
        # message first so it is easy not to provide a section
        if section:
            self.section = section
        else:
            self.section = tuple()
        self.message = message

    def __repr__(self):
        return '%s(%s, section=%s)' % (
            self.__class__.__name__,
            repr(self.message),
            repr(self.section),
        )
    __str__ = __repr__

class HoretuError(HoretuException):
    ok = False

class HoretuCouldNotParse(HoretuError):
    pass

class Error(HoretuError):
    pass

class HoretuShowHelp(HoretuException):
    ok = True
