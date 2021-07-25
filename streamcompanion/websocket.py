
import websockets
import json
from asyncio_channel._channel import Channel


uri = "ws://localhost:20727/tokens"
state = 0
misses = 0

plays = 0
retries = 0
status = ""


async def send_diff(hit_channel: Channel, new_state: list[int]):
    global state
    delta = new_state[state:]
    state = len(new_state)

    for item in delta:
        if await hit_channel.put(item):
            print(f'[hit_channel] -> Sent {item}.')
        else:
            print(f'[hit_channel] -\\> Blocked {item}.')


async def connect(hit_channel: Channel, miss_channel: Channel, status_channel: Channel):
    global state
    async with websockets.connect(uri) as ws:
        while True:
            await ws.send("[\"hitErrors\",\"miss\","
                          # Detects status change. Goes into status channel.
                          "\"plays\",\"retries\",\"rawStatus\"]")
            _recv = await ws.recv()
            j = json.loads(_recv)
            if "hitErrors" in j:
                if len(j["hitErrors"]) != state:
                    await send_diff(hit_channel, j["hitErrors"])
            if "plays" in j:
                global plays
                if j["plays"] != plays:
                    plays = j["plays"]
                    print(f'Detected new play. Resetting state')
                    state = 0
                    await status_channel.put('p')
            if "retries" in j:
                global retries
                if j["retries"] != retries:
                    retries = j["retries"]
                    print(f'Detected retry. Resetting state')
                    state = 0
                    await status_channel.put('r')
            if "rawStatus" in j:
                global status
                if j["rawStatus"] != status:
                    if j["rawStatus"] != 7:
                        print(f'Detected status change. Resetting state')
                        state = 0
                    status = j["rawStatus"]
                    await status_channel.put(status)
            global misses
            if "miss" in j:
                if misses != j["miss"]:
                    misses = j["miss"]
                    if await miss_channel.put(misses):
                        print(f'[miss_channel] -> Sent {misses}.')
                    else:
                        print(f'[miss_channel] -\\> Blocked {misses}.')
