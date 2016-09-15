import unittest
from typing import Any, Dict
import os
import tempfile
from kryptal.model.ConfigFileRef import ConfigFileRef
from nose.tools import assert_equals


class test_ConfigFileRef(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.path = os.path.join(self.tempdir.name, "my-test.file")

    def tearDown(self) -> None:
        self.tempdir.cleanup()

    def save(self, data: Dict[str, Any]) -> None:
        ConfigFileRef(self.path).save(data)

    def load(self) -> Dict[str, Any]:
        return ConfigFileRef(self.path).load()

    def assert_save_and_load_correct(self, data: Dict[str, Any]) -> None:
        self.save(data)
        assert_equals(data, self.load())

    def test_empty(self) -> None:
        self.assert_save_and_load_correct({})

    def test_structure(self) -> None:
        self.assert_save_and_load_correct({
            'key1': [1, 2, '5'],
            'key2': {
                'subkey1': 7,
                'subkey2': 3.5
            },
            'key3': [
                {'subkey3': 4, 'subkey4': 5},
                {'subkey7': [2, 3], 'subkey8': {'a': 'b'}},
                {'subkey9': [4, 5, {'subkey10': {'a': 'b'}}]},
                {'subkey5': 6, 'subkey6': '6'}
            ]
        })


    def test_umlauts(self) -> None:
        self.assert_save_and_load_correct({
            'käse': 'Spaß'
        })
