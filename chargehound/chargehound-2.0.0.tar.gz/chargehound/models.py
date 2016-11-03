from collections import namedtuple
from neobunch import NeoBunch


class ChargehoundObject(NeoBunch):
    pass


class List(ChargehoundObject):
    pass


class Dispute(ChargehoundObject):
    pass


class Product(ChargehoundObject):
    pass


class Response(ChargehoundObject):
    pass


HTTPResponse = namedtuple('HTTPResponse', 'status')
