from django import template
from django.template.base import TemplateSyntaxError

from ..utils import function_from_string

register = template.Library()

"""
class TemplateIfExperimentParser(IfParser):
    error_class = TemplateSyntaxError
    def __init__(self, parser, *args, **kwargs):
        self.template_parser = parser
        super(TemplateIfExperimentParser, self).__init__(*args, **kwargs)

    def create_var(self, value):
        pass
"""

class IfExperimentNode(template.Node):
    def __init__(self, nodelists):
        self.nodelists = nodelists

    def _set_user(self, context):
        request = template.Variable('request').resolve(context)
        if request.user.is_authenticated():
            self._user_id = request.user.id
            self._user_authenticated = True
        else:
            self._user_authenticated = False

    def prepare_experiment_params(self, bits, context):
        config = template.Variable(bits[0]).resolve(context)
        callable_name = None
        only_authenticated = None
        lbits = bits.__len__()
        if lbits > 1:
            mysterious = bits[1]
            if type(mysterious) == bool:
                only_authenticated = mysterious
            else:
                callable_name = mysterious
        elif lbits > 2:
            callable_name = bits[1]
            only_authenticated = bits[2]
        return config, callable_name, only_authenticated


    def matches_experiment(self, bits, context):
        if not bits:
            return True


        tup = self.prepare_experiment_params(bits, context)
        config = tup[0]

        if not config:
            return False

        callable_name = tup[1]
        only_authenticated = tup[2]

        if callable_name is None:
            if (only_authenticated is not None and
                    only_authenticated and
                    not self._user_authenticated):
                return False
            else:
                return True
        else:
            if not self._user_authenticated:
                return False
            else:
                _callable = function_from_string(callable_name)
                return self._user_id in _callable()
        return match

    def render(self, context):
        self._set_user(context)
        for nodelist, bits in self.nodelists:
            if self.matches_experiment(bits, context):
                return nodelist.render(context)
        return ''

@register.tag
def ifexperiment(parser, token):
    bits = token.split_contents()[1:]
    nodelist = parser.parse(('elifexperiment', 'else', 'endifexperiment'))
    nodelists = [(nodelist, bits)]
    token = parser.next_token()

    # {% elif ... %} (repeatable)
    while token.contents.startswith('elifexperiment'):
        bits = token.split_contents()[1:]
        nodelist = parser.parse(('elifexperiment', 'else', 'endifexperiment'))
        nodelists.append((nodelist, bits))
        token = parser.next_token()

    # {% else %} (optional)
    if token.contents == 'else':
        nodelist = parser.parse(('endifexperiment',))
        nodelists.append((nodelist, []))
        token = parser.next_token()

    # {% endif %}
    if token.contents != 'endifexperiment':
        raise TemplateSyntaxError('Malformed template tag at line {0}: "{1}"'.format(token.lineno, token.contents))

    return IfExperimentNode(nodelists)
