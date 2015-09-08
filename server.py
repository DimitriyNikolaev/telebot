__author__ = 'dimitriy'

from aiohttp import web, ClientSession, TCPConnector
import asyncio
from telebot import TeleBot
from api import send_reply
import settings


@asyncio.coroutine
def hello(request):
    data = yield from request.json()
    if data.get('ok'):
        session = ClientSession(connector=TCPConnector(verify_ssl=False, loop=eloop))
        replies = set()
        for update in data.get('result'):
            replies.add(asyncio.async(process_message(session, update), loop=eloop))
        done = yield from asyncio.wait(replies, loop=eloop, return_when=asyncio.ALL_COMPLETED)
    return web.Response(body=b"Ok")


@asyncio.coroutine
def process_message(session, update):
    bot = TeleBot(eloop, **update)
    response = yield from bot.get_response()
    r = yield from send_reply(session, response)
    return r


@asyncio.coroutine
def init(loop):
    app = web.Application(loop=loop)
    app.router.add_route('POST', '/', hello)
    srv = yield from loop.create_server(app.make_handler(), '127.0.0.1', 8888)
    return srv

eloop = asyncio.get_event_loop()
res = eloop.run_until_complete(init(eloop))
try:
    eloop.run_forever()
except KeyboardInterrupt:
    pass
