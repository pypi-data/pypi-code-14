from asyncio import Lock
from threading import Timer


class RateLimiter():

    def __init__(self, *, requests_per_minute):
        self.requests      = 0
        self.limit         = requests_per_minute
        self.requests_lock = Lock()
        self.limit_lock    = Lock()

    async def __aenter__(self):
        with await self.requests_lock:
            self.requests += 1
            hit_limit     = self.requests >= self.limit

        if hit_limit:
            await self.limit_lock.acquire()

    async def __aexit__(self, exc_type, exc, tb):
        Timer(60.0, self.remove_request).start()

    async def remove_request(self):
        with await self.requests_lock:
            self.requests -= 1
            self.limit_lock.release()
