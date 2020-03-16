import os.path, time
from datetime import datetime
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
        self.master.fl = None
        self.label = ttk.Label(master, text="Welcome")
        self.label.grid(row=0, column=0, columnspan=2)

        # collects route
        ttk.Button(master, text="Choose File", command=self.cf).grid(row=1, column=0)

        now = datetime.now()
        # time variables
        self.year = StringVar()
        self.month = StringVar()
        self.day = StringVar()
        self.hour = StringVar()
        self.minute = StringVar()

        # years
        year_box = ttk.Combobox(master, textvariable=self.year, values=self.cb(now.year, 1998))
        year_box.grid(row=2, column=0)
        year_box.set("Select years")

        # months
        month_box = ttk.Combobox(master, textvariable=self.month, values=self.cb(12, 0))
        month_box.grid(row=3, column=0)
        month_box.set("Select months")

        # days
        day_box = ttk.Combobox(master, textvariable=self.day, values=self.cb(31, 0))
        day_box.grid(row=4, column=0)
        day_box.set("Select days")

        # hours
        hour_box = ttk.Combobox(master, textvariable=self.hour, values=self.cb(23, -1))
        hour_box.grid(row=5, column=0)
        hour_box.set("Select hours")

        # minutes
        minute_box = ttk.Combobox(master, textvariable=self.minute, values=self.cb(59, -1))
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

    def cb(self, s, e):
        l = [i for i in range(s, e, -1)]
        l.insert(0, "Do not modify")
        return l

    def check_dates(self):
        lm = time.ctime(os.path.getmtime(self.master.fl)).split(' ')
        year = self.year.get()
        month = self.month.get()
        day = self.month.get()
        hour = self.month.get()
        minute = self.month.get()
        if (len(year) == 0) or (year == "Do not modify"):
            year = int(lm[-1])
        if (len(month) == 0) or (month == "Do not modify"):
            month = lm[1]
            if month == "Jan":
                month = 1
            elif month == "Feb":
                month = 2
            elif month == "Mar":
                month = 3
            elif month == "Apr":
                month = 4
            elif month == "May":
                month = 5

    def finalize(self):
        if not self.master.fl:
            self.label.config(text="Choose a valid file!")
        # elif self.check_dates():
        #     ...

if opsys() == 0:
    root = Tk()
    app = Apple(root)
    root.mainloop()
