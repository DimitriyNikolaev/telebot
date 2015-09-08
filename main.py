__author__ = 'dimitriy'

import asyncio
from puller import puller
import aioredis


@asyncio.coroutine
def go():
    pool = yield from aioredis.create_pool(
        ('localhost', 6379),
        minsize=5, maxsize=10, db=1,
        loop=loop)
    with (yield from pool) as redis:    # high-level redis API instance
        yield from redis.set('my-key', 'value')
        print((yield from redis.get('my-key')))
    pool.clear()    # closing all open connections


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    # loop.run_until_complete(go())
    loop.run_until_complete(puller(loop))








