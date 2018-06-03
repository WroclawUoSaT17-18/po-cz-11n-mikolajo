import unittest
from tkinter import *
from test import mainWindow
from unittest import TestCase

class TestMainWindow(TestCase):

    def test_class_init(self):
        root = Tk()
        window_1 = mainWindow(root)

        self.assertEqual(window_1.popup(), None) # sama obsluga okna wpisywania


if __name__ == "__main__":
    unittest.main()