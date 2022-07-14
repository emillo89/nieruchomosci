# import pytest
from webscrapping import change_zapytaj
import unittest

class TestString(unittest.TestCase):
    def test_change_zapytaj(self):
        output = change_zapytaj('zapytaj')
        expected = None

        self.assertEqual(output, expected)

    def test_change_zapytaj_good_value(self):
        output = change_zapytaj('goog_value')
        expected = 'goog_value'

        self.assertEqual(output, expected)
        

    def test_change_zapytaj_good_value(self):
        output = change_zapytaj('12344')
        expected = 'goog_value'

        self.assertEqual(output, expected)