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


from collections import namedtuple

from jsonmerge import Merger
from jsonmerge.exceptions import JSONMergeError
from voluptuous import Invalid, MultipleInvalid

from karellen.stack.core.schema.schemas import MINIMAL_SCHEMA_STACK_CORE, INHERIT_JSON_SCHEMA, INCLUDE_JSON_SCHEMA
from karellen.stack.core.schema.yaml import load
from karellen.stack.core.spi import Context, UrlLoader
from karellen.stack.utils import inherit_doc
from karellen.stack.utils.logging import getLogger


class StackConfigError(Exception):
    pass


DEPENDENCY_ACTION_INHERIT = "inherit"
DEPENDENCY_ACTION_INCLUDE = "include"
config_dependency = namedtuple("config_dependency", ["action", "source"])


@inherit_doc
class DependencyLoopError(StackConfigError):
    def __init__(self, dependency_path):
        self.dependency_path = dependency_path


@inherit_doc
class SchemaValidationError(StackConfigError):
    def __init__(self, invalid_error, data, source):
        if isinstance(invalid_error, MultipleInvalid):
            errors = invalid_error.errors
        else:
            errors = [invalid_error]
        self.errors = errors
        self.source = source
        self.data = data

    def __str__(self):
        return "The following validation errors occurred%s:%s" % \
               (" in '%s'" % self.source if self.source else "",
                "".join(("\n\t%s: %s" % (self.format_path(error.path),
                                         error.error_message) for error in self.errors)))

    def format_path(self, path):
        data_item = self._nested_getitem(path)
        return "%s=%s" % ("/".join((str(p) for p in path)), data_item)

    def _nested_getitem(self, path):
        data = self.data
        for item_index in path:
            try:
                data = data[item_index]
            except (KeyError, IndexError):
                # The index is not present in the dictionary, list or other indexable
                return None
        return data


@inherit_doc
class ConfigMergeError(StackConfigError):
    def __init__(self, source_url, dest_url):
        self.source_url = source_url
        self.dest_url = dest_url


StackExtensionPlugin = namedtuple("StackExtensionPlugin",
                                  ["name", "extension_name", "extension", "plugin", "dependencies"])


