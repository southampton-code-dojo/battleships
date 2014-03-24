from unittest import TestCase
from ..competition import Entry


class TestEntry(TestCase):
    def test_entry_records_wins(self):
        """ Test the entry records wins. """
        entry = Entry(1, ai=None)
        self.assertEquals(entry.wins, 0)

        entry.win(1)
        self.assertEquals(entry.wins, 1)
        self.assertEquals(entry.losses, 0)
        self.assertEquals(entry.total_games, 1)

    def test_entry_records_losses(self):
        """ Test the entry records wins. """
        entry = Entry(1, ai=None)
        self.assertEquals(entry.losses, 0)

        entry.lose(1)
        self.assertEquals(entry.wins, 0)
        self.assertEquals(entry.losses, 1)
        self.assertEquals(entry.total_games, 1)

    def test_clear_results(self):
        """ Test an entry can clear results for a given opponent. """
        entry = Entry(1, ai=None)

        entry.win(1)
        entry.lose(1)
        entry.win(2)

        self.assertEquals(entry.wins, 2)
        self.assertEquals(entry.losses, 1)
        self.assertEquals(entry.total_games, 3)

        entry.clear_results(1)

        self.assertEquals(entry.wins, 1)
        self.assertEquals(entry.losses, 0)
        self.assertEquals(entry.total_games, 1)

    def test_clear_all_results(self):
        """ Test an entry can clear all results. """
        entry = Entry(1, ai=None)

        entry.win(1)
        entry.lose(1)
        entry.win(2)

        self.assertEquals(entry.wins, 2)
        self.assertEquals(entry.losses, 1)
        self.assertEquals(entry.total_games, 3)

        entry.clear_results()

        self.assertEquals(entry.wins, 0)
        self.assertEquals(entry.losses, 0)
        self.assertEquals(entry.total_games, 0)