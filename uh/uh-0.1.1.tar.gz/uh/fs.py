import os

import aiohttp.web

from .base import BaseUploader


UPLOAD_PATH = os.getenv('UPLOAD_PATH', '/tmp/')


class Uploader(BaseUploader):

    async def file_ready(self):
        filename = await self.get_filename()
        filepath = os.path.join(UPLOAD_PATH, filename)

        with open(filepath, 'wb') as f:
            while True:
                chunk = await self.file.read_chunk()
                if not chunk:
                    break

                f.write(chunk)

    async def serve(self, filename):
        filepath = os.path.join(UPLOAD_PATH, filename)
        with open(filepath, 'rb') as f:
            return aiohttp.web.Response(
                body=f.read()
            )
