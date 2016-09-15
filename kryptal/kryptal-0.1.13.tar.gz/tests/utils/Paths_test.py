from kryptal.utils import Paths


def test_plugin_paths_not_empty() -> None:
    assert len(Paths.plugin_paths()) > 0

def test_plugin_paths_are_strings() -> None:
    for path in Paths.plugin_paths():
        assert isinstance(path, str)

def test_plugin_paths_filesystems_not_empty() -> None:
    assert len(Paths.plugin_paths_filesystems()) > 0

def test_plugin_paths_filesystems_are_strings() -> None:
    for path in Paths.plugin_paths_filesystems():
        assert isinstance(path, str)

def test_plugin_paths_storageproviders_not_empty() -> None:
    assert len(Paths.plugin_paths_storageproviders()) > 0

def test_plugin_paths_storageproviders_are_strings() -> None:
    for path in Paths.plugin_paths_storageproviders():
        assert isinstance(path, str)
