import tkinter
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from opsys import opsys


def par(s):
    ns = ''
    path = False

    for i in s:
        if i == "\'":
            if path:
                break
            path = True
        if path:
            ns += i

    if len(ns) == 0:
        return -1
    return ns


class Apple:
    def __init__(self, master):
        self.master = master
        self.master.fl = ''
        self.label = ttk.Label(master, text="Welcome")
        self.label.grid(row=0, column=0, columnspan=2)

        # collects route
        ttk.Button(master, text="Choose File", command=self.cf).grid(row=1, column=0)

        # drop down menu for time

    def cf(self):
        sel_str = str(filedialog.askopenfile(parent=self.master, title='Select a File to Modify'))

        # sel_str -> '/Users/...'
        self.master.fl = par(sel_str)


if opsys() == 0:
    root = Tk()
    app = Apple(root)
    root.mainloop()
