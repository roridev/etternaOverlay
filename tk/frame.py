from tkinter import *
from tkinter.ttk import *


from trio.abc import ReceiveChannel

from scoring.InTheGroove import get_acc, rate
from scoring.JUDGE import JUDGE_4


class Dump(object):
    pass


class Frame:
    def __init__(self):
        self.base = Tk()
        self.is_running = False
        self.canvas = Canvas(self.base, width=300, height=300, bg="#00ff00")
        self.state = {"MA": 0, "PF": 0, "GR": 0, "GD": 0, "BA": 0, "MISS": 0}

        self.hell_if_i_dont = StringVar(self.canvas, value="")

        window_attr = Dump()
        y_pos = 15
        style = Style()
        style.configure("BW.Label", foreground="#ffffff", background="#00ff00")
        for attr in ["last_hit", "count_ma", "count_pf", "count_gr", "count_gd", "count_ba", "count_miss", "stat_acc"]:
            setattr(self, attr, StringVar(self.canvas, value=""))
            label = Label(self.canvas, textvariable=getattr(self, attr), font=('Press Start 2P', 17, ''), style="BW.Label")

            setattr(window_attr, attr, label)
            label.pack()
            self.canvas.create_window(150, y_pos, window=getattr(window_attr, attr))
            y_pos += 25
        self.canvas.pack()

    async def read_judge(self, hit_ch: ReceiveChannel):
        async for hit in hit_ch:
            rating = rate(hit, JUDGE_4)
            self.state[rating] = self.state[rating] + 1
            self.last_hit.set(f'Last Hit : {rating}')
            self.update_labels()
            self.canvas.update()

    async def read_miss(self, miss_ch: ReceiveChannel):
        async for update in miss_ch:
            self.state["MISS"] = update
            self.update_labels()
            self.canvas.update()

    async def read_reset(self, reset_ch):
        async for reset in reset_ch:
            if reset != 7:
                self.state = {"MA": 0, "PF": 0, "GR": 0, "GD": 0, "BA": 0, "MISS": 0}
                self.update_labels()
                self.canvas.update()
            else:
                print(f'{get_acc(self.state):.2f}% [{self.state["MA"]}|{self.state["PF"]}|{self.state["GR"]}|'
                      f'{self.state["GD"]}|{self.state["BA"]}] <{self.state["MISS"]}xMISS>')

    def close(self):
        self.is_running = False

    async def run(self):
        self.is_running = True
        while self.is_running:
            self.canvas.update()

    def update_labels(self):
        self.count_ma.set(f'MA: {self.state["MA"]}')
        self.count_pf.set(f'PF: {self.state["PF"]}')
        self.count_gr.set(f'GR: {self.state["GR"]}')
        self.count_gd.set(f'PD: {self.state["GD"]}')
        self.count_ba.set(f'BA: {self.state["BA"]}')
        self.count_miss.set(f'MISS: {self.state["MISS"]}')
        self.stat_acc.set(f'Acc: {get_acc(self.state):.2f}%')



