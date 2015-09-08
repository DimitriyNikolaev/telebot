__author__ = 'dimitriy'

import aiohttp
import asyncio
import time
import api


def get_new_connector(loop):
    return aiohttp.TCPConnector(verify_ssl=False, loop=loop)


def puller(loop):
    connector = get_new_connector(loop)
    req_count_per_connection = 0
    while True:
            try:
                if req_count_per_connection == 1:
                    connector = get_new_connector(loop)
                raw = yield from api.get_updates(connector)
                req_count_per_connection += 1
                if raw.get('ok'):
                    local_connector = aiohttp.TCPConnector(verify_ssl=False, loop=loop)
                    # for message in raw["result"]:
                    #     last = int(message["update_id"])
                    res = yield from api.redirect_to_local(local_connector, raw)
            except Exception as x:
                connector = get_new_connector(loop)
            yield from asyncio.sleep(30)
