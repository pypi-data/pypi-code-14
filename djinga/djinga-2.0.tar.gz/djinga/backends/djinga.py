"""
Djinga backend for use in Django 1.8+
"""

from inspect import getargspec
import jinja2

from django.template.backends.django import DjangoTemplates
from django.conf import settings
from django.utils.module_loading import import_string

try:
    from django.template.engine import _dirs_undefined
except ImportError:
    # Django >= 1.10
    _dirs_undefined = None


JJENV_OPTION_NAMES = getargspec(jinja2.environment.Environment.__init__)[0][1:]


class DjingaTemplates(DjangoTemplates):

    def __init__(self, params):

        options = params['OPTIONS']

        env = options.pop('environment', 'djinga.Environment')
        env_cls = import_string(env)

        jjenv_options_names = JJENV_OPTION_NAMES + \
                              getargspec(env_cls.__init__)[0][1:]

        jjenv_options = {}
        for k in list(options.keys()):
            if k in jjenv_options_names:
                jjenv_options[k] = options.pop(k)

        super(DjingaTemplates, self).__init__(params.copy())

        jjenv_options.setdefault(
            'loader', jinja2.FileSystemLoader(self.template_dirs)
        )

        jjenv_options.setdefault('auto_reload', settings.DEBUG)
        jjenv_options.setdefault('undefined',
                                  jinja2.DebugUndefined
                                  if settings.DEBUG else jinja2.Undefined)

        self.env = env_cls(**jjenv_options)

    def from_string(self, template_code):
        return self.env.from_string(template_code)

    def _get_template(self, template_name, **kwargs):
        if self.env.use_jinja(template_name):
            return self.env.get_template(template_name)
        return super(DjingaTemplates, self).get_template(template_name,
                                                         **kwargs)

    if _dirs_undefined is None:
        # django 1.10+
        def get_template(self, template_name):
            return self._get_template(template_name)
    else:
        def get_template(self, template_name, dirs=_dirs_undefined):
            return self._get_template(template_name, dirs=dirs)
