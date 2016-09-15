import subprocess
from kryptal.pluginmanager import IFilesystem
from kryptal.pluginmanager.IFilesystem import FilesystemCreateException


class CryFS(IFilesystem.IFilesystem):
    def name(self) -> str:
        return "CryFS"

    def create(self, ciphertextDir: str, plaintextDir: str, password: bytes) -> None:
        try:
            subprocess.run(["cryfs", ciphertextDir, plaintextDir], input=password, stderr=subprocess.PIPE, check=True, env={
                "CRYFS_FRONTEND": "noninteractive",
                "CRYFS_NO_UPDATE_CHECK": "true"
            })
        except subprocess.CalledProcessError as e:
            raise FilesystemCreateException(e.stderr.decode(encoding="UTF-8"))
