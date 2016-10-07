import logging
import os
import re
from collections import namedtuple
from functools import wraps
from ..lib import Program
from ..signature import Signature
from .doc import Doc

try:
    from ..templates import Jinja2
except ImportError:
    import sys
    def template(filename):
        def decorator(f):
            def wrapper(*args, **kwargs):
                logger.error('Jinja2 is not installed; run this: pip install horetu[all]')
                sys.exit(1)
        return decorator
else:
    _template_dir = os.path.abspath(os.path.join(__file__, '..', 'templates'))
    template = Jinja2(_template_dir).file

logger = logging.getLogger(__name__)

WebResponse = namedtuple('WebResponse', ['content_type', 'data'])
def content_type(x):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return WebResponse(x, func(*args, **kwargs))
        return wrapper
    return decorator

def _endpoints(prog, root_section):
    for section in sorted(prog):
        if section[:len(root_section)] == root_section:
            s = Signature(prog[section])

            signature = ''
            for x in section:
                signature += '/%s' % x
            for x in s.positional:
                signature += '/:%s' % x.name
            for x in s.keyword1:
                signature += '/[%s]' % x.name
            if s.var_positional:
                signature += '/&lt;%s&gt;' % s.var_positional.name
            signature += '?(option=...)'
            yield signature

@content_type('text/html')
@template('wsgi-usage.html')
def usage(f, h):
    prog = Program(f)
    if hasattr(prog.get(h.section), '__call__'):
        sections = []
        endpoints = list(_endpoints(prog, h.section))
    else:
        sections = ['/'.join(h.section + s) for s in prog]
        endpoints = []
    return {
        'message': h.message,
        'sections': sections,
        'endpoints': endpoints,
    }

@content_type('text/html')
@template('wsgi-man.html')
def man(f, h):
    prog = Program(f)
    g = prog.get(h.section)
    fdoc = Doc(g)
    return {
        'is_section': hasattr(g, 'items'),
        'is_callable': hasattr(g, '__call__'),
        'endpoints': list(_endpoints(prog, h.section)),
        'description': list(filter(None, re.split('r[\n\r]{2,}', fdoc.desc))),
        'args': fdoc.args,
        'kwargs': fdoc.kwargs,
    }
