import json
from trio.abc import SendChannel
from trio_websocket import open_websocket_url

from actor.main_actor import MainActor

uri = "ws://localhost:20727/tokens"


async def connect(hit_channel: SendChannel, miss_channel: SendChannel, status_channel: SendChannel):
    async with open_websocket_url(uri) as ws:
        actor = MainActor(ws, hit_channel, miss_channel, status_channel)
        await actor.run()
