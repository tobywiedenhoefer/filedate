import unittest
from datetime import datetime
from tkinter import *
from main import par, rem_excess, check_dates, too_far_ahead

now = datetime.now()
ny = int(now.year)
nmo = int(now.month)
nd = int(now.day)
nh = int(now.hour)
nmi = int(now.minute)


class TestMain(unittest.TestCase):
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
        self.assertTrue(too_far_ahead(ny, nmo, nd, nh, nmi + 1))  # minutes
        self.assertTrue(too_far_ahead(ny, nmo, nd, nh + 1, nmi))  # hours
        self.assertTrue(too_far_ahead(ny, nmo, nd + 1, nh, nmi))  # days
        self.assertTrue(too_far_ahead(ny, nmo + 1, nd, nh, nmi))  # months
        self.assertFalse(too_far_ahead(1998, 12, 25, 12, 12))  # past date



if __name__ == '__main__':
    unittest.main()
