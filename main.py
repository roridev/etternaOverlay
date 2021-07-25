# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import asyncio
from asyncio import gather

from asyncio_channel import create_channel

from streamcompanion.channeling import consume_hit, consume_miss, consume_status
from streamcompanion.websocket import connect


async def main():
    miss_ch = create_channel(3)
    hit_ch = create_channel(10)
    status_ch = create_channel(3)

    await gather(connect(hit_ch, miss_ch, status_ch), consume_hit(hit_ch), consume_miss(miss_ch),
                 consume_status(status_ch))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    asyncio.run(main())

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
