import datetime
import time
import os


def mod(y, mo, d, h, mi, floc):
    date = datetime.datetime(y, mo, d, h, mi)
    modtime = time.mktime(date.timetuple())
    os.utime(floc, (modtime, modtime))
