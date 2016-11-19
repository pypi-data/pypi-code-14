from os import path, mkdir, listdir
from .values import DATA_DIR
import ujson
import asyncio
PsuedoDB_DIR = path.join(DATA_DIR, 'pseudodb')
class PsuedoDB:
    def __init__(self, DB, loop=None):
        self.__data = {}
        if DB == ':memory:':
            self.__dir = None
        else:
            self.__dir = path.join(PsuedoDB_DIR, DB)
            if not path.join(self.__dir):
                mkdir(self.__dir)
        self.__load()
        self.lock = asyncio.lock()
        self.loop = loop or asyncio.get_event_loop()
        self.__modified = []

    def __load_json(table, entry):
        with open(path.join(self.__dir, table, entry)) as f:
            return ujson.load(f)

    def __load(self):
        for _dir in listdir(self.__dir):
            self.__data[_dir] = {}
            try:
                for _nfile in listdir(path.join(self.__dir, _dir)):
                    self.__data[_dir][_nfile] = self.__load_json(_dir, _nfile)
            except:
                pass

    def __save(self):
        for k,v in self.__dir.items():
            t = v.keys()
            p = path.join(self.__dir, k)
            if not path.exists(p):
                mkdir(p)
            for _nfile in t:
                with open(path.join(p, _nfile), 'w') as f:
                    ujson.dump(self.__data, f)

    async def load(self):
        with await self.lock:
            await loop.run_in_executor(None, self.__load)

    async def save(self):
        with await self.lock:
            await self.loop.run_in_executor(None, self.__save)
