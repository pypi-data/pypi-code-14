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


from threading import local
from typing import Iterable

from pkg_resources import EntryPoint  # noqa
from pkg_resources import WorkingSet

from karellen.stack.core import Url, url  # noqa
from karellen.stack.utils import inherit_doc
from karellen.stack.utils.logging import getLogger, TRACE, DEBUG


class ProviderError(RuntimeError):
    pass


class NoSuchProviderError(ProviderError):
    pass


class AmbiguousProviderError(ProviderError):
    pass


class PluginManager(object):
    logger = getLogger(__name__ + ".PluginManager")

    def __init__(self, *, site_path=None, **kwargs):
        self._site_path = site_path
        self._working_set = WorkingSet(entries=self._site_path)

    def providers(self, service_name, provider_name=None) -> Iterable[EntryPoint]:
        return self._working_set.iter_entry_points(service_name, provider_name)

    def provider(self, service_name, provider_name):
        self.logger.debug("resolving provider '%s' for service name '%s'", provider_name, service_name)
        providers = [provider for provider in self.providers(service_name, provider_name)]
        if not providers:
            raise NoSuchProviderError("no provider '%s' found for service name '%s'" % (provider_name, service_name))
        # if len(providers) > 1:
        #   raise AmbiguousProviderError(
        #   "multiple providers '%s' found for service name '%s': %s" % (provider_name, service_name, providers))
        provider = providers[0]  # type: EntryPoint
        self.logger.debug("resolved service name '%s': %s", service_name, provider)
        return provider.resolve()


class ExtensionError(ProviderError):
    pass


class ExtensionPointConflictError(ExtensionError):
    def __init__(self, ep1, ep2, entry_name):
        self.ep1 = ep1
        self.ep2 = ep2
        self.entry_name = entry_name


class NoSuchExtensionError(ExtensionError):
    pass


class ExtensionPointManager(object):
    logger = getLogger(__name__ + ".ExtensionPointManager")

    def __init__(self, plugin_manager: PluginManager):
        self.plugin_manager = plugin_manager
        self._extensions = {}
        self._extension_entries = {}

        epss = self._extensions
        logger = self.logger
        config_entries = self._extension_entries

        for extension in self.plugin_manager.providers("karellen.stack.core.extension"):
            epss[extension.name] = plugin_class = extension.resolve()  # type: Extension
            if logger.isEnabledFor(DEBUG):
                logger.debug("Registered extension point %s = %s " +
                             "with configuration entries:%s", extension.name,
                             plugin_class,
                             "".join(("\n\t" + entry for entry in plugin_class.config_entries()))
                             )
        for eps_name in epss:
            eps = epss[eps_name]
            for ce in eps.config_entries():
                if ce in config_entries:
                    raise ExtensionPointConflictError(eps, config_entries[ce], ce)
                self._extension_entries[ce] = eps

    def get_extension(self, name):
        try:
            return self._extensions[name]
        except KeyError:
            raise NoSuchExtensionError from None


class Context(object):
    CURRENT_CONTEXT = local()
    logger = getLogger(__name__ + ".Context")

    def __init__(self, *,
                 plugin_manager,
                 auth_provider,
                 extension_manager,
                 path_manager,
                 **kwargs):
        self._plugin_manager = plugin_manager
        self._auth_provider = auth_provider
        self._extension_manager = extension_manager
        self._path_manager = path_manager

        self._loader_cache = {}  #: (source_url, base_url): UrlLoader

    @property
    def path_manager(self) -> "PathManager":
        return self._path_manager

    @property
    def plugin_manager(self) -> "PluginManager":
        return self._plugin_manager

    @property
    def auth_provider(self) -> "AuthenticationProvider":
        return self._auth_provider

    @property
    def extension_manager(self) -> "ExtensionPointManager":
        return self._extension_manager

    def get_loader(self, source, base=None):
        id = UrlLoader.to_absolute(source, base)
        loader_cache = self._loader_cache
        loader = loader_cache.get(id)
        if not loader:
            loader = ContextUrlLoader(self, source, base)
            loader_cache[id] = loader
        else:
            self.logger.log(TRACE, "Using an existing loader for %s: %s", id, loader)

        return loader


