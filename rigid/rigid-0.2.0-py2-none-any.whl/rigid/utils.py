class ObservedFileWrapper(object):
    def __init__(self, fd, callback):
        self.fd = fd
        self.callback = callback

    def __getattr__(self, attr):
        get = object.__getattribute__

        if attr in ('read', 'callback'):
            return get(self, attr)

        fd = get(self, 'fd')
        return getattr(fd, attr)

    def read(self, size):
        self.callback(size)
        return self.fd.read(size)
