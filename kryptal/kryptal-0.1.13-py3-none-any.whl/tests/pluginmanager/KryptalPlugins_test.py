from kryptal.pluginmanager.IFilesystem import IFilesystem
from kryptal.pluginmanager.IStorageProvider import IStorageProvider
from kryptal.pluginmanager.KryptalPlugins import KryptalPlugins
from nose.tools import assert_equals


def test_filesystems_is_array() -> None:
    assert isinstance(KryptalPlugins().filesystems(), dict)

def test_storageproviders_is_array() -> None:
    assert isinstance(KryptalPlugins().storage_providers(), dict)

def test_filesystems_not_empty() -> None:
    assert len(KryptalPlugins().filesystems()) > 0

def test_storageproviders_not_empty() -> None:
    assert len(KryptalPlugins().storage_providers()) > 0

def test_filesystems_valid() -> None:
    for name, fs in KryptalPlugins().filesystems().items():
        assert isinstance(fs, IFilesystem)

def test_storageproviders_valid() -> None:
    for name, fs in KryptalPlugins().storage_providers().items():
        assert isinstance(fs, IStorageProvider)

def test_filesystems_has_cryfs() -> None:
    names = [name for name, fs in KryptalPlugins().filesystems().items()]
    assert names.count("CryFS") == 1

def test_storageproviders_has_localstorage() -> None:
    names = [name for name, sp in KryptalPlugins().storage_providers().items()]
    assert names.count("LocalFolder") == 1

def test_filesystems_names_correct() -> None:
    for name, fs in KryptalPlugins().filesystems().items():
        assert_equals(name, fs.name())

def test_storageproviders_names_correct() -> None:
    for name, sp in KryptalPlugins().storage_providers().items():
        assert_equals(name, sp.name())
