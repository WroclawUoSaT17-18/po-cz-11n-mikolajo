import unittest
from tkinter import *
from test import mainWindow
from unittest import TestCase


#      ~~~~~~~~~~~~~~~~TEST CASE INTRODUCTION~~~~~~~~~~~~~~~~

#       Testujemy funkcjonalność inicjalizacji klasy okna
#       biblioteki Tkinter, tworzony jest obiekt,
#       następnie sprawdzana jest poprawność działania
#       wprowadzania danych do okna dialogowego.
#       Testowana wartość to "przykladowa wartosc"
#       sprawdzamy formatowanie.

class TestMainWindow(TestCase):

    def test_class_init(self):
        root = Tk()
        window_1 = mainWindow(root)
        value = 'przyklad'

        self.assertEqual(window_1.popup(), None)  # sama obsluga okna wpisywania
        self.assertEqual(window_1.entryValue(), value)  # w okno wpisz 'przykladowa wartosc'
        self.addTypeEqualityFunc(str, window_1.entryValue()) #sprawdzenie czy typ danych otrzymywany z okna to string


if __name__ == "__main__":
    unittest.main()