class UrlLoader(object):
    def __init__(self, context, source, base=None):
        self.context = context
        if isinstance(source, str):
            source = url(source)
        self.source = source  # type: Url
        if base and isinstance(base, str):
            base = url(base)
        self.base = base  # type: Url
        self._absolute_url = base.as_abs_base(source) if base else source  # type: Url
        self._canonical_url = None
        self._version = None

    @property
    def resolved(self):
        return self._canonical_url is not None

    @property
    def canonical(self):
        """Canonical URL is the URL that should be used to access the resource.

        Canonical URL may be distinctly different from an absolute URL, including being completely different in every
        way. Obtaining canonical URL may involve lengthy I/O operations and access to remote third-party resources
        and may result in an error.
        """
        canonical_url = self._canonical_url
        if canonical_url is None:
            self._resolve()
            return self.canonical
        return canonical_url

    @property
    def absolute(self):
        """An absolute URL that was calculated based on the source and base provided.

        Absolute URL merely identifies the resource the way the user has designated it. Obtaining this URL never
        involves any I/O or accessing any resources and is a syntactical computation only. Access to stream or content
        is done through a canonical URL.
        """
        return self._absolute_url

    def stream(self):
        """Retrieves the content as a stream of the resource identified by the canonical URL"""
        return self._stream(self.canonical)

    def _stream(self, url):
        raise NotImplementedError

    def content(self):
        """Retrieves the entire content of the resource identified by the canonical URL"""
        return self._content(self.canonical)

    def _content(self, url):
        raise NotImplementedError

    def close(self):
        pass

    def _resolve(self):
        """Canonizes the URL, determines the version of the resource and """
        self._canonical_url = self._absolute_url
        self._version = ""

    @property
    def version(self):
        """Returns the uniquely identifying version of this resource.

        The version uniquely identifies this the content of this resource. For a simple file it could be a hash. For a
        file in a repository it will most like be a revision identifier.
        """
        version = self._version
        if version is None:
            self._resolve()
            return self.version
        return version

    @staticmethod
    def to_absolute(source, base=None):
        if isinstance(source, str):
            source = url(source)

        if base and isinstance(base, str):
            base = url(base)

        return base.as_abs_base(source) if base else source  # type: Url

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def __repr__(self):
        return "%s %s" % (type(self), self.__dict__)

    def __str__(self):
        return self.absolute.geturl()

    def __hash__(self):
        return hash(self.absolute)

    def __eq__(self, other):
        return type(other) == type(self) and other.absolute == self.absolute


@inherit_doc
class ContextUrlLoader(UrlLoader):
    def __new__(cls, context, source, base=None):
        loader = UrlLoader(context, source, base)
        absolute_url = loader.absolute
        provider_type = loader.context.plugin_manager.provider("karellen.stack.schema.loader", absolute_url.scheme)
        return provider_type(context, absolute_url)


# class ContextUnavailable(RuntimeError):
#    def __init__(self, *args):
#        super().__init__(*args)


class Provider(object):
    #   def __init__(self):
    #       self._context = None

    #    def capabilities(self) -> dict:
    #        """
    #        Retrieve all supported capabilities.
    #
    #       Minimally this method always returns at least `provider_capabilities`
    #      """
    #        caps = type(self).provider_capabilities()
    #       if self.has_context():
    #            caps += self.current_capabilities()
    #        return caps

    #    def current_capabilities(self) -> dict:
    #        """Capabilities that may be discoverable by the provider implementation in a particular environment
    #
    #        Requires context.
    #        """
    #        pass

    #   @classmethod
    #    def provider_capabilities(cls) -> dict:
    #        """Retrieve the minimal capabilities supported by this provider in any environment.
    #
    #        These capabilities are inherent to the implementing provider and are always present in any context.
    #        """

    @classmethod
    def config_entries(cls) -> Iterable[str]:
        """Returns the list of configuration entries that the plugin is capable of processing.

        These are designed to validate and initialize the configuration of the provider instance in a specific stack.
        """

        # @property
        #    def context(self):
        #        return self._context

        #    @context.setter
        #    def context(self, context: Context):
        #        self._context = context

        #    def has_context(self):
        #        return self._context

        #    def _assert_context_set(self):
        #        if not self.has_context():
        #            raise ContextUnavailable
