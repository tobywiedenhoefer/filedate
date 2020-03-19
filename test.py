import unittest
import time
import os
from datetime import datetime
from tkinter import *
from main import par, rem_excess, check_dates, too_far_ahead, switch_months
from main import Apple


class TestStatic(unittest.TestCase):

    def setUp(self):
        self.now = datetime.now()
        self.ny = int(self.now.year)
        self.nmo = int(self.now.month)
        self.nd = int(self.now.day)
        self.nh = int(self.now.hour)
        self.nmi = int(self.now.minute)

    def test_par(self):
        # parse directory
        ideal_string = "/Users/somewhere/filedate/test.txt"

        # running str(filedialog.askopenfile(parent=self.master, title='Select a File to Modify')), we get:
        s = "<_io.TextIOWrapper name='/Users/somewhere/filedate/test.txt' mode='r' encoding='UTF-8'>"
        self.assertEqual(ideal_string, par(s))

    def test_refine_list(self):
        ideal_list = ['Sun', 'Feb', '2', '02:02:00', '2020']

        # problem that occurs with modifying a modified file
        incorrect_list = ['Sun', 'Feb', '', '2', '02:02:00', '2020']
        self.assertEqual(ideal_list, rem_excess(incorrect_list))

    def test_check_date(self):
        y, mo, d = 2020, 12, 31
        self.assertTrue(check_dates(y, mo, d))
        y, mo, d = 2019, 2, 29
        self.assertFalse(check_dates(y, mo, d))

    def test_too_far_ahead(self):
        self.assertTrue(too_far_ahead(self.ny, self.nmo, self.nd, self.nh, self.nmi + 1))  # minutes
        self.assertTrue(too_far_ahead(self.ny, self.nmo, self.nd, self.nh + 1, self.nmi))  # hours
        self.assertTrue(too_far_ahead(self.ny, self.nmo, self.nd + 1, self.nh, self.nmi))  # days
        self.assertTrue(too_far_ahead(self.ny, self.nmo + 1, self.nd, self.nh, self.nmi))  # months
        self.assertFalse(too_far_ahead(1998, 12, 25, 12, 12))  # past date


class TestApple(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        root = Tk()
        cls.app = Apple(root)
        with open("unittest.txt", "w+") as _:
            cls.app.master.fl = "unittest.txt"
        file_date = rem_excess(time.ctime(os.path.getmtime(cls.app.master.fl)).split(' '))
        cls.expected_time = [int(file_date[-1]), switch_months(file_date[1]),
                             int(file_date[2]), int(file_date[3].split(":")[0]), int(file_date[3].split(":")[1])]

    @classmethod
    def tearDownClass(cls):
        os.remove("unittest.txt")

    def test_conv_times(self):
        # test 'do not modify'
        y, mo, d, h, mi = self.app.conv_times("Do not modify", "Do not modify",
                                              "Do not modify", "Do not modify", "Do not modify")
        self.assertEqual(self.expected_time, [y, mo, d, h, mi])

        # nothing selected, for whatever reason
        y, mo, d, h, mi = self.app.conv_times("Select years", "Select months",
                                              "Select days", "Select hours", "Select minutes")
        self.assertEqual(self.expected_time, [y, mo, d, h, mi])

    def test_finalize(self):
        # testing whether the file was modified
        self.app.finalize(self.app.conv_times(2020, 2, 20, 0, 0))
        file_date = rem_excess(time.ctime(os.path.getmtime(self.app.master.fl)).split(' '))
        file_date = [int(file_date[-1]), switch_months(file_date[1]), int(file_date[2]),
                     int(file_date[3].split(":")[0]), int(file_date[3].split(":")[1])]
        self.assertEqual(file_date, [2020, 2, 20, 0, 0])
        self.assertEqual(self.app.label.cget("text"), "Modified time converted!")

        # invalid date
        self.app.finalize(self.app.conv_times(2019, 2, 29, 0, 0))
        self.assertEqual(self.app.label.cget("text"), "Choose a valid date!")

        # future date
        self.app.finalize(self.app.conv_times(2020, 12, 31, 0, 0))
        self.assertEqual(self.app.label.cget("text"), "Choose a non-future date!")

        # invalid file
        self.app.master.fl = None
        self.app.finalize(self.app.conv_times(2020, 3, 19, 0, 0))
        self.assertEqual(self.app.label.cget("text"), "Choose a valid file!")


if __name__ == '__main__':
    unittest.main()
