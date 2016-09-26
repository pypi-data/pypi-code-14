from collections import namedtuple


Host = namedtuple('Host', ['address', 'port'])

HTTP_METHODS = ['get', 'options', 'head', 'post', 'put', 'patch', 'delete']
