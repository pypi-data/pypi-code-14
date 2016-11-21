import logging
import os
import re
from functools import wraps
from ..lib import Program
from ..signature import Signature, serialize_endpoint
from .doc import Doc

logger = logging.getLogger(__name__)

@serialize_endpoint
def _endpoints(section, s):
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
    return signature

def usage(f, h):
    prog = Program(f)
    if hasattr(prog.get(h.section), '__call__'):
        sections = []
        endpoints = _endpoints(prog, h.section)
    else:
        sections = ['/'.join(h.section + s) for s in prog]
        endpoints = []

    message = h.message
    sections = sections

    if message:
        yield '<em>%s</em>' % message
    yield '<ul>'
    for signature in sections:
        msg = '<li><a href="%(signature)s">%(signature)s</a></li>'
        yield msg % {'signature': signature}
    for signature in endpoints:
        yield '<li><code>%s</code></li>' % signature
    yield '</ul>'

def man(f, h):
    prog = Program(f)
    g = prog.get(h.section)
    fdoc = Doc(g)

    print(prog)
    is_section = hasattr(g, 'items')
    is_callable = hasattr(g, '__call__')
    endpoints = _endpoints(prog, h.section)
    description = list(filter(None, re.split('r[\n\r]{2,}', fdoc.desc)))
    args = list(fdoc.args)
    kwargs = fdoc.kwargs

    yield '''\
<h2>Synopsis<h2>
<ul>
'''
    for i, signature in enumerate(endpoints):
        if is_section and i == 0:
            yield '<strong>'
        yield signature
        if is_section and i == 0:
            yield '</strong>'
    yield '</ul>'
    if description:
        yield '<h2>Description</h2>'
        for p in description:
            yield '<p>%s</p>' % p
    if is_callable:
        if args:
            yield '''\
<h3>Inputs</h3>
<dl>
'''
        for pair in args:
            yield '<dt>%s</dt><dd>%s</dt>' % pair
        if len(args) == 0:
            yield '<p>(None)</p>'
        yield '''\
</dl>
<h3>Options</h3>
<dl>
'''
        for pair in kwargs:
            yield '<dt>%s</dt><dd>%s</dd>' % pair
        yield '</dl>'
    yield '''\
<h2>Detail</h2>
<p>
  Put "help" in the query string ("?help") for more help about a
  particular endpoint.
</p>
'''
