import os
from abc import ABCMeta
from functools import wraps, partial

def AppIter(x):
    '''
    :param x: Anything (returned from the underlying program)
    :rtype: Iterable of bytes
    :returns: Output as bytes
    '''
    if x is None:
        raise StopIteration
    elif isinstance(x, bytes):
        yield x
    elif isinstance(x, str):
        yield x.encode('utf-8')
    elif hasattr(x, '__iter__'):
        for y in x:
            yield from AppIter(y)
    else:
        yield format(x).encode('utf-8')

class TemplateEnvironment(metaclass=ABCMeta):
    raw_templates = {}
    def __init__(self, directory=None):
        if directory:
            self._directory = os.path.abspath(directory)
        else:
            self._directory = None

    @staticmethod
    def Template(x):
        raise NotImplementedError('You must define the Template method.')

    @property
    def render(self):
        msg = 'Set the %(c).render property to the %(c).Template method for rendering.'
        raise NotImplementedError(msg % {'c': self.__class__.__name__})

    def string(self, template):
        '''
        Render a template from a string.

        :param str template: The string of the template
        :rtype: decorator
        '''
        tpl = Template(path)
        return self._render(tpl)

    def file(self, filename):
        '''
        Render a template from a file.

        :param str filename: The file containing the template
        :rtype: decorator
        '''
        abspath = os.path.join(self._directory, filename)
        if abspath not in self.raw_templates:
            with open(abspath) as fp:
                self.raw_templates[abspath] = self.Template(fp.read())
        return self._render(self.raw_templates[abspath])

    def _render(self, tpl):
        def decorator(func):
            '''
            :param func: Function that returns a mapping (dict)
            '''
            @wraps(func)
            def wrapper(*args, **kwargs):
                fields = func(*args, **kwargs)
                if isinstance(self.render, str):
                    f = getattr(tpl, self.render)
                else:
                    f = partial(self.render, tpl)
                return AppIter(f(**fields))
            return wrapper
        return decorator

import string
class Template(TemplateEnvironment):
    Template = string.Template
    render = 'safe_substitute'

try:
    import airspeed
except ImportError:
    pass
else:
    class Airspeed(TemplateEnvironment):
        Template = airspeed.Template
        render = 'merge'

try:
    import bottle
except ImportError:
    pass
else:
    class Bottle(TemplateEnvironment):
        Template = bottle.SimpleTemplate
        render = 'render'

try:
    import django.conf, django.template
    django.conf.settings.configure()
except ImportError:
    pass
else:
    class Django(TemplateEnvironment):
        Template = django.template.Template
        @staticmethod
        def render(tpl, **ctx):
            return tpl.render(django.template.Context(ctx))

try:
    import jinja2
except ImportError:
    pass
else:
    class Jinja2(TemplateEnvironment):
        Template = jinja2.Template
        render = 'render'

try:
    import mako.template
except ImportError:
    pass
else:
    class Mako(TemplateEnvironment):
        Template = mako.template.Template
        render = 'render'

try:
    import moody
except ImportError:
    pass
else:
    class Moody(TemplateEnvironment):
        Template = moody.compile
        render = 'render'

try:
    import pystache
except ImportError:
    pass
else:
    class Mustache(TemplateEnvironment):
        Template = pystache.parse
        @staticmethod
        def render(tpl, **ctx):
            pystache.renderer

try:
    import pyratemp
except ImportError:
    pass
else:
    class Pyratemp(TemplateEnvironment):
        Template = pyratemp.Template
        render = '__call__'

try:
    import tempita
except ImportError:
    pass
else:
    class Tempita(TemplateEnvironment):
        Template = tempita.Template
        render = 'substitute'

try:
    import tonnikala.loader
except ImportError:
    pass
else:
    class Tonnikala(TemplateEnvironment):
        Template = tonnikala.loader.Loader().load_string
        render = 'render'

try:
    import trender
except ImportError:
    pass
else:
    class TRender(TemplateEnvironment):
        Template = trender.TRender
        render = 'render'

try:
    import wheezy.template
except ImportError:
    pass
else:
    class Wheezy(TemplateEnvironment):
        @staticmethod
        def Template(x):
            name = 'unnecessary-template-name'
            l = wheezy.template.DictLoader({name: x})
            e = wheezy.template.Engine(loader=l,
                                       extensions=[wheezy.template.CoreExtension()])
            return e.get_template(name)
        render = 'render'

'''
# Template template
try:
    import 
except ImportError:
    pass
else:
    class (TemplateEnvironment):
        Template = 
        render = ''
'''
