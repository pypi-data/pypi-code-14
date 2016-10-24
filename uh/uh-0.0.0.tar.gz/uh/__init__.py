import os
from importlib import import_module

import chilero

ENDPOINT = os.getenv('ENDPOINT', 'files')
Uploader = import_module(
    os.getenv('UPLOADER', 'uh.fs')
).Uploader


class UploadHandler(chilero.web.View):

    async def post(self):
        return await Uploader(self.request).upload()


class FileHandler(chilero.web.View):
    async def get(self, filename):
        return await Uploader(self.request).serve(filename)


routes = [
    ['/{}'.format(ENDPOINT), UploadHandler, 'upload'],
    ['/{}/{{filename}}'.format(ENDPOINT), FileHandler, 'file'],
]


def main():
    chilero.web.run(
        chilero.web.Application,
        routes=routes
    )


if __name__ == '__main__':
    main()
