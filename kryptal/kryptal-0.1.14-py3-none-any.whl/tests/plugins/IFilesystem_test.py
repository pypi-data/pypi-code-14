from kryptal.pluginmanager.IFilesystem import IFilesystem
from kryptal.pluginmanager.KryptalPlugins import KryptalPlugins
from nose_parameterized import parameterized, param #type: ignore


_filesystems = [param(fs) for name, fs in KryptalPlugins().filesystems().items()]

@parameterized(_filesystems)
def test_has_name(filesystem: IFilesystem) -> None:
    isinstance(filesystem.name(), str)
