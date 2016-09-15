import unittest
from typing import List

import os
import tempfile
from kryptal.model.Filesystem import Filesystem
from kryptal.model.FilesystemStateFileRef import FilesystemsStateFileRef
from nose.tools import assert_equals


filesystem_fixture1 = Filesystem(name="My name 1", fstype="MyFSType1", ciphertextDirectory="/my/ciphertext/1", plaintextDirectory="/my/plaintext/1")
filesystem_fixture2 = Filesystem(name="My name 2", fstype="MyFSType2", ciphertextDirectory="/my/ciphertext/2", plaintextDirectory="/my/plaintext/2")

class test_FilesystemsStateFile(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.path = os.path.join(self.tempdir.name, "my-test.file")

    def tearDown(self) -> None:
        self.tempdir.cleanup()

    def save(self, data: List[Filesystem]) -> None:
        FilesystemsStateFileRef(self.path).save(data)

    def load(self) -> List[Filesystem]:
        return FilesystemsStateFileRef(self.path).load()

    def assert_save_and_load_correct(self, filesystems: List[Filesystem]) -> None:
        self.save(filesystems)
        assert_equals(filesystems, self.load())

    def test_notexisting(self) -> None:
        assert_equals([], FilesystemsStateFileRef(os.path.join(self.tempdir.name, "notexisting")).load())

    def test_empty(self) -> None:
        self.assert_save_and_load_correct([])

    def test_one(self) -> None:
        self.assert_save_and_load_correct([filesystem_fixture1])

    def test_two(self) -> None:
        self.assert_save_and_load_correct([filesystem_fixture1, filesystem_fixture2])
