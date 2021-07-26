import json
from trio.abc import SendChannel
from trio_websocket import open_websocket_url

uri = "ws://localhost:20727/tokens"
state = 0
misses = 0

plays = 0
retries = 0
status = ""


async def send_diff(hit_channel: SendChannel, new_state: list[int]):
    global state
    delta = new_state[state:]
    state = len(new_state)

    for item in delta:
        await hit_channel.send(item)
        print(f'[hit_channel] -> Sent {item}.')


async def connect(hit_channel: SendChannel, miss_channel: SendChannel, status_channel: SendChannel):
    global state
    async with open_websocket_url(uri) as ws:
        while True:
            await ws.send_message("[\"hitErrors\",\"miss\","
                                  # Detects status change. Goes into status channel.
                                  "\"plays\",\"retries\",\"rawStatus\"]")
            _recv = await ws.get_message()
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
                    await status_channel.send('p')
            if "retries" in j:
                global retries
                if j["retries"] != retries:
                    retries = j["retries"]
                    print(f'Detected retry. Resetting state')
                    state = 0
                    await status_channel.send('r')
            if "rawStatus" in j:
                global status
                if j["rawStatus"] != status:
                    if j["rawStatus"] != 7:
                        print(f'Detected status change. Resetting state')
                        state = 0
                    status = j["rawStatus"]
                    await status_channel.send(status)
            global misses
            if "miss" in j:
                if misses != j["miss"]:
                    misses = j["miss"]
                    await miss_channel.send(misses)
                    print(f'[miss_channel] -> Sent {misses}.')