@inherit_doc
class StackConfig(object):
    logger = getLogger(__name__ + ".StackConfig")

    def __init__(self, context: Context, loader: UrlLoader, *,
                 _prev: "StackConfig" = None,
                 _target: "StackConfig" = None):
        self.loader = loader
        self.context = context
        self._prev = _prev
        self._target = _target if _target else self

        self.doc_source = None
        self.declared_doc = None
        self.effective_doc = None

        self._configs = {}  # Loader: StackConfig
        self._pending_loads = []

        self._parent = None
        self._includes = []

        self._extensions = {}

    @property
    def previous(self) -> 'StackConfig':
        """Previous ``StackConfig`` which caused this configuration to be loaded"""
        return self._prev

    @property
    def target(self) -> 'StackConfig':
        """Target ``StackConfig`` which transitively caused this configuration to be loaded"""
        return self._target

    @property
    def parent(self) -> 'StackConfig':
        """``StackConfig`` from which this inherits"""
        return self._parent

    @property
    def source_url(self):
        """``Url``: The absolute ``Url`` from which this ``StackConfig`` was loaded"""
        return self.loader.absolute

    @property
    def canonical_url(self):
        """``Url``: The canonical Url from which this ``StackConfig`` was loaded"""
        return self.loader.canonical

    def load(self):
        self._configs[self.loader] = self

        self._load()

        pending_loads = self._pending_loads
        while pending_loads:
            pending_load = pending_loads.pop()
            for dummy in pending_load:
                pass

        self._validate_dep_chain()

        self._assemble_effective_config()

        self._configure_extension_points()

    def _load(self):
        """Load source and resolve source dependencies"""

        self._load_source()

        self._resolve()

    def _load_source(self):
        """Simply load source of this ``Stack Configuration``"""
        if not self.previous:
            self.logger.info("Loading configuration source from '%s'", self.source_url)
        else:
            self.logger.info("Loading configuration source from '%s' initiated by '%s'", self.source_url,
                             self.previous.source_url)

        with self.loader as loader:
            with loader.stream() as s:
                self.doc_source = load(s)
                if not self.doc_source:
                    self.doc_source = {}

    def _validate_linkage_config(self):
        self.logger.debug("Validating '%s'", self.loader.absolute)
        try:
            self.declared_doc = MINIMAL_SCHEMA_STACK_CORE(self.doc_source)
        except (Invalid, MultipleInvalid) as e:
            raise SchemaValidationError(e, self.doc_source, self.loader) from None

    def _resolve(self):
        """Perform resolution of this ``StackConfig``.

        The process consist of:
            #. Validate linkage data
            #. Processing includes
            #. Processing inheritance
        """

        self._validate_linkage_config()

        self.target._pending_loads.append(self._load_included())

        self.target._pending_loads.append(self._load_inherited())

    def _load_inherited(self):
        self.logger.debug("Loading inheritance for '%s'", self.source_url)
        parent = self.declared_doc.get("inherit")
        if parent:
            loader = self.context.get_loader(parent, self.source_url)
            if loader in self.target._configs:
                parent_config = self.target._configs[loader]
                self._parent = parent_config
            else:
                parent_config = StackConfig(self.context, loader, _prev=self, _target=self.target)
                self.target._configs[loader] = parent_config
                self._parent = parent_config

                yield

                parent_config._load()

    def _load_included(self):
        self.logger.debug("Loading includes for '%s'", self.source_url)
        includes = self.declared_doc.get("include")
        if includes:
            includes_to_load = []
            for include in includes:
                loader = self.context.get_loader(include, self.source_url)
                if loader in self.target._configs:
                    include_config = self.target._configs[loader]
                    self._includes.append(include_config)
                else:
                    include_config = StackConfig(self.context, loader, _prev=self, _target=self.target)
                    self.target._configs[loader] = include_config
                    self._includes.append(include_config)
                    includes_to_load.append(include_config)

            yield

            for include_config in includes_to_load:
                include_config._load()

    def _validate_dep_chain(self):
        def validate_dep_chain(config, action, traversed, path):
            path.append(config_dependency(action, config.source_url))

            if (action, config) in traversed:
                raise DependencyLoopError(path)

            traversed.add((action, config))

            if config._parent:
                validate_dep_chain(config._parent, DEPENDENCY_ACTION_INHERIT, traversed, path)

            if config._includes:
                for include in config._includes:
                    validate_dep_chain(include, DEPENDENCY_ACTION_INCLUDE,
                                       set((v for v in traversed if v[0] in DEPENDENCY_ACTION_INCLUDE)), path)

        traversed_set = {(DEPENDENCY_ACTION_INCLUDE, self)}
        validate_dep_chain(self, DEPENDENCY_ACTION_INHERIT, traversed_set, [])

    def _assemble_effective_config(self):
        pending_loads = []
        pending_generators = []

        def get_heritable_config(doc):
            return {k: v for k, v in doc.items() if k not in {"inherit", "include"}}

        def merge_configs(action, from_source, into_dest, source_url, dest_url):
            try:
                merger = Merger(
                    schema=INHERIT_JSON_SCHEMA if action == DEPENDENCY_ACTION_INHERIT else INCLUDE_JSON_SCHEMA)
                return merger.merge(into_dest, from_source)
            except JSONMergeError as e:
                raise ConfigMergeError(source_url, dest_url) from e

        def assemble_config(self):
            parent = self.parent

            scheduled_dependent_loads = False

            if parent:
                if parent.effective_doc is None:
                    pending_loads.append(parent)
                    scheduled_dependent_loads = True

            if self._includes:
                for include in self._includes:
                    if include.effective_doc is None:
                        pending_loads.append(include)
                        scheduled_dependent_loads = True

            if scheduled_dependent_loads:
                yield

            if self.effective_doc is not None:
                self.logger.debug("Found effective configuration for '%s'", self.source_url)
                return

            self.logger.info("Compiling effective configuration for '%s'", self.source_url)

            effective_doc = {}

            if parent:
                effective_doc = merge_configs(DEPENDENCY_ACTION_INHERIT,
                                              parent.effective_doc,
                                              effective_doc,
                                              parent.source_url,
                                              self.source_url)

            for include in self._includes:
                effective_doc = merge_configs(DEPENDENCY_ACTION_INCLUDE,
                                              include.effective_doc,
                                              effective_doc,
                                              include.source_url,
                                              self.source_url)

            effective_doc = merge_configs(DEPENDENCY_ACTION_INHERIT,
                                          get_heritable_config(self.declared_doc),
                                          effective_doc,
                                          self.source_url,
                                          self.source_url)

            self.effective_doc = effective_doc

        pending_generators.append(assemble_config(self))

        while pending_loads or pending_generators:
            while pending_loads:
                pending_generators.append(assemble_config(pending_loads.pop()))

            while pending_generators:
                gen = pending_generators[-1]
                try:
                    next(gen)
                    break
                except StopIteration:
                    pending_generators.pop()

        assert not pending_loads
        assert not pending_generators
        assert self.effective_doc is not None

    def _configure_extension_points(self):
        context = self.context
        extensions = self.effective_doc.get("extensions")

        if extensions:
            for name, extension_config in extensions.items():
                extension_name = extension_config["extension"]
                plugin = extension_config["plugin"]
                dependencies = extension_config.get("dependencies")

                extension = context.extension_manager.get_extension(extension_name)
                extension_plugin = StackExtensionPlugin(name, extension_name, extension, plugin, dependencies)
                self.logger.debug("Registering extension plugin %s = %s, %s, %s", name, extension_name, plugin,
                                  dependencies)
                self._extensions[name] = extension_plugin

    def __repr__(self):
        return "%s<%s>" % (type(self).__name__, self.source_url)
