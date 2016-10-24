from aiohttp import FormData, ClientSession
from chilero.web.test import WebTestCase, asynctest

import uh


class TestHTTP(WebTestCase):
    routes = uh.routes

    @asynctest
    async def test_upload(self):
        url = self.full_url(self.app.reverse('upload'))
        data = FormData()
        async with ClientSession() as session:
            with open('test_uh.py', 'rb') as f:
                data.add_field(
                    'file', f, filename='test_uh.py'
                )

                r = await session.post(url, data=data)
                assert r.headers['Location'] == '/files/test_uh.py'
                r.close()

            r2 = await session.get(self.full_url('/files/test_uh.py'))
            content = await r2.read()
            r2.close()
            assert 'class TestHTTP(WebTestCase):' in content.decode()
