from unittest import TestCase
from ..util import number_to_words


class TestUtil(TestCase):
    def test_number_to_words(self):
        """ Test converting numbers to words. """
        self.assertEquals(number_to_words(1), "One")
        self.assertEquals(number_to_words(10), "Ten")
        self.assertEquals(number_to_words(11), "Eleven")
        self.assertEquals(number_to_words(22), "Twentytwo")
        self.assertEquals(number_to_words(99), "Ninetynine")
