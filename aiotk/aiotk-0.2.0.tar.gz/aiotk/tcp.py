# -*- coding: utf-8 -*-


import asyncio


class TCPServer(object):
    """Asynchronous context manager to accept TCP connections.

    This context manager provides the following features over direct use of
    ``asyncio.start_server()``:

    - connection handlers are coroutines
    - prevent leaking connections when the writer is not properly closed by the
      connection handler
    - automatically cancel all tasks that handle connections when it's time to
      shut down
    - wait until all connections are closed before shutting down the server
      application (includes handling of a rare race condition)

    :param host: Network interface on which to listen for incoming connections.
    :param port: Port number on which to listen for incoming connections.
    :param callback: Coroutine function that will be used to spawn a task for
     each established connection.  This coroutine must accept two positional
     arguments: ``(reader, writer)`` which allow interaction with the peer.
    :param loop: Event loop in which to run the server's asynchronous tasks.
     When ``None``, the current default event loop will be used.

    .. versionadded: 0.2

    """

    def __init__(self, host, port, callback, loop=None):
        self._callback = callback
        self._host = host
        self._port = port
        self._loop = loop or asyncio.get_event_loop()
        self._sessions = set()
        self._server = None

    @property
    def host(self):
        """Network interface on which the server listens for connections.

        See:

        - :py:data:`aiotk.TCPServer.port`
        """
        return self._host

    @property
    def port(self):
        """Port number on which the server listens for connections.

        See:

        - :py:data:`aiotk.TCPServer.host`
        """
        return self._port

    async def __aenter__(self):
        self.start()
        await self.wait_started()
        return self

    async def __aexit__(self, *args):
        self.close()
        await self.wait_closed()

    def start(self):
        """Start accepting connections.

        Only use this method if you are not using the server as an asynchronous
        context manager.

        See:

        - :py:meth:`aiotk.TCPServer.wait_started`
        - :py:meth:`aiotk.TCPServer.close`
        """
        if self._server:
            raise Exception('Already running.')
        self._server = self._loop.create_task(asyncio.start_server(
            self._client_connected, host=self._host, port=self._port,
        ))

    # NOTE: start is synchronous, so we can't await in there.
    async def wait_started(self):
        """Wait until the server is ready to accept connections.

        See:

        - :py:meth:`aiotk.TCPServer.start`
        - :py:meth:`aiotk.TCPServer.close`
        """
        if not self._server:
            raise Exception('Not started.')
        if isinstance(self._server, asyncio.Future):
            self._server = await self._server

    # NOTE: cancel pending sessions immediately.
    #
    # TODO: make cancelling session optionnal (graceful shutdown).
    def close(self):
        """Stop accepting connections.

        .. note::

           Since connections may still be pending in the kernel's TCP stack at
           the time where you call this, it's possible that new connections
           seem to get established after you signal your intent to stop
           accepting connections.

        See:

        - :py:meth:`aiotk.TCPServer.wait_started`
        - :py:meth:`aiotk.TCPServer.wait_closed`

        """
        if not self._server:
            return
        if isinstance(self._server, asyncio.Future):
            raise Exception('Starting.')
        self._server.close()
        for session in self._sessions:
            session.cancel()

    # NOTES:
    # - caller can retry if they hit the timeout;
    # - not clear if we can still accept connections until
    #   ```self._server.wait_closed()` completes, so we cancel again after it
    #   does.
    async def wait_closed(self, timeout=None):
        """Wait until all connections are closed.

        See:

        - :py:meth:`aiotk.TCPServer.wait_started`
        - :py:meth:`aiotk.TCPServer.wait_closed`
        """

        if not self._server:
            return
        await self._server.wait_closed()
        for session in self._sessions:
            session.cancel()
        pending = self._sessions
        if pending:
            _, pending = await asyncio.wait(
                pending,
                return_when=asyncio.ALL_COMPLETED,
                timeout=timeout,
            )
        if pending:
            raise asyncio.TimeoutError()
        assert not self._sessions

    # NOTE: not closing writer here leaks connection.
    async def _client_wrapper(self, reader, writer):
        try:
            return await self._callback(
                reader=reader, writer=writer,
            )
        except asyncio.CancelledError:
            pass
        finally:
            writer.close()

    # NOTE: exception here leaks connection.
    def _client_connected(self, reader, writer):
        s = self._loop.create_task(
            self._client_wrapper(reader, writer)
        )
        s.add_done_callback(self._sessions.remove)
        self._sessions.add(s)
