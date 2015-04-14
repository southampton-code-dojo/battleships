from unittest import TestCase
from ..util import number_to_words, format_grid


class TestUtil(TestCase):
    def test_number_to_words(self):
        """ Test converting numbers to words. """
        self.assertEquals(number_to_words(1), "One")
        self.assertEquals(number_to_words(10), "Ten")
        self.assertEquals(number_to_words(11), "Eleven")
        self.assertEquals(number_to_words(22), "Twentytwo")
        self.assertEquals(number_to_words(99), "Ninetynine")

    def test_format_grid(self):
        """ Test formatting a grid. """
        formatted = format_grid([[1,2,3],[4,5,6],[7,8,9]])
        s = formatted.split()
        self.assertEquals(s, ["1", "4", "7", "2", "5", "8", "3", "6", "9"])
