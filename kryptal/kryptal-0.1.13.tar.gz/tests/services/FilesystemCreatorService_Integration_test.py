import unittest
from unittest.mock import create_autospec, Mock  #type: ignore

import os
import tempfile
from kryptal.model.Filesystems import Filesystem, Filesystems
from kryptal.pluginmanager.IFilesystem import IFilesystem
from kryptal.pluginmanager.KryptalPlugins import KryptalPlugins
from kryptal.services.FilesystemCreatorService import FilesystemCreatorService
from yapsy.PluginInfo import PluginInfo


filesystem_fixture = Filesystem(name="My name", fstype="MyFSType", ciphertextDirectory="/my/ciphertext", plaintextDirectory="/my/plaintext")
password = "mypassword".encode(encoding="UTF-8")


class test_FilesystemCreatorService_Integration(unittest.TestCase):
    def setUp(self) -> None:
        self.plugins = KryptalPlugins()
        self.mockPlugin = self._createMockPlugin()
        self._addMockPlugin(self.plugins, self.mockPlugin)
        self._stateTempDir = tempfile.TemporaryDirectory()
        self.model = Filesystems(os.path.join(self._stateTempDir.name, "filesystems.yaml"))
        self.service = FilesystemCreatorService(self.plugins, self.model)

    def tearDown(self) -> None:
        self._stateTempDir.cleanup()

    def _createMockPlugin(self) -> Mock:
        fsPluginMock = create_autospec(IFilesystem)
        fsPluginMock.name.return_value = filesystem_fixture.fstype
        return fsPluginMock

    def _addMockPlugin(self, plugins: KryptalPlugins, plugin: IFilesystem) -> None:
        fsPluginInfoMock = create_autospec(PluginInfo)
        fsPluginInfoMock.plugin_object = plugin
        fsPluginInfoMock.name.return_value = filesystem_fixture.fstype
        plugins._filesystemPlugins._manager.appendPluginToCategory(fsPluginInfoMock, "Filesystem")

    def test_adds_to_model(self) -> None:
        self.service.create(name=filesystem_fixture.name, fstype=filesystem_fixture.fstype, password=password,
                       ciphertextDirectory=filesystem_fixture.ciphertextDirectory,
                       plaintextDirectory=filesystem_fixture.plaintextDirectory)
        assert self.model.count() == 1
        assert self.model.get(0) == filesystem_fixture

    def test_creates_filesystem(self) -> None:
        self.service.create(name=filesystem_fixture.name, fstype=filesystem_fixture.fstype, password=password,
                       ciphertextDirectory=filesystem_fixture.ciphertextDirectory,
                       plaintextDirectory=filesystem_fixture.plaintextDirectory)
        self.mockPlugin.create.assert_called_once_with(ciphertextDir=filesystem_fixture.ciphertextDirectory,
                                                       plaintextDir=filesystem_fixture.plaintextDirectory,
                                                       password=password)
