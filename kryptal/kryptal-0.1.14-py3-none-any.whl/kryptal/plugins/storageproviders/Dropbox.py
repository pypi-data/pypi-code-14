from kryptal.pluginmanager import IStorageProvider


class Dropbox(IStorageProvider.IStorageProvider):
    def name(self) -> str:
        return "Dropbox"
