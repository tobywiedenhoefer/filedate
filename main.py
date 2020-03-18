import os.path
import time
from datetime import datetime
from tkinter import *
from tkinter import filedialog
from tkinter import ttk

from modfile import mod
from opsys import opsys


# for apple
def par(s):
    ns = ''
    path = False

    for i in s:
        if i == "\'":
            if path:
                break
            path = True
        elif path:
            ns += i

    if len(ns) == 0:
        return -1
    return ns


def cb(s, e):
    l = [i for i in range(s, e, -1)]
    l.insert(0, "Do not modify")
    return l


def switch_months(m):
    months = ["Jan", "Feb", "Mar", "Apr", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    for i, j in enumerate(months):
        if j == m:
            return i + 1
    return 0


def rem_excess(l):
    if len(l) == 5:
        return l
    tmpl = []
    for i in l:
        if len(i) > 0:
            tmpl.append(i)
    return tmpl


def too_far_ahead(y, mo, d, h, mi):
    now = datetime.now()
    ny = int(now.year)
    nmo = int(now.month)
    nd = int(now.day)
    nh = int(now.hour)
    nmi = int(now.minute)
    # self.year.get() set up such that year never greater than now.year
    if (y == ny) and (mo == nmo) and (d == nd) and (h == nh) and (mi >= nmi):
        return True
    elif (y == ny) and (mo == nmo) and (d == nd) and ((h >= nh) or (mi >= nmi)):
        return True
    elif (y == ny) and (mo == nmo) and ((d >= nd) or (h >= nh) or (mi >= nmi)):
        return True
    elif (y == ny) and ((mo >= nmo) or (d >= nd) or (h >= nh) or (mi >= nmi)):
        return True
    # year cannot be greater than now.year by design.
    else:
        return False


def check_dates(y, mo, d):  # returns whether a date is possible
    valid = True
    try:
        datetime(y, mo, d)
    except:
        valid = False
    return valid


class Apple:
    def __init__(self, master):
        self.master = master
        self.master.fl = None
        self.label = ttk.Label(master, text="Welcome")
        self.label.grid(row=0, column=0, columnspan=2)

        # collects route
        ttk.Button(master, text="Choose a File", command=self.cf).grid(row=1, column=0)

        now = datetime.now()
        # time variables
        self.year = StringVar()
        self.month = StringVar()
        self.day = StringVar()
        self.hour = StringVar()
        self.minute = StringVar()

        # years
        year_box = ttk.Combobox(master, textvariable=self.year, values=cb(now.year, 1998))
        year_box.grid(row=2, column=0)
        year_box.set("Select years")

        # months
        month_box = ttk.Combobox(master, textvariable=self.month, values=cb(12, 0))
        month_box.grid(row=3, column=0)
        month_box.set("Select months")

        # days
        day_box = ttk.Combobox(master, textvariable=self.day, values=cb(31, 0))
        day_box.grid(row=4, column=0)
        day_box.set("Select days")

        # hours
        hour_box = ttk.Combobox(master, textvariable=self.hour, values=cb(23, -1))
        hour_box.grid(row=5, column=0)
        hour_box.set("Select hours")

        # minutes
        minute_box = ttk.Combobox(master, textvariable=self.minute, values=cb(59, -1))
        minute_box.grid(row=6, column=0)
        minute_box.set("Select minutes")

        # final button
        final = ttk.Button(master, text="Change File", command=self.finalize)
        final.grid(row=8, column=0)

    def cf(self):  # choose file
        sel_str = str(filedialog.askopenfile(parent=self.master, title='Select a File to Modify'))

        # sel_str -> '/Users/...'
        if sel_str != -1:
            self.master.fl = par(sel_str)

    def conv_times(self, y, mo, d, h, mi):
        # return's a file's last modified times
        lm = rem_excess(time.ctime(os.path.getmtime(self.master.fl)).split(' '))

        if (len(y) == 0) or (y == "Do not modify") or (y == "Select years"):
            y = int(lm[-1])
        if (len(mo) == 0) or (mo == "Do not modify") or (mo == "Select months"):
            mo = int(switch_months(lm[1]))
        if (len(d) == 0) or (d == "Do not modify") or (d == "Select days"):
            d = int(lm[2])
        if (len(h) == 0) or (h == "Do not modify") or (h == "Select hours"):
            hm = lm[3].split(":")
            h = int(hm[0])
        if (len(mi) == 0) or (mi == "Do not modify") or (mi == "Select minutes"):
            hm = lm[3].split(":")
            mi = int(hm[0])
        return int(y), int(mo), int(d), int(h), int(mi)

    def finalize(self):
        y, mo, d, h, mi = self.conv_times(self.year.get(), self.month.get(),
                                          self.day.get(), self.hour.get(), self.minute.get())
        if not self.master.fl:
            self.label.config(text="Choose a valid file!")
        elif not check_dates(y, mo, d):
            self.label.config(text="Choose a valid date!")
        elif too_far_ahead(y, mo, d, h, mi):
            self.label.config(text="Choose a non-future date!")
        else:
            mod(y, mo, d, h, mi, self.master.fl)
            self.label.config(text="Modified time converted!")


if opsys() == 0:
    root = Tk()
    app = Apple(root)
    root.mainloop()
