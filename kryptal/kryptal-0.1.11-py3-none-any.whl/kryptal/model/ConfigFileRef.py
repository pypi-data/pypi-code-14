from typing import Dict, Any
import yaml #type: ignore


class ConfigFileRef(object):
    def __init__(self, path: str) -> None:
        self._path = path

    def load(self) -> Dict[str, Any]:
        stream = open(self._path, 'r')
        return yaml.safe_load(stream)

    def save(self, data: Dict[str, Any]) -> None:
        stream = open(self._path, 'w')
        yaml.safe_dump(data, stream, default_flow_style=False)
