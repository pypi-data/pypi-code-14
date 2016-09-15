from kryptal.model.Filesystems import Filesystem, Filesystems
from kryptal.pluginmanager.KryptalPlugins import KryptalPlugins


class FilesystemCreatorService(object):
    def __init__(self, kryptalPlugins: KryptalPlugins, filesystemModel: Filesystems) -> None:
        self._kryptalPlugins = kryptalPlugins
        self._filesystemModel = filesystemModel

    def create(self, name: str, fstype: str, ciphertextDirectory: str, plaintextDirectory: str, password: bytes) -> None:
        self._kryptalPlugins.filesystems()[fstype].create(ciphertextDir=ciphertextDirectory, plaintextDir=plaintextDirectory, password=password)
        self._filesystemModel.add(Filesystem(name=name, fstype=fstype, ciphertextDirectory=ciphertextDirectory, plaintextDirectory=plaintextDirectory))
