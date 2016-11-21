import logging
from funmap import funmap
from triedict import triedict

logger = logging.getLogger(__name__)

def validate_param_name(*xs):
    msg = 'It is best if you remove "%s" from the argument name "%s".'
    for x in xs:
        for c in '/?[]<>():':
            if x in c:
                logger.warning(msg % (c, x))
    
def Program(functions):
    '''
    :param functions: Base function or functions
    :rtype: dict
    :returns: Map path tuples to functions.
    '''
    return triedict(_sub(tuple(), functions))

def _sub(section, fs):
    '''
    :param tuple section: Sections that this sub-program is under
    '''
    if hasattr(fs, '__call__'):
        yield section, fs, 

    if hasattr(fs, 'items'):
        items = fs.items()
    elif hasattr(fs, '__iter__'):
        items = ((f.__name__,f) for f in fs)
    else:
        items = []
    for name, f in items:
        validate_param_name(*name)
        yield from _sub(section + (name,), f)
