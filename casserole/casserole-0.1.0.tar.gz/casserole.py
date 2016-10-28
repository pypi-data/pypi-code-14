import itertools
import operator
import optparse
import os
import sys


class SettingsItem(object):
    optparse_types = {
        str: 'string',
        unicode: 'string',
        int: 'int',
        float: 'float',
        bool: 'bool',
    }

    def __init__(self, key, data_type=None, default=None, choices=None,
                 flags=None, **kwargs):
        self.key = key
        self.norm_key = key.upper()
        self.default = default
        self.choices = choices
        self.option_config = kwargs
        self.flags = flags or ('-%s' % key[0], '--%s' % key.lower())

        if data_type and data_type not in self.optparse_types:
            type_list = sorted('%r' % k for k in self.optparse_types)
            raise ValueError('Unsupported type "%r". Must be one of %s.' % (
                data_type,
                ', '.join(type_list)))
        self.data_type = data_type

    def make_option(self):
        config = {'dest': self.norm_key, 'choices': self.choices}
        if self.data_type is bool:
            config['action'] = 'store_true'
        elif self.data_type:
            config['type'] = self.optparse_types[self.data_type]

        config.update(self.option_config)
        return optparse.make_option(*self.flags, **config)

    def _read(self, source, is_attr=False):
        method = operator.attrgetter if is_attr else operator.itemgetter
        try:
            return method(self.norm_key)(source)
        except (KeyError, AttributeError):
            pass

    def read(self, sources):
        for source, is_attr in sources:
            if source is not None:
                value = self._read(source, is_attr=is_attr)
                if value is not None:
                    return value
        return self.default


class Settings(object):
    def __init__(self, *settings_items):
        self.items = settings_items
        self.sources = []

    def register_source(self, source, is_attr=False):
        self.sources.append((source, is_attr))
        return self

    def read(self, *additional_sources):
        if additional_sources:
            sources = self.sources + list(additional_sources)
        settings = {}
        for item in self.items:
            settings[item.key] = item.read(sources)
        return settings

    def option_parser(self, **kwargs):
        parser = optparse.OptionParser(**kwargs)
        for item in self.items:
            parser.add_option(item.make_option())
        return parser

    def load(self, command_options=True, environment=True):
        additional_sources = []
        if command_options:
            option_parser = self.option_parser()
            options, args = option_parser.parse_args()
            additional_sources.append((options, True))

        if environment:
            additional_sources.append((os.environ, False))

        return self.read(*additional_sources)
