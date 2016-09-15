from typing import List, Dict, Generic, TypeVar, Type, cast

from yapsy.IPlugin import IPlugin
from yapsy.PluginFileLocator import PluginFileLocator
from yapsy.PluginManager import PluginManager

from kryptal.pluginmanager.IFilesystem import IFilesystem
from kryptal.pluginmanager.IStorageProvider import IStorageProvider
from kryptal.utils import Paths


class KryptalPlugins(object):
    def __init__(self) -> None:
        self._filesystemPlugins = _FilesystemPlugins()
        self._storageProviderPlugins = _StorageProviderPlugins()

    def filesystems(self) -> Dict[str, IFilesystem]:
        return self._filesystemPlugins.all()

    def storage_providers(self) -> Dict[str, IStorageProvider]:
        return self._storageProviderPlugins.all()


PluginType = TypeVar('PluginType', bound=IPlugin)
class _PluginManagerBase(Generic[PluginType]):
    def __init__(self, directories: List[str], categories: Dict[str, Type[PluginType]]) -> None:
        locator = PluginFileLocator()
        locator.setPluginInfoExtension("kryptal-plugin")
        locator.setPluginPlaces(directories)
        self._manager = PluginManager()
        self._manager.setCategoriesFilter(categories)
        self._manager.setPluginLocator(locator)

    def list_all(self) -> List[PluginType]:
        self._manager.collectPlugins()
        return [cast(PluginType, p.plugin_object) for p in self._manager.getAllPlugins()]


class _FilesystemPlugins(_PluginManagerBase[IFilesystem]):
    def __init__(self) -> None:
        super(_FilesystemPlugins, self).__init__(Paths.plugin_paths_filesystems(), {"Filesystem": IFilesystem})

    def all(self) -> Dict[str, IFilesystem]:
        return {p.name(): p for p in self.list_all()}


class _StorageProviderPlugins(_PluginManagerBase[IStorageProvider]):
    def __init__(self) -> None:
        super(_StorageProviderPlugins, self).__init__(Paths.plugin_paths_storageproviders(), {"StorageProvider": IStorageProvider})

    def all(self) -> Dict[str, IStorageProvider]:
        return {p.name(): p for p in self.list_all()}
