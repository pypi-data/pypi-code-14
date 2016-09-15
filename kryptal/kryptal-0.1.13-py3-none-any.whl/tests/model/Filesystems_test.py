import unittest
from unittest.mock import Mock #type: ignore

import os
import tempfile
from kryptal.model.Filesystems import Filesystems, Filesystem
from nose.tools import assert_equals

filesystem_fixture1 = Filesystem(name="My name 1", fstype="MyFSType1", ciphertextDirectory="/my/ciphertext/1", plaintextDirectory="/my/plaintext/1")
filesystem_fixture2 = Filesystem(name="My name 2", fstype="MyFSType2", ciphertextDirectory="/my/ciphertext/2", plaintextDirectory="/my/plaintext/2")


class test_Filesystems(unittest.TestCase):
    def setUp(self) -> None:
        self._stateTempDir = tempfile.TemporaryDirectory()
        self.model = Filesystems(os.path.join(self._stateTempDir.name, "filesystems.yaml"))

    def tearDown(self) -> None:
        self._stateTempDir.cleanup()

    def test_count_empty(self) -> None:
        assert_equals(0, self.model.count())

    def test_count_one(self) -> None:
        self.model.add(filesystem_fixture1)
        assert_equals(1, self.model.count())

    def test_count_two(self) -> None:
        self.model.add(filesystem_fixture1)
        self.model.add(filesystem_fixture2)
        assert_equals(2, self.model.count())

    def test_get_one(self) -> None:
        self.model.add(filesystem_fixture1)
        assert_equals(filesystem_fixture1, self.model.get(0))

    def test_get_two(self) -> None:
        self.model.add(filesystem_fixture1)
        self.model.add(filesystem_fixture2)
        assert_equals(filesystem_fixture1, self.model.get(0))
        assert_equals(filesystem_fixture2, self.model.get(1))

    def test_change_handler(self) -> None:
        handler = Mock()
        self.model.addChangeHandler(handler)
        self.model.add(filesystem_fixture1)
        handler.assert_called_once_with()

    def test_multiple_change_handler(self) -> None:
        handler1 = Mock()
        handler2 = Mock()
        self.model.addChangeHandler(handler1)
        self.model.addChangeHandler(handler2)
        self.model.add(filesystem_fixture1)
        handler1.assert_called_once_with()
        handler2.assert_called_once_with()


class test_FilesystemsIO(unittest.TestCase):
    def setUp(self) -> None:
        self._stateTempDir = tempfile.TemporaryDirectory()
        self.path = os.path.join(self._stateTempDir.name, "filesystems.yaml")

    def tearDown(self) -> None:
        self._stateTempDir.cleanup()

    def test_save_and_load_empty(self) -> None:
        Filesystems(self.path)
        obj2 = Filesystems(self.path)
        assert_equals(0, obj2.count())

    def test_save_and_load_one(self) -> None:
        obj = Filesystems(self.path)
        obj.add(filesystem_fixture1)
        obj2 = Filesystems(self.path)
        assert_equals(1, obj2.count())
        assert_equals(filesystem_fixture1, obj2.get(0))

    def test_save_and_load_two(self) -> None:
        obj = Filesystems(self.path)
        obj.add(filesystem_fixture1)
        obj.add(filesystem_fixture2)
        obj2 = Filesystems(self.path)
        assert_equals(2, obj2.count())
        assert_equals(filesystem_fixture1, obj2.get(0))
        assert_equals(filesystem_fixture2, obj2.get(1))
