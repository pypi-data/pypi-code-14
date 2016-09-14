from unittest.mock import create_autospec  #type: ignore

from kryptal.model.Filesystems import Filesystem, Filesystems
from kryptal.pluginmanager.KryptalPlugins import KryptalPlugins
from kryptal.services.FilesystemCreatorService import FilesystemCreatorService


filesystem_fixture = Filesystem(name="My name", fstype="MyFSType", ciphertextDirectory="/my/ciphertext", plaintextDirectory="/my/plaintext")
password = "mypassword".encode(encoding="UTF-8")

def test_adds_to_model() -> None:
    plugins = create_autospec(KryptalPlugins)
    model = create_autospec(Filesystems)
    service = FilesystemCreatorService(plugins, model)
    service.create(name=filesystem_fixture.name, fstype=filesystem_fixture.fstype, password=password,
                   ciphertextDirectory=filesystem_fixture.ciphertextDirectory,
                   plaintextDirectory=filesystem_fixture.plaintextDirectory)
    model.add.assert_called_once_with(filesystem_fixture)

def test_creates_filesystem() -> None:
    plugins = create_autospec(KryptalPlugins)
    model = create_autospec(Filesystems)
    service = FilesystemCreatorService(plugins, model)
    service.create(name=filesystem_fixture.name, fstype=filesystem_fixture.fstype, password=password,
                   ciphertextDirectory=filesystem_fixture.ciphertextDirectory,
                   plaintextDirectory=filesystem_fixture.plaintextDirectory)
    plugins.filesystems()[filesystem_fixture.fstype].create.assert_called_once_with(
        ciphertextDir=filesystem_fixture.ciphertextDirectory, plaintextDir=filesystem_fixture.plaintextDirectory, password=password)
