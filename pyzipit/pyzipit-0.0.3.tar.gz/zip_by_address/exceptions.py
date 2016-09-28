class ZipByAddressResolverException(Exception):
    pass


class NoSuchAddress(ZipByAddressResolverException):
    def __init__(self, address=None):
        self.address = address

    def __str__(self):
        return str(self.address)
