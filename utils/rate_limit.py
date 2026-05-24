import asyncio

class AsyncRateLimiter:
    def __init__(self, limit: int):
        self.semaphore = asyncio.Semaphore(limit)

    async def __aenter__(self):
        await self.semaphore.acquire()

    async def __aexit__(self, exc_type, exc, tb):
        self.semaphore.release()