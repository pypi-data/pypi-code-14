from typing import Optional, Set

import aiohttp

from .resolver import ServiceResolver


class HTTPDispatcher:
    """
    Simple dispatcher implementation that uses HTTP to effectively proxy to
    and from remote services.

    :param service_resolver: Implementation of a service resolver used to
                             locate service urls based on names.
    :param sensitive_headers: Optional set of headers that should be
                              considered as sensitive and blocked from
                              being sent back to the caller. Defaults to
                              'Authorization' and 'Set-Cookie'
    :param buff_size: How large of a buffer (in bytes) to incrementally read
                      for streaming data from the remote service.
    """
    # TODO: define a dispatcher interface

    def __init__(self, service_resolver: ServiceResolver, *,
                 sensitive_headers: Optional[Set[str]] = None,
                 buff_size: int = 512):
        self._service_resolver = service_resolver
        self._session = aiohttp.ClientSession()
        self._sensitive_headers = sensitive_headers or {'Authorization',
                                                        'Set-Cookie'}
        self._buff_size = buff_size

    def __del__(self):
        if not self._session.closed:
            self._session.close()

    def filter_headers(self, headers):
        """
        Filter out any sensitive headers from the input iterable.
        :param headers: Iterable of header tuples. Usually this will
                        be a dict view.
        :return: List of headers to send to the caller.
        """
        return [header for header in headers
                if header[0] not in self._sensitive_headers]

    async def dispatch(self, service, path, message, payload, writer) -> None:
        """TODO: this implementation will need to change to abstract
        out a lot of the underlying asyncio transports."""
        url = await self._service_resolver.resolve(service)
        if not url:
            raise aiohttp.HttpProcessingError(code=404,
                                              message='Unable to find remote service.')  # noqa

        data = None if payload.at_eof() else payload
        full_url = url + path
        async with self._session.request(message.method, full_url,
                                         headers=message.headers, data=data) \
                as remote_response:

            response = aiohttp.Response(writer, remote_response.status,
                                        http_version=message.version)
            headers = self.filter_headers(remote_response.headers.items())
            response.add_headers(*headers)
            response.add_header('X-SERVICE-NAME', service)
            response.send_headers()
            while True:
                block = await remote_response.content.read(self._buff_size)
                if not block:
                    break
                response.write(block)
            await response.write_eof()
