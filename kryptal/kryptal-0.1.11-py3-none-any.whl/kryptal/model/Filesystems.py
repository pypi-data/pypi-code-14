from typing import List, Callable

from kryptal.model.Filesystem import Filesystem
from kryptal.model.FilesystemStateFileRef import FilesystemsStateFileRef


class Filesystems(object):
    def __init__(self, stateFilePath: str) -> None:
        self._stateFile = FilesystemsStateFileRef(stateFilePath)
        self._filesystems = self._stateFile.load()
        self._changeHandlers = [] #type: List[Callable[[], None]]
        self.addChangeHandler(self._saveState)

    def add(self, filesystem: Filesystem) -> None:
        self._filesystems.append(filesystem)
        self._callChangeHandlers()

    def count(self) -> int:
        return len(self._filesystems)

    def get(self, index: int) -> Filesystem:
        return self._filesystems[index]

    def _callChangeHandlers(self) -> None:
        for handler in self._changeHandlers:
            handler()

    def addChangeHandler(self, changeHandler: Callable[[], None]) -> None:
        self._changeHandlers.append(changeHandler)

    def _saveState(self) -> None:
        self._stateFile.save(self._filesystems)
