# Copyright 2016 Oliver Cope
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from gettext import NullTranslations

from piglet import compilexml
from piglet import compilett
from piglet.parse import parse_html
from piglet.compile import compile_to_module
from piglet.exceptions import PigletParseError
from piglet.runtime import data as rtdata, munge_exception_messages

ustr = type(u'')


class BaseTemplate:

    filename = None
    loader = None

    def compile_intermediate(self):
        raise NotImplementedError()

    def __init__(self, source,
                 filename='<string>',
                 loader=None,
                 translations_factory=None):
        self.filename = filename
        self.loader = loader
        if translations_factory:
            self.translations_factory = translations_factory
        try:
            self.template_module = compile_to_module(
                self.compile_intermediate(source),
                filename,
                bootstrap={'__piglet_template': self})
        except PigletParseError as e:
            e.filename = filename
            raise
        assert self.template_module is not None
        self.root_fn = self.template_module.__piglet_root__

    def __repr__(self):
        return "<{} {!r}>".format(type(self).__name__, self.filename)

    def __call__(self, context, *args, **kwargs):
        if not hasattr(rtdata, 'context'):
            rtdata.context = []
        rtdata.context.append(context)
        rtdata.exception_locations = []
        translations = self.translations_factory()
        context.update({'_': translations.gettext,
                        'gettext': translations.gettext,
                        'ngettext': translations.ngettext})
        content = munge_exception_messages(self.root_fn(*args, **kwargs),
                                           context)
        try:
            for s in content:
                yield s
        finally:
            rtdata.context.pop()

    def render(self, context, *args, **kwargs):
        return ''.join(map(ustr, self(context, *args, **kwargs)))

    def __getattr__(self, name):
        """
        Expose template functions as attributes, eg:

            >>> t = Template('<py:def function="greeting">Hello!</py:def>')
            >>> print(t.greeting())
            'Hello!'
        """
        return getattr(self.template_module, name)

    def translations_factory(self):
        return NullTranslations()


class HTMLTemplate(BaseTemplate):
    def compile_intermediate(self, src):
        parsed = parse_html(src)
        return compilexml.compile_intermediate(parsed)


class TextTemplate(BaseTemplate):
    def compile_intermediate(self, src):
        parsed = compilett.parse_tt(src)
        return compilett.compile_intermediate(parsed)


Template = HTMLTemplate
