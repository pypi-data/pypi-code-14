from aiohttp.web_exceptions import HTTPNoContent


class BaseUploader(object):
    def __init__(self, request):
        self.request = request
        self.file = None

    async def get_filename(self):
        return self.file.filename

    async def get_file_url(self):
        return self.request.app.reverse(
            'file', filename=await self.get_filename()
        )

    async def before_upload(self):
        pass

    async def file_ready(self):
        raise NotImplementedError()

    async def upload(self):
        await self.before_upload()
        reader = await self.request.multipart()
        self.file = await reader.next()
        await self.file_ready()

        return HTTPNoContent(
            headers=(
                ('Location', await self.get_file_url()),
            )
        )

    async def serve(self, filename):
        raise NotImplementedError()
