from trio.abc import SendChannel
from trio_websocket import WebSocketConnection

import json


def exist_and_state_changed(json_data, key, state):
    if key in json_data and state != json_data[key]:
        return True
    return False


def exist_and_state_changed_map(json_data, key, state, func):
    if key in json_data and state != func(json_data[key]):
        return True
    return False


class MainActor:
    def __init__(self, ws: WebSocketConnection, hit_ch: SendChannel, miss_ch: SendChannel, status_ch: SendChannel):
        self.hit_ch = hit_ch
        self.miss_ch = miss_ch
        self.status_ch = status_ch
        self.ws = ws

        self.is_running = False
        self.hit_error_count = 0
        self.game_state = 0
        self.play_count = 0
        self.retry_count = 0
        self.miss_count = 0

    async def run(self):
        self.is_running = True
        async with self.ws:
            while self.is_running:
                await self.ws.send_message("[\"hitErrors\",\"miss\","
                                           # Detects status change. Goes into status channel.
                                           "\"plays\",\"retries\",\"rawStatus\"]")
                data = await self.ws.get_message()
                json_data = json.loads(data)

                if exist_and_state_changed_map(json_data, "hitErrors", self.hit_error_count, len):
                    for hit in json_data["hitErrors"][self.hit_error_count:]:
                        await self.hit_ch.send(hit)
                    self.hit_error_count = len(json_data["hitErrors"])

                if exist_and_state_changed(json_data, "miss", self.miss_count):
                    await self.miss_ch.send(json_data["miss"])
                    self.miss_count = json_data["miss"]

                if exist_and_state_changed(json_data, "plays", self.play_count):
                    await self.status_ch.send('p')
                    self.play_count = json_data["plays"]

                if exist_and_state_changed(json_data, "retries", self.retry_count):
                    await self.status_ch.send('r')
                    self.retry_count = json_data["retries"]

                if exist_and_state_changed(json_data, "rawStatus", self.game_state):
                    await self.status_ch.send(json_data["rawStatus"])
                    self.game_state = json_data["rawStatus"]

    def close(self):
        self.is_running = False

    def reset_state(self):
        self.hit_error_count = 0
        self.game_state = 0
        self.play_count = 0
        self.retry_count = 0
        self.miss_count = 0
