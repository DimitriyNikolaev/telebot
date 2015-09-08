__author__ = 'dimitriy'

import asyncio
import aiohttp
import settings
import ujson as json


@asyncio.coroutine
def get_updates(conn):
    r = yield from aiohttp.request('GET', settings.URL+'getUpdates', connector=conn)
    body = yield from r.json()
    return body


@asyncio.coroutine
def send_reply(ses, responses):
    for response in responses:
        r = yield from ses.post(settings.URL+response['method'], data=response['msg'])
        p = yield from r.read()
        print(p)
    return


@asyncio.coroutine
def redirect_to_local(conn, mes):
    data = json.dumps(mes)
    r = yield from aiohttp.request('POST', "http://127.0.0.1:8888/",
                                   data=data,
                                   headers={'content-type': 'application/json'},
                                   connector=conn)
    return r
