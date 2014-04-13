from unittest import TestCase
from ..util import n2w


class TestUtil(TestCase):
    def test_n2w(self):
        """ Test converting numbers to words. """
        self.assertEquals(n2w(1), "One")
        self.assertEquals(n2w(10), "Ten")
        self.assertEquals(n2w(11), "Eleven")
        self.assertEquals(n2w(22), "Twentytwo")
        self.assertEquals(n2w(99), "Ninetynine")
