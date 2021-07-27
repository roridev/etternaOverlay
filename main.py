# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import trio

from streamcompanion.channeling import consume_hit, consume_miss, consume_status
from streamcompanion.websocket import connect
from tk.frame import Frame


async def main():
    async with trio.open_nursery() as nursery:
        miss_send, miss_receive = trio.open_memory_channel(3)
        hit_send, hit_receive = trio.open_memory_channel(10)
        status_send, status_receive = trio.open_memory_channel(3)

        frame = Frame()

        nursery.start_soon(connect, hit_send, miss_send, status_send)

        nursery.start_soon(frame.read_judge, hit_receive)
        nursery.start_soon(frame.read_miss, miss_receive)
        nursery.start_soon(frame.read_reset, status_receive)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    trio.run(main)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
