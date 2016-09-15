from typing import List, Any, Dict

from kryptal.model.ConfigFileRef import ConfigFileRef
from kryptal.model.Filesystem import Filesystem


class FilesystemsStateFileRef(object):
    def __init__(self, path: str) -> None:
        self._file = ConfigFileRef(path)

    def save(self, filesystems: List[Filesystem]) -> None:
        self._file.save({
            'filesystems': [self._serializeFilesystem(fs) for fs in filesystems]
        })

    def load(self) -> List[Filesystem]:
        try:
            fileobj = self._file.load()
            return [self._deserializeFilesystem(fs) for fs in fileobj['filesystems']]
        except FileNotFoundError:
            return []

    def _serializeFilesystem(self, fs: Filesystem) -> Dict[str, Any]:
        return {
            'name': fs.name,
            'fstype': fs.fstype,
            'ciphertextDirectory': fs.ciphertextDirectory,
            'plaintextDirectory': fs.plaintextDirectory
        }

    def _deserializeFilesystem(self, serialized: Dict[str, Any]) -> Filesystem:
        return Filesystem(
            name=serialized['name'],
            fstype=serialized['fstype'],
            ciphertextDirectory=serialized['ciphertextDirectory'],
            plaintextDirectory=serialized['plaintextDirectory']
        )
