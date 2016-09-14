from kryptal.pluginmanager.IStorageProvider import IStorageProvider
from kryptal.pluginmanager.KryptalPlugins import KryptalPlugins
from nose_parameterized import parameterized, param #type: ignore


_storageproviders = [param(sp) for name, sp in KryptalPlugins().storage_providers().items()]

@parameterized(_storageproviders)
def test_has_name(storageprovider: IStorageProvider) -> None:
    isinstance(storageprovider.name(), str)
