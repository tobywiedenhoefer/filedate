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
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
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

    if y < ny:
        return False

    # construct num of mo + d + h + mi in seconds
    std_mi = 60
    std_h = std_mi * 60
    std_d = std_h * 24
    std_mo = std_d * 29  # just estimation
    now_seconds = (nmo * std_mo) + (nd * std_d) + (nh * std_h) + (nmi * std_mi)
    entered_seconds = (mo * std_mo) + (d * std_d) + (h * std_h) + (mi * std_mi)
    diff = now_seconds - entered_seconds
    if diff >= 0:  # it is ok, although odd, to update the time modified to now.
        return False
    return True


def check_dates(y, mo, d):  # returns whether a date is possible
    valid = True
    try:
        datetime(y, mo, d)
    except:
        valid = False
    return valid


class Apple:
    def __init__(self, master):
        master.title('Modify File Date')
        master.resizable(False, False)

        self.master = master
        self.master.fl = None
        self.label = ttk.Label(master, text="Welcome")
        self.label.pack()

        # collects route
        ttk.Button(master, text="Choose a File", command=self.cf).pack()

        now = datetime.now()
        # time variables
        self.year = StringVar()
        self.month = StringVar()
        self.day = StringVar()
        self.hour = StringVar()
        self.minute = StringVar()

        # years
        year_box = ttk.Combobox(master, textvariable=self.year, values=cb(now.year, 1997))
        year_box.set("Select years")
        year_box.pack()

        # months
        month_box = ttk.Combobox(master, textvariable=self.month, values=cb(12, 0))
        month_box.set("Select months")
        month_box.pack()

        # days
        day_box = ttk.Combobox(master, textvariable=self.day, values=cb(31, 0))
        day_box.set("Select days")
        day_box.pack()

        # hours
        hour_box = ttk.Combobox(master, textvariable=self.hour, values=cb(23, -1))
        hour_box.pack()
        hour_box.set("Select hours")

        # minutes
        minute_box = ttk.Combobox(master, textvariable=self.minute, values=cb(59, -1))
        minute_box.pack()
        minute_box.set("Select minutes")

        # final button
        final = ttk.Button(master, text="Change File", command=lambda: self.finalize(
            self.conv_times(self.year.get(), self.month.get(), self.day.get(), self.hour.get(), self.minute.get())))
        final.pack()

    def cf(self):  # choose file
        # sel_str -> '/Users/...'
        sel_str = str(filedialog.askopenfile(parent=self.master, title='Select a File to Modify'))
        self.master.fl = par(sel_str)

    def conv_times(self, y, mo, d, h, mi):
        # return's a file's last modified times
        if self.master.fl is None:
            return 0, 0, 0, 0, 0
        lm = rem_excess(time.ctime(os.path.getmtime(self.master.fl)).split(' '))

        if (y == "Do not modify") or (y == "Select years"):
            y = int(lm[-1])
        if (mo == "Do not modify") or (mo == "Select months"):
            mo = int(switch_months(lm[1]))
        if (d == "Do not modify") or (d == "Select days"):
            d = int(lm[2])
        if (h == "Do not modify") or (h == "Select hours"):
            hm = lm[3].split(":")
            h = int(hm[0])
        if (mi == "Do not modify") or (mi == "Select minutes"):
            hm = lm[3].split(":")
            mi = int(hm[1])
        return int(y), int(mo), int(d), int(h), int(mi)

    def finalize(self, conv_times):
        y, mo, d, h, mi = conv_times
        if self.master.fl is None:
            self.label.config(text="Choose a valid file!")
        elif not check_dates(y, mo, d):
            self.label.config(text="Choose a valid date!")
        elif too_far_ahead(y, mo, d, h, mi):
            self.label.config(text="Choose a non-future date!")
        else:
            mod(y, mo, d, h, mi, self.master.fl)
            self.label.config(text="Modified time converted!")


if __name__ == '__main__':  # for unit testing
    if opsys() == 0:
        root = Tk()
        app = Apple(root)
        root.mainloop()
