from trio.abc import ReceiveChannel

from scoring.InTheGroove import rate, get_acc
from scoring.JUDGE import JUDGE_4

state = {"MA": 0, "PF": 0, "GR": 0, "GD": 0, "BA": 0, "MISS": 0}


async def consume_hit(hit_ch: ReceiveChannel):
    global state
    async for hit in hit_ch:
        rating = rate(hit, JUDGE_4)
        state[rating] = state[rating] + 1
        acc = get_acc(state)
        print(f'[hit_ch] ({rating}) {hit} @ {acc:.2f}% <- Received '
              f'[{state["MA"]}|{state["PF"]}|{state["GR"]}|{state["GD"]}|{state["BA"]}] <{state["MISS"]}>')


async def consume_miss(miss_ch: ReceiveChannel):
    global state
    async for miss in miss_ch:
        if miss == 0:
            print(f'[miss_ch] Received reset signal.')
            state["miss"] = 0
        else:
            print(f'[miss_ch] {miss} <- Received')
            state["MISS"] = miss


async def consume_status(status_ch: ReceiveChannel):
    global state
    async for change in status_ch:
        if change == 7:
            print(f'[status_ch] Manual bypass for result screen. You\'d want to compare stuff lel.')
        else:
            state = {"MA": 0, "PF": 0, "GR": 0, "GD": 0, "BA": 0, "MISS": 0}
            if change == 'r':
                print(f'[status_ch] Detected a retry. Resetting the global state.')
            elif change == 'p':
                print(f'[status_ch] Detected a new play. Resetting the global state.')
            else:
                print(f'[status_ch] Detected a status change ({change}). Resetting the global state.')