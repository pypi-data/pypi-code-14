#
#  -*- coding: utf-8 -*-
#
# (C) Copyright 2016 Karellen, Inc. (http://karellen.co/)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from collections import OrderedDict

import yaml
from yaml.composer import Composer
from yaml.constructor import ConstructorError, SafeConstructor
from yaml.emitter import Emitter
from yaml.nodes import SequenceNode, MappingNode
from yaml.parser import Parser
from yaml.reader import Reader
from yaml.representer import SafeRepresenter
from yaml.resolver import Resolver
from yaml.scanner import Scanner
from yaml.serializer import Serializer


class _KarellenStackConstructor(SafeConstructor):
    def construct_yaml_omap(self, node):
        # Note: we do not check for duplicate keys, because it's too
        # CPU-expensive.
        omap = OrderedDict()
        yield omap
        if not isinstance(node, SequenceNode):
            raise ConstructorError("while constructing an ordered map", node.start_mark,
                                   "expected a sequence, but found %s" % node.id, node.start_mark)
        for subnode in node.value:
            if not isinstance(subnode, MappingNode):
                raise ConstructorError("while constructing an ordered map", node.start_mark,
                                       "expected a mapping of length 1, but found %s" % subnode.id,
                                       subnode.start_mark)
            if len(subnode.value) != 1:
                raise ConstructorError("while constructing an ordered map", node.start_mark,
                                       "expected a single mapping item, but found %d items" % len(subnode.value),
                                       subnode.start_mark)
            key_node, value_node = subnode.value[0]
            key = self.construct_object(key_node)
            value = self.construct_object(value_node)
            omap[key] = value


_KarellenStackConstructor.add_constructor('tag:yaml.org,2002:omap', _KarellenStackConstructor.construct_yaml_omap)


class _KarellenStackLoader(Reader, Scanner, Parser, Composer, _KarellenStackConstructor,
                           Resolver):
    def __init__(self, stream):
        Reader.__init__(self, stream)
        Scanner.__init__(self)
        Parser.__init__(self)
        Composer.__init__(self)
        _KarellenStackConstructor.__init__(self)
        Resolver.__init__(self)


class _KarellenStackRepresenter(SafeRepresenter):
    def represent_ordered_dict(self, data):
        # Provide uniform representation across different Python versions.
        tag = 'tag:yaml.org,2002:omap'
        items = [{key: value} for key, value in data.items()]
        return self.represent_sequence(tag, items)


_KarellenStackRepresenter.add_representer(OrderedDict, _KarellenStackRepresenter.represent_ordered_dict)


class _KarellenStackDumper(Emitter, Serializer, _KarellenStackRepresenter, Resolver):
    def __init__(self, stream,
                 default_style=None, default_flow_style=None,
                 canonical=None, indent=None, width=None,
                 allow_unicode=None, line_break=None,
                 encoding=None, explicit_start=None, explicit_end=None,
                 version=None, tags=None):
        Emitter.__init__(self, stream, canonical=canonical, indent=indent, width=width, allow_unicode=allow_unicode,
                         line_break=line_break)
        Serializer.__init__(self, encoding=encoding, explicit_start=explicit_start, explicit_end=explicit_end,
                            version=version, tags=tags)
        _KarellenStackRepresenter.__init__(self, default_style=default_style, default_flow_style=default_flow_style)
        Resolver.__init__(self)


def load(stream):
    return yaml.load(stream, _KarellenStackLoader)


def dump(data, stream, **kwargs):
    return yaml.dump(data, stream, _KarellenStackDumper, **kwargs)
